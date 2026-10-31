from flask import Blueprint, request, jsonify
from models import BrandGuideline, ApprovedFact, EvaluationFlag, db
from engines.tone_calibrator import ToneCalibrator
from engines.claims_checker import ClaimsFactChecker
from engines.regulatory_engine import regulatory_engine
from engines.url_scanner import url_scanner_engine
from engines.ai_copilot import ai_copilot

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/scan', methods=['POST'])
def api_scan():
    """Programmatic API endpoint to scan draft text."""
    data = request.get_json() or {}
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'Missing text parameter in request body'}), 400

    guidelines = BrandGuideline.query.filter_by(is_active=True).all()
    approved_facts = ApprovedFact.query.filter_by(is_active=True).all()

    tone_res = ToneCalibrator(guidelines).evaluate(text)
    claim_res = ClaimsFactChecker(approved_facts, guidelines).evaluate(text)

    all_flags = tone_res['flags'] + claim_res['flags']
    overall_score = int((tone_res['score'] * 0.45) + (claim_res['score'] * 0.55))

    return jsonify({
        'status': 'success',
        'overall_score': overall_score,
        'tone_score': tone_res['score'],
        'claim_score': claim_res['score'],
        'flag_count': len(all_flags),
        'flags': all_flags
    })

@api_bp.route('/guidelines', methods=['GET'])
def api_guidelines():
    guidelines = BrandGuideline.query.filter_by(is_active=True).all()
    return jsonify([{
        'rule_code': g.rule_code,
        'category': g.category,
        'title': g.rule_title,
        'severity': g.severity,
        'citation': g.citation_ref
    } for g in guidelines])

# =============================================================================
# BRANDGUARD AI CO-PILOT API ENDPOINTS
# =============================================================================

@api_bp.route('/ai/harmonize', methods=['POST'])
def ai_harmonize():
    """
    AI Deep Semantic Rewrite: Polishes marketing copy to eliminate clichés,
    aggressive polarities, and unsubstantiated claims while preserving brand voice.
    """
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    voice = data.get('voice', 'ENTERPRISE_CONSULTATIVE')

    if not content:
        return jsonify({'success': False, 'message': 'No content provided for harmonization.'}), 400

    result = ai_copilot.harmonize_draft(content, brand_voice=voice)
    return jsonify(result)


@api_bp.route('/ai/safe-harbor', methods=['POST'])
def ai_safe_harbor():
    """
    AI Regulatory Disclaimer Synthesizer: Generates FTC Section 5,
    SEC safe harbor, and WCAG accessibility disclaimers.
    """
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    domain = data.get('domain', 'enterprise_tech')

    if not content:
        return jsonify({'success': False, 'message': 'No content provided.'}), 400

    result = ai_copilot.generate_safe_harbor(content, domain=domain)
    return jsonify(result)


@api_bp.route('/ai/chat', methods=['POST'])
def ai_chat():
    """
    Interactive BrandGuard AI Co-Pilot chat endpoint.
    Answers compliance questions, explains rules, and suggests rewrites.
    """
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    context_text = data.get('context', '')

    if not message:
        return jsonify({'success': False, 'reply': 'Please ask a brand governance or compliance question.'}), 400

    result = ai_copilot.chat(message, context_text=context_text)
    return jsonify({
        'success': True,
        'reply': result.get('reply', ''),
        'source': result.get('source', 'BrandGuard AI Co-Pilot')
    })


@api_bp.route('/ai/suggest-guideline', methods=['POST'])
def ai_suggest_guideline():
    """
    AI Guideline Synthesizer: Converts a plain topic prompt into a
    structured brand guideline definition ready for database ingestion.
    """
    data = request.get_json() or {}
    topic = data.get('topic', '').strip()

    if not topic:
        return jsonify({'success': False, 'message': 'Please provide a guideline topic.'}), 400

    result = ai_copilot.synthesize_guideline(topic)
    return jsonify(result)


@api_bp.route('/ai/status', methods=['GET'])
def ai_status():
    """Returns real-time telemetry on active AI engine (Gemini Cloud vs Local Semantic)."""
    return jsonify(ai_copilot.get_status())


# =============================================================================
# NEW ENDPOINTS — PHASE 2 UPGRADE
# =============================================================================

@api_bp.route('/ai/analyze', methods=['POST'])
def ai_analyze():
    """
    Full Submission Analysis: Performs structured deep-analysis of marketing copy.
    Returns tone_issues, claim_risks, suggested_improvements, and overall_quality_rating.
    Uses Google Gemini when available, else falls back to local heuristics.
    """
    data = request.get_json() or {}
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'success': False, 'message': 'No content provided for analysis.'}), 400

    result = ai_copilot.analyze_submission(content)
    return jsonify(result)


@api_bp.route('/ai/headlines', methods=['POST'])
def ai_headlines():
    """
    Headline Variant Generator: Produces 5 compliant, enterprise-grade headline
    variants for a given topic or draft text.
    Uses Google Gemini when available, else template-based local generation.
    """
    data = request.get_json() or {}
    topic = data.get('topic', data.get('content', '')).strip()

    if not topic:
        return jsonify({'success': False, 'message': 'No topic or content provided.'}), 400

    result = ai_copilot.generate_headline_variants(topic)
    return jsonify(result)


@api_bp.route('/ai/explain-flag', methods=['POST'])
def ai_explain_flag():
    """
    Flag Explainer: Returns a detailed educational explanation of a compliance flag,
    including why it was flagged, real-world consequences, alternative phrasings,
    and the governing regulation in plain language.
    """
    data = request.get_json() or {}
    flag_data = data.get('flag', data)  # Accept either {flag: {...}} or flat dict

    if not flag_data:
        return jsonify({'success': False, 'message': 'No flag data provided.'}), 400

    result = ai_copilot.explain_flag(flag_data)
    return jsonify(result)


@api_bp.route('/ai/test-key', methods=['GET'])
def ai_test_key():
    """
    Gemini API Key Diagnostic: Tests the configured Gemini API key and connection.
    Returns detailed diagnostic information including key format validation,
    model availability, and connection status.
    """
    result = ai_copilot.test_connection()
    status_code = 200 if result.get('success') else 503
    return jsonify(result), status_code


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Extended Health Check: Returns overall system health including database status,
    AI engine status, and key configuration checks.
    """
    from models import db

    # Database health
    db_ok = False
    db_message = "Unknown"
    try:
        db.session.execute(db.text('SELECT 1'))
        db_ok = True
        db_message = "Connected"
    except Exception as e:
        db_message = str(e)

    # AI engine status
    ai_status_data = ai_copilot.get_status()

    return jsonify({
        "status": "healthy" if db_ok else "degraded",
        "database": {
            "ok": db_ok,
            "message": db_message
        },
        "ai_engine": {
            "active_engine": ai_status_data.get("active_engine"),
            "is_cloud_active": ai_status_data.get("is_cloud_active"),
            "key_valid": ai_status_data.get("key_valid"),
            "warning": ai_status_data.get("warning")
        },
        "version": "2.0.0",
        "engines": {
            "tone_calibrator": "online",
            "claims_checker": "online",
            "visual_inspector": "online",
            "ai_copilot": "online",
            "regulatory_engine": "online",
            "url_scanner_engine": "online"
        }
    })


# =============================================================================
# ENTERPRISE EXTENSIONS — REGULATORY, URL SCANNER & CI/CD GATES
# =============================================================================

@api_bp.route('/regulatory/evaluate', methods=['POST'])
def api_regulatory_evaluate():
    """
    Evaluates text against SEC AI-Washing, EU AI Act, and UK CMA Green Claims.
    Payload: { "text": "...", "jurisdiction": "US|EU|UK|GLOBAL" }
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    jurisdiction = data.get('jurisdiction', 'GLOBAL').strip().upper()

    if not text:
        return jsonify({'error': 'Missing text parameter in request body'}), 400

    result = regulatory_engine.evaluate(text, jurisdiction=jurisdiction)
    return jsonify(result)


@api_bp.route('/regulatory/disclaimer', methods=['POST'])
def api_regulatory_disclaimer():
    """
    Generates jurisdictional regulatory safe harbor / compliance disclaimers.
    Payload: { "text": "...", "jurisdiction": "US|EU|UK|GLOBAL" }
    """
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    jurisdiction = data.get('jurisdiction', 'GLOBAL').strip().upper()

    disclaimer = regulatory_engine.generate_tailored_disclaimer(text, jurisdiction=jurisdiction)
    all_disclaimers = regulatory_engine.generate_disclaimers(text, jurisdiction=jurisdiction)

    return jsonify({
        'jurisdiction': jurisdiction,
        'disclaimer': disclaimer,
        'all_disclaimers': all_disclaimers
    })


@api_bp.route('/scan-url', methods=['POST'])
def api_scan_url():
    """
    Crawls and extracts live web page copy from URL.
    Payload: { "url": "https://..." }
    """
    data = request.get_json() or {}
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'Missing url parameter in request body'}), 400

    result = url_scanner_engine.fetch_url_content(url)
    status_code = 200 if result.get('success') else 400
    return jsonify(result), status_code


@api_bp.route('/competitor-benchmark', methods=['POST'])
def api_competitor_benchmark():
    """
    Audits competitor copy, identifies claim vulnerabilities against SQL Truth Bank,
    and synthesizes sales battlecards and counter-messaging.
    Payload: { "url": "...", "content": "...", "competitor_name": "..." }
    """
    data = request.get_json() or {}
    url = data.get('url', '').strip()
    content = data.get('content', '').strip()
    competitor_name = data.get('competitor_name', 'Competitor').strip() or "Competitor"

    if url and not content:
        fetch_res = url_scanner_engine.fetch_url_content(url)
        if not fetch_res.get('success'):
            return jsonify(fetch_res), 400
        content = fetch_res.get('content', '')
        if competitor_name == "Competitor":
            competitor_name = fetch_res.get('title', 'Competitor')[:40]

    if not content:
        return jsonify({'error': 'Provide either a valid url or textual content'}), 400

    approved_facts = ApprovedFact.query.filter_by(is_active=True).all()
    url_scanner_engine.ai_copilot = ai_copilot
    result = url_scanner_engine.audit_competitor_claims(
        content=content,
        title=competitor_name,
        approved_facts=approved_facts,
        competitor_name=competitor_name
    )
    return jsonify(result)


@api_bp.route('/guidelines/auto-remediate', methods=['POST'])
def api_guideline_auto_remediate():
    """
    AI Ambiguity Resolver API: Evaluates creator dispute justifications and
    returns a clarified rule amendment.
    Payload: { "rule_code": "BG-TONE-01", "override_reasons": [...] }
    """
    data = request.get_json() or {}
    rule_code = data.get('rule_code', '').strip().upper()
    override_reasons = data.get('override_reasons', [])

    rule = BrandGuideline.query.filter_by(rule_code=rule_code).first()
    if not rule:
        return jsonify({'error': f"Rule '{rule_code}' not found."}), 404

    if not override_reasons:
        disputed_flags = EvaluationFlag.query.filter_by(guideline_id=rule.id).filter(
            EvaluationFlag.status.in_(['DISMISSED', 'OVERRIDDEN'])
        ).all()
        override_reasons = [f.override_reason for f in disputed_flags if f.override_reason]

    result = ai_copilot.remediate_rule_ambiguity(
        rule_code=rule.rule_code,
        current_title=rule.rule_title,
        current_description=rule.rule_description,
        current_patterns=rule.forbidden_patterns or "",
        current_replacement=rule.recommended_replacement or "",
        override_reasons=override_reasons
    )
    return jsonify(result)


@api_bp.route('/gate/check', methods=['POST'])
def api_ci_cd_quality_gate():
    """
    CI/CD Pre-Publication Stage-Gate Endpoint:
    Designed for GitHub Actions, CMS webhooks, and automated deployment pipelines.
    Payload:
    {
      "content": "...",
      "title": "PR Release",
      "threshold": 85,
      "jurisdiction": "GLOBAL",
      "block_on_critical": true,
      "department": "Content Marketing"
    }

    Returns:
    - HTTP 200 with { pass: true, ... } if content passes the gate.
    - HTTP 422 with { pass: false, ... } if content is blocked.
    """
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    title = data.get('title', 'CI/CD Pipeline Content').strip()
    threshold = int(data.get('threshold', 85))
    jurisdiction = data.get('jurisdiction', 'GLOBAL').strip().upper()
    block_on_critical = bool(data.get('block_on_critical', True))
    department = data.get('department', 'Engineering/CI')

    if not content:
        return jsonify({
            'pass': False,
            'status': 'REJECTED_EMPTY_CONTENT',
            'error': 'Missing content parameter in request body'
        }), 400

    # 1. Run Tone Engine
    guidelines = BrandGuideline.query.filter_by(is_active=True).all()
    approved_facts = ApprovedFact.query.filter_by(is_active=True).all()

    tone_res = ToneCalibrator(guidelines).evaluate(content)
    claim_res = ClaimsFactChecker(approved_facts, guidelines).evaluate(content)
    reg_res = regulatory_engine.evaluate(content, jurisdiction=jurisdiction)

    all_flags = tone_res['flags'] + claim_res['flags'] + reg_res['flags']
    overall_score = int(
        (tone_res['score'] * 0.30) +
        (claim_res['score'] * 0.35) +
        (reg_res['score'] * 0.35)
    )

    critical_violations = [f for f in all_flags if f.get('severity') == 'CRITICAL']
    warning_violations = [f for f in all_flags if f.get('severity') == 'WARNING']

    # Determine gate pass / fail
    is_blocked_by_critical = block_on_critical and len(critical_violations) > 0
    passed = (overall_score >= threshold) and not is_blocked_by_critical

    response_payload = {
        'pass': passed,
        'status': 'APPROVED_STAGE_GATE' if passed else 'BLOCKED_STAGE_GATE',
        'score': overall_score,
        'threshold': threshold,
        'tone_score': tone_res['score'],
        'claim_score': claim_res['score'],
        'regulatory_score': reg_res['score'],
        'jurisdiction': jurisdiction,
        'blocking_violations': critical_violations if is_blocked_by_critical or not passed else [],
        'flag_summary': {
            'total': len(all_flags),
            'critical': len(critical_violations),
            'warning': len(warning_violations),
            'suggestion': len(all_flags) - len(critical_violations) - len(warning_violations)
        },
        'disclaimers': reg_res.get('disclaimers', {}),
        'summary': (
            f"Content passed BrandGuard Stage-Gate ({overall_score}/100 >= {threshold}%)."
            if passed else
            f"Blocked by BrandGuard CI/CD Quality Gate: Score {overall_score}/100 (Threshold: {threshold}%) with {len(critical_violations)} critical violations."
        )
    }

    status_code = 200 if passed else 422
    return jsonify(response_payload), status_code

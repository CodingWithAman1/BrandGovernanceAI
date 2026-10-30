from flask import Blueprint, request, jsonify
from models import BrandGuideline, ApprovedFact
from engines.tone_calibrator import ToneCalibrator
from engines.claims_checker import ClaimsFactChecker
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

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import BrandGuideline, ApprovedFact, BrandAsset, db

guidelines_bp = Blueprint('guidelines', __name__, url_prefix='/guidelines')

@guidelines_bp.route('/')
@login_required
def list_all():
    guidelines = BrandGuideline.query.order_by(BrandGuideline.category, BrandGuideline.rule_code).all()
    approved_facts = ApprovedFact.query.order_by(ApprovedFact.created_at.desc()).all()
    brand_assets = BrandAsset.query.all()
    
    return render_template(
        'guidelines/list.html',
        guidelines=guidelines,
        approved_facts=approved_facts,
        brand_assets=brand_assets
    )

@guidelines_bp.route('/rule/add', methods=['POST'])
@login_required
def add_rule():
    if current_user.role not in ['MANAGER', 'ADMIN']:
        flash("Only Managers and Admins can create brand rules.", "danger")
        return redirect(url_for('guidelines.list_all'))

    rule_code = request.form.get('rule_code', '').strip().upper()
    category = request.form.get('category', 'TONE')
    rule_title = request.form.get('rule_title', '').strip()
    rule_description = request.form.get('rule_description', '').strip()
    severity = request.form.get('severity', 'WARNING')
    forbidden_patterns = request.form.get('forbidden_patterns', '').strip()
    recommended_replacement = request.form.get('recommended_replacement', '').strip()
    citation_ref = request.form.get('citation_ref', '').strip()

    if not rule_code or not rule_title or not rule_description:
        flash("Rule code, title, and description are required.", "danger")
        return redirect(url_for('guidelines.list_all'))

    # Check for duplicate rule code
    if BrandGuideline.query.filter_by(rule_code=rule_code).first():
        flash(f"Rule code '{rule_code}' already exists.", "warning")
        return redirect(url_for('guidelines.list_all'))

    new_rule = BrandGuideline(
        rule_code=rule_code,
        category=category,
        rule_title=rule_title,
        rule_description=rule_description,
        severity=severity,
        forbidden_patterns=forbidden_patterns,
        recommended_replacement=recommended_replacement,
        citation_ref=citation_ref
    )
    db.session.add(new_rule)
    db.session.commit()
    flash(f"Brand rule {rule_code} added successfully!", "success")
    return redirect(url_for('guidelines.list_all'))

@guidelines_bp.route('/fact/add', methods=['POST'])
@login_required
def add_fact():
    if current_user.role not in ['REVIEWER', 'MANAGER', 'ADMIN']:
        flash("Only Reviewers and Managers can add approved claims.", "danger")
        return redirect(url_for('guidelines.list_all'))

    topic = request.form.get('topic', '').strip()
    claim_statement = request.form.get('claim_statement', '').strip()
    approved_source_link = request.form.get('approved_source_link', '').strip()
    evidence_excerpt = request.form.get('evidence_excerpt', '').strip()
    expiration_date = request.form.get('expiration_date', '').strip()

    if not topic or not claim_statement:
        flash("Topic and verified claim statement are required.", "danger")
        return redirect(url_for('guidelines.list_all'))

    new_fact = ApprovedFact(
        topic=topic,
        claim_statement=claim_statement,
        approved_source_link=approved_source_link,
        evidence_excerpt=evidence_excerpt,
        expiration_date=expiration_date
    )
    db.session.add(new_fact)
    db.session.commit()
    flash("Approved claim and evidence added to truth bank!", "success")
    return redirect(url_for('guidelines.list_all'))

@guidelines_bp.route('/asset/add', methods=['POST'])
@login_required
def add_asset():
    if current_user.role not in ['MANAGER', 'ADMIN']:
        flash("Only Managers can add design tokens.", "danger")
        return redirect(url_for('guidelines.list_all'))

    name = request.form.get('name', '').strip()
    asset_type = request.form.get('asset_type', 'PALETTE')
    asset_value = request.form.get('asset_value', '').strip()

    if not name or not asset_value:
        flash("Asset name and value are required.", "danger")
        return redirect(url_for('guidelines.list_all'))

    new_asset = BrandAsset(name=name, asset_type=asset_type, asset_value=asset_value)
    db.session.add(new_asset)
    db.session.commit()
    flash(f"Design token '{name}' ({asset_value}) added!", "success")
    return redirect(url_for('guidelines.list_all'))

@guidelines_bp.route('/rule/remediate/<int:rule_id>', methods=['POST'])
@login_required
def remediate_rule(rule_id):
    """
    AI Ambiguity Resolver: Evaluates disputed rule overrides and automatically
    synthesizes a clarifying amendment into BrandGuideline.
    """
    if current_user.role not in ['MANAGER', 'ADMIN']:
        flash("Only Managers and Admins can amend brand rules.", "danger")
        return redirect(url_for('guidelines.list_all'))

    from models import EvaluationFlag
    from engines.ai_copilot import ai_copilot

    rule = BrandGuideline.query.get_or_404(rule_id)
    disputed_flags = EvaluationFlag.query.filter_by(guideline_id=rule.id).filter(
        EvaluationFlag.status.in_(['DISMISSED', 'OVERRIDDEN'])
    ).all()

    reasons = [f.override_reason for f in disputed_flags if f.override_reason]
    if not reasons:
        reasons = ["Creators noted rule lacks clear operational boundary conditions."]

    res = ai_copilot.remediate_rule_ambiguity(
        rule_code=rule.rule_code,
        current_title=rule.rule_title,
        current_description=rule.rule_description,
        current_patterns=rule.forbidden_patterns or "",
        current_replacement=rule.recommended_replacement or "",
        override_reasons=reasons
    )

    if res.get('success'):
        rule.rule_title = res.get('amended_title', rule.rule_title)
        rule.rule_description = res.get('amended_description', rule.rule_description)
        rule.forbidden_patterns = res.get('amended_forbidden_patterns', rule.forbidden_patterns)
        rule.recommended_replacement = res.get('amended_recommended_replacement', rule.recommended_replacement)
        db.session.commit()
        flash(f"Rule {rule.rule_code} auto-remediated via {res.get('engine_used')}: {res.get('explanation_of_amendment')}", "success")
    else:
        flash("AI Ambiguity Resolver could not process amendment at this time.", "warning")

    return redirect(url_for('guidelines.list_all'))


# =============================================================================
# BRAND VOICE DNA PROFILER & ARCHETYPE CALIBRATOR
# =============================================================================

@guidelines_bp.route('/brand-dna', methods=['GET', 'POST'])
@login_required
def brand_dna():
    """
    Brand Voice DNA Profiler:
    Extracts voice polarities, power lexicons, and prohibited synthetic clichés
    from unstructured brand manifestos, with 1-click rulebook commitment.
    """
    from engines.ai_copilot import ai_copilot

    archetypes = {
        'stripe': {
            'name': 'Enterprise Consultative (Stripe / AWS)',
            'sample': (
                "We believe infrastructure should be invisible, dependable, and rigorously architected. "
                "Our tone is consultative, clear, and grounded in empirical data. We avoid marketing fluff, "
                "unsubstantiated '#1' claims, and aggressive hype. We explain complex systems simply and treat "
                "developers and CFOs as discerning partners."
            )
        },
        'apple': {
            'name': 'Minimalist Precision (Apple / Braun)',
            'sample': (
                "Simplicity is the ultimate sophistication. Every word must earn its place. We craft experiences "
                "that feel intuitive, human, and thoughtfully restrained. We avoid corporate buzzwords, excessive adjectives, "
                "and synthetic filler. Our products speak with quiet confidence and meticulous craft."
            )
        },
        'nike': {
            'name': 'Bold Challenger (Nike / Liquid Death)',
            'sample': (
                "We champion the relentless pursuit of greatness. We speak with urgency, conviction, and fearless energy. "
                "We challenge the status quo, destroy complacency, and celebrate grit. Our voice is raw, direct, and unapologetic. "
                "Passive language has no place here."
            )
        }
    }

    dna_profile = None
    input_text = ""
    selected_archetype = ""

    if request.method == 'POST':
        action = request.form.get('action', 'analyze')
        
        if action == 'save_rule':
            if current_user.role not in ['MANAGER', 'ADMIN']:
                flash("Only Managers and Admins can commit brand rules to the official rulebook.", "warning")
            else:
                rule_title = request.form.get('rule_title', 'Voice DNA Calibrated Rule').strip()
                rule_desc = request.form.get('rule_desc', '').strip()
                banned = request.form.get('banned_patterns', '').strip()
                replacement = request.form.get('replacement', '').strip()
                
                existing_count = BrandGuideline.query.filter(BrandGuideline.rule_code.like('BG-DNA-%')).count()
                rule_code = f"BG-DNA-{existing_count + 1:02d}"

                new_rule = BrandGuideline(
                    rule_code=rule_code,
                    category='TONE',
                    rule_title=rule_title,
                    rule_description=rule_desc,
                    severity='WARNING',
                    forbidden_patterns=banned,
                    recommended_replacement=replacement,
                    citation_ref=f"Brand Voice DNA § {rule_code}"
                )
                db.session.add(new_rule)
                db.session.commit()
                flash(f"Brand Voice Rule '{rule_code}: {rule_title}' successfully committed to Rulebook!", "success")
                return redirect(url_for('guidelines.list_all'))

        selected_archetype = request.form.get('archetype', '')
        if selected_archetype in archetypes and not request.form.get('manifesto_text', '').strip():
            input_text = archetypes[selected_archetype]['sample']
        else:
            input_text = request.form.get('manifesto_text', '').strip()

        if input_text:
            dna_profile = ai_copilot.extract_brand_dna(input_text)
            flash(f"Brand Voice DNA Profile extracted via {dna_profile.get('engine_used', 'AI Engine')}!", "info")
        else:
            flash("Please enter manifesto text or select a voice archetype.", "warning")

    return render_template(
        'guidelines/brand_dna.html',
        archetypes=archetypes,
        dna_profile=dna_profile,
        input_text=input_text,
        selected_archetype=selected_archetype
    )

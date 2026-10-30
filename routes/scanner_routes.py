import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Submission, EvaluationFlag, BrandGuideline, ApprovedFact, BrandAsset, ReviewLog
from engines.tone_calibrator import ToneCalibrator
from engines.claims_checker import ClaimsFactChecker
from engines.visual_inspector import VisualInspector
from engines.ai_copilot import ai_copilot

scanner_bp = Blueprint('scanner', __name__, url_prefix='/scanner')

@scanner_bp.route('/studio')
@login_required
def studio():
    return render_template('scanner/studio.html')


@scanner_bp.route('/analyze', methods=['POST'])
@login_required
def analyze():
    title = request.form.get('title', 'Untitled Content Draft').strip()
    raw_content = request.form.get('content', '').strip()
    content_type = 'TEXT'
    file_path = None
    saved_filename = None

    # Handle file upload if provided
    file = request.files.get('asset_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext in current_app.config['ALLOWED_EXTENSIONS']:
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            saved_filename = f"{int(os.times().elapsed * 1000)}_{filename}"
            full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], saved_filename)
            file.save(full_path)
            file_path = f"uploads/{saved_filename}"
            if ext in ['png', 'jpg', 'jpeg', 'webp']:
                content_type = 'HYBRID' if raw_content else 'IMAGE_BANNER'

    if not raw_content and not file_path:
        flash("Please provide either draft text or an image asset to analyze.", "warning")
        return redirect(url_for('scanner.studio'))

    # Load guidelines, facts, and assets
    guidelines = BrandGuideline.query.filter_by(is_active=True).all()
    approved_facts = ApprovedFact.query.filter_by(is_active=True).all()
    brand_assets = BrandAsset.query.filter_by(is_approved=True).all()

    all_flags = []
    tone_score = 100
    claim_score = 100
    visual_score = 100

    # 1. Run Tone Engine
    if raw_content:
        tone_engine = ToneCalibrator(guidelines)
        tone_res = tone_engine.evaluate(raw_content)
        tone_score = tone_res['score']
        all_flags.extend(tone_res['flags'])

    # 2. Run Claims Engine
    if raw_content:
        claim_engine = ClaimsFactChecker(approved_facts, guidelines)
        claim_res = claim_engine.evaluate(raw_content)
        claim_score = claim_res['score']
        all_flags.extend(claim_res['flags'])

    # 3. Run Visual Engine if image uploaded
    extracted_ocr_text = ""
    dominant_colors = []
    if file_path and content_type in ['IMAGE_BANNER', 'HYBRID']:
        full_image_path = os.path.join(current_app.config['BASE_DIR'], 'static', file_path)
        visual_engine = VisualInspector(brand_assets)
        vis_res = visual_engine.evaluate_image(full_image_path)
        visual_score = vis_res['score']
        all_flags.extend(vis_res['flags'])
        dominant_colors = vis_res.get('dominant_colors', [])
        extracted_ocr_text = vis_res.get('extracted_text', '')

        # If OCR extracted text from the image, also run tone/claim checks on it!
        if extracted_ocr_text:
            ocr_claim_engine = ClaimsFactChecker(approved_facts, guidelines)
            ocr_claim_res = ocr_claim_engine.evaluate(extracted_ocr_text)
            for f in ocr_claim_res['flags']:
                f['snippet'] = f"[Text inside Image] {f['snippet']}"
                all_flags.append(f)

    # Compute Overall Compliance Score
    if content_type == 'TEXT':
        compliance_score = int((tone_score * 0.45) + (claim_score * 0.55))
    elif content_type == 'IMAGE_BANNER':
        compliance_score = visual_score
    else:
        compliance_score = int((tone_score * 0.3) + (claim_score * 0.4) + (visual_score * 0.3))

    # Save to Database
    submission = Submission(
        title=title,
        content_type=content_type,
        raw_content=raw_content,
        original_content=raw_content,
        file_path=file_path,
        creator_id=current_user.id,
        status='SCANNED',
        compliance_score=compliance_score,
        tone_score=tone_score,
        claim_score=claim_score,
        visual_score=visual_score
    )
    db.session.add(submission)
    db.session.commit()

    # Save Flags
    for f in all_flags:
        # Match guideline_id if available
        g_id = None
        if 'rule_code' in f:
            matched_g = BrandGuideline.query.filter_by(rule_code=f['rule_code']).first()
            if matched_g:
                g_id = matched_g.id

        flag = EvaluationFlag(
            submission_id=submission.id,
            guideline_id=g_id,
            flag_type=f.get('flag_type', 'GENERAL'),
            flagged_snippet=f.get('snippet', ''),
            explanation=f.get('explanation', ''),
            suggested_fix=f.get('suggested_fix', ''),
            severity=f.get('severity', 'WARNING'),
            status='PENDING'
        )
        db.session.add(flag)

    # Log action
    db.session.add(ReviewLog(
        submission_id=submission.id,
        actor_id=current_user.id,
        action='SCAN',
        comment=f"Pre-publication scan completed. Overall Health: {compliance_score}/100. Total flags: {len(all_flags)}."
    ))
    db.session.commit()

    return redirect(url_for('scanner.report', submission_id=submission.id))


@scanner_bp.route('/report/<int:submission_id>')
@login_required
def report(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    flags = EvaluationFlag.query.filter_by(submission_id=sub.id).all()
    
    # Calculate counts
    pending_flags = [f for f in flags if f.status == 'PENDING']
    accepted_flags = [f for f in flags if f.status == 'ACCEPTED']
    critical_count = sum(1 for f in flags if f.severity == 'CRITICAL' and f.status == 'PENDING')
    warning_count = sum(1 for f in flags if f.severity == 'WARNING' and f.status == 'PENDING')

    return render_template(
        'scanner/report.html',
        sub=sub,
        flags=flags,
        pending_flags=pending_flags,
        accepted_flags=accepted_flags,
        critical_count=critical_count,
        warning_count=warning_count
    )


@scanner_bp.route('/apply-fix/<int:flag_id>', methods=['POST'])
@login_required
def apply_fix(flag_id):
    """1-Click Tone-Preserving Fix Remediator."""
    flag = EvaluationFlag.query.get_or_404(flag_id)
    sub = flag.submission

    if flag.status == 'ACCEPTED':
        return jsonify({'success': False, 'message': 'Fix already applied.'})

    # Replace snippet in raw_content
    snippet = flag.flagged_snippet.replace('[Text inside Image] ', '')
    if snippet and flag.suggested_fix:
        # Regex or direct replacement
        sub.raw_content = sub.raw_content.replace(snippet, flag.suggested_fix)

    flag.status = 'ACCEPTED'
    
    # Boost score dynamically on acceptance!
    sub.compliance_score = min(100, sub.compliance_score + (15 if flag.severity == 'CRITICAL' else 8))
    if flag.flag_type == 'TONE':
        sub.tone_score = min(100, sub.tone_score + 12)
    elif flag.flag_type == 'CLAIM':
        sub.claim_score = min(100, sub.claim_score + 15)
    elif flag.flag_type in ['VISUAL', 'ACCESSIBILITY']:
        sub.visual_score = min(100, sub.visual_score + 15)

    db.session.add(ReviewLog(
        submission_id=sub.id,
        actor_id=current_user.id,
        action='FIX_ACCEPTED',
        comment=f"Applied 1-click suggested fix for '{flag.flagged_snippet}' -> '{flag.suggested_fix}'."
    ))
    db.session.commit()

    return jsonify({
        'success': True,
        'new_content': sub.raw_content,
        'new_score': sub.compliance_score,
        'flag_id': flag.id
    })


@scanner_bp.route('/dismiss-flag/<int:flag_id>', methods=['POST'])
@login_required
def dismiss_flag(flag_id):
    flag = EvaluationFlag.query.get_or_404(flag_id)
    reason = request.form.get('reason', 'Dismissed by author as intentional brand voice.')
    
    flag.status = 'DISMISSED'
    flag.override_reason = reason

    db.session.add(ReviewLog(
        submission_id=flag.submission_id,
        actor_id=current_user.id,
        action='FLAG_DISMISSED',
        comment=f"Dismissed flag '{flag.flagged_snippet}'. Reason: {reason}"
    ))
    db.session.commit()
    flash(f"Flag dismissed with note: {reason}", "info")
    return redirect(url_for('scanner.report', submission_id=flag.submission_id))


@scanner_bp.route('/submit-for-review/<int:submission_id>', methods=['POST'])
@login_required
def submit_for_review(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    sub.status = 'PENDING'
    
    db.session.add(ReviewLog(
        submission_id=sub.id,
        actor_id=current_user.id,
        action='SUBMIT',
        comment="Draft submitted to Stage-Gate Review Queue for Manager & Legal clearance."
    ))
    db.session.commit()
    flash("Submission routed to Stage-Gate Review Queue for manager approval!", "success")
    return redirect(url_for('reviews.queue'))


@scanner_bp.route('/ai-harmonize/<int:submission_id>', methods=['POST'])
@login_required
def ai_harmonize(submission_id):
    """Applies AI Deep Semantic Harmonization to the full submission draft."""
    sub = Submission.query.get_or_404(submission_id)
    if not sub.raw_content:
        flash("No textual content available to harmonize.", "warning")
        return redirect(url_for('scanner.report', submission_id=sub.id))

    res = ai_copilot.harmonize_draft(sub.raw_content)
    if res.get('success'):
        sub.raw_content = res.get('harmonized_text', sub.raw_content)
        # Mark pending tone/claim flags as accepted
        flags = EvaluationFlag.query.filter_by(submission_id=sub.id, status='PENDING').all()
        for f in flags:
            f.status = 'ACCEPTED'
        
        # Boost compliance scores
        sub.compliance_score = max(sub.compliance_score, 94)
        sub.tone_score = max(sub.tone_score, 95)
        sub.claim_score = max(sub.claim_score, 92)

        db.session.add(ReviewLog(
            submission_id=sub.id,
            actor_id=current_user.id,
            action='AI_HARMONIZED',
            comment=f"Applied AI Deep Harmonization ({res.get('engine_used', 'AI Engine')}). Shift: {res.get('tone_shift', 'Enterprise Consultative')}."
        ))
        db.session.commit()
        flash("AI Deep Harmonization applied! Clichés neutralized and score increased to " + str(sub.compliance_score) + "%.", "success")
    else:
        flash("AI Harmonization could not be completed.", "danger")

    return redirect(url_for('scanner.report', submission_id=sub.id))


@scanner_bp.route('/append-safe-harbor/<int:submission_id>', methods=['POST'])
@login_required
def append_safe_harbor(submission_id):
    """Appends an AI-generated FTC & SEC Safe Harbor Disclaimer to the submission."""
    sub = Submission.query.get_or_404(submission_id)
    res = ai_copilot.generate_safe_harbor(sub.raw_content or sub.title)
    if res.get('success'):
        disclaimer = res.get('disclaimer', '')
        sub.raw_content = f"{sub.raw_content.rstrip()}\n\n---\n**COMPLIANCE DISCLAIMER:**\n{disclaimer}"
        sub.claim_score = min(100, sub.claim_score + 10)
        sub.compliance_score = min(100, sub.compliance_score + 8)

        db.session.add(ReviewLog(
            submission_id=sub.id,
            actor_id=current_user.id,
            action='SAFE_HARBOR_APPENDED',
            comment="Appended AI-generated FTC Section 5 and SEC safe harbor regulatory disclaimers."
        ))
        db.session.commit()
        flash("FTC & SEC Safe Harbor Disclaimer successfully appended to draft!", "success")
    return redirect(url_for('scanner.report', submission_id=sub.id))


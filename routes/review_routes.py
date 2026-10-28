import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models import db, Submission, EvaluationFlag, ReviewLog, ReviewComment
from engines.pdf_cert import PDFCertificateGenerator

review_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@review_bp.route('/queue')
@login_required
def queue():
    if current_user.role not in ['REVIEWER', 'MANAGER', 'ADMIN']:
        flash("Access Denied: The Stage-Gate Review Queue is restricted to authorized Reviewers & Legal Counsel.", "warning")
        return redirect(url_for('portal.client_portal'))

    # Filter submissions
    pending = Submission.query.filter_by(status='PENDING').order_by(Submission.created_at.desc()).all()
    approved = Submission.query.filter_by(status='APPROVED').order_by(Submission.created_at.desc()).limit(10).all()
    in_revision = Submission.query.filter(Submission.status.in_(['CHANGES_REQUESTED', 'SCANNED'])).order_by(Submission.created_at.desc()).limit(10).all()

    return render_template(
        'reviews/queue.html',
        pending=pending,
        approved=approved,
        in_revision=in_revision
    )


@review_bp.route('/detail/<int:submission_id>')
@login_required
def detail(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    flags = EvaluationFlag.query.filter_by(submission_id=sub.id).all()
    logs = ReviewLog.query.filter_by(submission_id=sub.id).order_by(ReviewLog.timestamp.desc()).all()
    comments = ReviewComment.query.filter_by(submission_id=sub.id).order_by(ReviewComment.created_at.asc()).all()

    return render_template(
        'reviews/detail.html',
        sub=sub,
        flags=flags,
        logs=logs,
        comments=comments
    )


@review_bp.route('/action/<int:submission_id>', methods=['POST'])
@login_required
def take_action(submission_id):
    if current_user.role not in ['MANAGER', 'REVIEWER', 'ADMIN']:
        flash("Only authorized Managers, Reviewers, or Admins can issue stage-gate decisions.", "danger")
        return redirect(url_for('reviews.detail', submission_id=submission_id))

    sub = Submission.query.get_or_404(submission_id)
    action = request.form.get('action')  # APPROVE, REQUEST_CHANGES, REJECT
    comment = request.form.get('comment', '').strip()

    if action == 'APPROVE':
        sub.status = 'APPROVED'
        sub.reviewer_id = current_user.id
        db.session.add(ReviewLog(
            submission_id=sub.id,
            actor_id=current_user.id,
            action='APPROVED',
            comment=comment or "Submission approved and certified for publication."
        ))

        # Generate Official PDF Certificate
        output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'certificates')
        cert_filename = PDFCertificateGenerator.generate_certificate(sub, output_dir)
        flash(f"Submission #{sub.id} APPROVED! Compliance Certificate generated: {cert_filename}", "success")

    elif action == 'REQUEST_CHANGES':
        sub.status = 'CHANGES_REQUESTED'
        db.session.add(ReviewLog(
            submission_id=sub.id,
            actor_id=current_user.id,
            action='CHANGES_REQUESTED',
            comment=comment or "Changes requested by reviewer."
        ))
        if comment:
            db.session.add(ReviewComment(submission_id=sub.id, user_id=current_user.id, message=f"[Changes Requested] {comment}"))
        flash(f"Changes requested on submission #{sub.id}.", "warning")

    elif action == 'REJECT':
        sub.status = 'REJECTED'
        db.session.add(ReviewLog(
            submission_id=sub.id,
            actor_id=current_user.id,
            action='REJECTED',
            comment=comment or "Submission rejected."
        ))
        flash(f"Submission #{sub.id} REJECTED.", "danger")

    db.session.commit()
    return redirect(url_for('reviews.detail', submission_id=sub.id))


@review_bp.route('/comment/<int:submission_id>', methods=['POST'])
@login_required
def post_comment(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    message = request.form.get('message', '').strip()
    if message:
        comment = ReviewComment(submission_id=sub.id, user_id=current_user.id, message=message)
        db.session.add(comment)
        db.session.commit()
        flash("Comment posted.", "info")
    return redirect(url_for('reviews.detail', submission_id=sub.id))


@review_bp.route('/certificate/<int:submission_id>')
@login_required
def download_certificate(submission_id):
    sub = Submission.query.get_or_404(submission_id)
    output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'certificates')
    
    # Generate on the fly if needed
    cert_filename = PDFCertificateGenerator.generate_certificate(sub, output_dir)
    return send_from_directory(output_dir, cert_filename, as_attachment=True)

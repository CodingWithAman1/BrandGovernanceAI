from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Submission, BrandGuideline, ApprovedFact, EvaluationFlag, ReviewLog, db
from sqlalchemy import func

portal_bp = Blueprint('portal', __name__, url_prefix='')

# ==================== CLIENT / CREATOR PORTAL DASHBOARD ====================

@portal_bp.route('/client')
@portal_bp.route('/client/dashboard')
@portal_bp.route('/portal/client')
@login_required
def client_portal():
    # Content specific to this client/creator
    my_submissions = Submission.query.filter_by(creator_id=current_user.id).order_by(Submission.created_at.desc()).all()
    
    total_my_scans = len(my_submissions)
    pending_count = sum(1 for s in my_submissions if s.status == 'PENDING')
    changes_req_count = sum(1 for s in my_submissions if s.status == 'CHANGES_REQUESTED')
    approved_count = sum(1 for s in my_submissions if s.status == 'APPROVED')
    
    avg_score = (
        round(sum(s.compliance_score for s in my_submissions) / total_my_scans, 1)
        if total_my_scans > 0 else 100
    )

    # Active brand guidelines for client quick reference
    active_guidelines = BrandGuideline.query.filter_by(is_active=True).order_by(BrandGuideline.category).limit(6).all()

    return render_template(
        'portals/client_portal.html',
        my_submissions=my_submissions,
        total_my_scans=total_my_scans,
        pending_count=pending_count,
        changes_req_count=changes_req_count,
        approved_count=approved_count,
        avg_score=avg_score,
        active_guidelines=active_guidelines
    )


# ==================== REVIEWER / MANAGER PORTAL DASHBOARD ====================

@portal_bp.route('/reviewer')
@portal_bp.route('/reviewer/dashboard')
@portal_bp.route('/portal/reviewer')
@login_required
def reviewer_portal():
    # RBAC: Only Reviewers, Managers, and Admins can access the Reviewer Desk
    if current_user.role not in ['REVIEWER', 'MANAGER', 'ADMIN']:
        flash("Access Denied: You are signed in as a Client. The Reviewer Desk is restricted to authorized Reviewers & Legal Counsel.", "warning")
        return redirect(url_for('portal.client_portal'))

    # Reviewers inspect all incoming client submissions
    pending_queue = Submission.query.filter_by(status='PENDING').order_by(Submission.created_at.desc()).all()
    approved_list = Submission.query.filter_by(status='APPROVED').order_by(Submission.updated_at.desc()).limit(10).all()
    in_revision = Submission.query.filter_by(status='CHANGES_REQUESTED').order_by(Submission.updated_at.desc()).limit(10).all()

    total_pending = len(pending_queue)
    total_certified = Submission.query.filter_by(status='APPROVED').count()

    return render_template(
        'portals/reviewer_portal.html',
        pending_queue=pending_queue,
        approved_list=approved_list,
        in_revision=in_revision,
        total_pending=total_pending,
        total_certified=total_certified
    )


# ==================== EXECUTIVE ADMIN PORTAL (RESTRICTED TO AMAN SHARMA) ====================

@portal_bp.route('/admin')
@portal_bp.route('/admin/dashboard')
@portal_bp.route('/portal/admin')
@login_required
def admin_portal():
    # STRICT SECURITY CHECK: Only Aman Sharma is the Admin
    if not current_user.is_admin:
        flash("Access Denied: The Executive Admin Portal is strictly restricted to Aman Sharma (Sole Administrator).", "danger")
        if current_user.role in ['REVIEWER', 'MANAGER']:
            return redirect(url_for('portal.reviewer_portal'))
        else:
            return redirect(url_for('portal.client_portal'))

    # Admin oversees everything across the system
    all_users = User.query.order_by(User.role, User.name).all()
    total_clients = User.query.filter_by(role='CREATOR').count()
    total_reviewers = User.query.filter(User.role.in_(['REVIEWER', 'MANAGER'])).count()
    total_guidelines = BrandGuideline.query.count()
    total_facts = ApprovedFact.query.count()
    total_submissions = Submission.query.count()

    system_logs = ReviewLog.query.order_by(ReviewLog.timestamp.desc()).limit(12).all()

    return render_template(
        'portals/admin_portal.html',
        all_users=all_users,
        total_clients=total_clients,
        total_reviewers=total_reviewers,
        total_guidelines=total_guidelines,
        total_facts=total_facts,
        total_submissions=total_submissions,
        system_logs=system_logs
    )


@portal_bp.route('/admin/toggle-user/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized action: Only the Sole Administrator can alter account states.", "danger")
        return redirect(url_for('portal.client_portal'))

    target_user = User.query.get_or_404(user_id)
    if target_user.is_admin:
        flash("Cannot deactivate the sole administrator account.", "warning")
        return redirect(url_for('portal.admin_portal'))

    target_user.is_active_account = not target_user.is_active_account
    db.session.commit()
    status_str = "activated" if target_user.is_active_account else "deactivated"
    flash(f"User {target_user.name} ({target_user.email}) has been {status_str}.", "info")
    return redirect(url_for('portal.admin_portal'))

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Submission, BrandGuideline, ApprovedFact, EvaluationFlag, ReviewLog, db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@dashboard_bp.route('')
@login_required
def index():
    """Intelligent role-aware router: sends user straight to their dedicated portal dashboard."""
    if current_user.is_admin:
        return redirect(url_for('portal.admin_portal'))
    elif current_user.role in ['REVIEWER', 'MANAGER']:
        return redirect(url_for('portal.reviewer_portal'))
    else:
        return redirect(url_for('portal.client_portal'))


@dashboard_bp.route('/overview')
@login_required
def global_overview():
    """System-wide operational telemetry view."""
    total_audits = Submission.query.count()
    pending_reviews = Submission.query.filter_by(status='PENDING').count()
    approved_count = Submission.query.filter_by(status='APPROVED').count()
    
    avg_score = db.session.query(func.avg(Submission.compliance_score)).scalar() or 0
    avg_score = round(avg_score, 1)

    recent_submissions = Submission.query.order_by(Submission.created_at.desc()).limit(6).all()
    recent_logs = ReviewLog.query.order_by(ReviewLog.timestamp.desc()).limit(8).all()
    
    # Category flag counts
    flag_counts = db.session.query(
        EvaluationFlag.flag_type,
        func.count(EvaluationFlag.id)
    ).group_by(EvaluationFlag.flag_type).all()
    flag_dict = {f[0]: f[1] for f in flag_counts}

    total_rules = BrandGuideline.query.filter_by(is_active=True).count()
    total_facts = ApprovedFact.query.filter_by(is_active=True).count()

    return render_template(
        'dashboard/index.html',
        total_audits=total_audits,
        pending_reviews=pending_reviews,
        approved_count=approved_count,
        avg_score=avg_score,
        recent_submissions=recent_submissions,
        recent_logs=recent_logs,
        flag_dict=flag_dict,
        total_rules=total_rules,
        total_facts=total_facts
    )

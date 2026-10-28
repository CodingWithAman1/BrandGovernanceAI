from flask import Blueprint, render_template
from flask_login import login_required
from engines.clarity_engine import ClarityEngine
from models import EvaluationFlag, Submission, db
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
@login_required
def index():
    clarity_insights = ClarityEngine.get_clarity_insights()
    
    # Category totals
    category_totals = db.session.query(
        EvaluationFlag.flag_type,
        func.count(EvaluationFlag.id)
    ).group_by(EvaluationFlag.flag_type).all()

    # Status breakdown
    status_counts = db.session.query(
        Submission.status,
        func.count(Submission.id)
    ).group_by(Submission.status).all()

    return render_template(
        'analytics/index.html',
        clarity_insights=clarity_insights,
        category_totals=category_totals,
        status_counts=status_counts
    )

from models import EvaluationFlag, BrandGuideline, db
from sqlalchemy import func

class ClarityEngine:
    """
    Engine 4: Guideline Clarity Index
    Analyzes dispute rates, recurring infractions, and overrides to surface
    ambiguous or contested brand guidelines for executive leadership.
    """

    @staticmethod
    def get_clarity_insights():
        """Computes friction stats and clarity index per guideline category."""
        # Query total flags grouped by guideline
        flag_stats = db.session.query(
            EvaluationFlag.guideline_id,
            func.count(EvaluationFlag.id).label('total_flags'),
            func.sum(db.case((EvaluationFlag.status == 'DISMISSED', 1), else_=0)).label('dismissed_count'),
            func.sum(db.case((EvaluationFlag.status == 'OVERRIDDEN', 1), else_=0)).label('overridden_count'),
            func.sum(db.case((EvaluationFlag.status == 'ACCEPTED', 1), else_=0)).label('accepted_count')
        ).group_by(EvaluationFlag.guideline_id).all()

        insights = []
        for g_id, total, dismissed, overridden, accepted in flag_stats:
            guideline = BrandGuideline.query.get(g_id) if g_id else None
            title = guideline.rule_title if guideline else "General Engine Rule"
            code = guideline.rule_code if guideline else "GEN-01"
            category = guideline.category if guideline else "SYSTEM"
            
            # Friction score: high dismissals/overrides mean creators find the rule ambiguous or unreasonable
            dispute_count = (dismissed or 0) + (overridden or 0)
            friction_pct = round((dispute_count / total * 100), 1) if total > 0 else 0
            
            # Clarity score: 100 minus friction percentage
            clarity_score = max(10, int(100 - friction_pct))

            status_recommendation = (
                "Review & Clarify Rule" if friction_pct > 40
                else "High Compliance" if friction_pct < 15
                else "Moderate Adherence"
            )

            insights.append({
                'rule_code': code,
                'title': title,
                'category': category,
                'total_flags': total,
                'accepted': accepted or 0,
                'disputed': dispute_count,
                'friction_pct': friction_pct,
                'clarity_score': clarity_score,
                'recommendation': status_recommendation
            })

        insights.sort(key=lambda x: x['friction_pct'], reverse=True)
        return insights

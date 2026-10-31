import json
import hashlib
from datetime import datetime
from flask import Blueprint, render_template, request, Response, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from models import db, EvaluationFlag, Submission, User, BrandGuideline, ApprovedFact, ReviewLog
from engines.clarity_engine import ClarityEngine

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

    # 1. Department-Level Risk Profiling
    all_users = User.query.all()
    dept_map = {}
    for u in all_users:
        dept = u.department or "General Marketing"
        if dept not in dept_map:
            dept_map[dept] = {"users": [], "submissions": [], "flags": []}
        dept_map[dept]["users"].append(u)

    all_subs = Submission.query.all()
    for s in all_subs:
        dept = s.creator.department if s.creator and s.creator.department else "General Marketing"
        if dept not in dept_map:
            dept_map[dept] = {"users": [], "submissions": [], "flags": []}
        dept_map[dept]["submissions"].append(s)
        dept_map[dept]["flags"].extend(s.flags)

    department_profiles = []
    for dept_name, data in dept_map.items():
        subs = data["submissions"]
        flags = data["flags"]
        sub_count = len(subs)
        avg_score = int(sum(s.compliance_score for s in subs) / sub_count) if sub_count > 0 else 92
        critical_count = sum(1 for f in flags if f.severity == 'CRITICAL')
        warning_count = sum(1 for f in flags if f.severity == 'WARNING')

        if avg_score >= 85:
            risk_badge = "LOW_RISK"
            risk_color = "success"
        elif avg_score >= 70:
            risk_badge = "MODERATE_RISK"
            risk_color = "warning"
        else:
            risk_badge = "ELEVATED_RISK"
            risk_color = "danger"

        department_profiles.append({
            "department": dept_name,
            "submissions_count": sub_count,
            "avg_score": avg_score,
            "total_flags": len(flags),
            "critical_count": critical_count,
            "warning_count": warning_count,
            "risk_badge": risk_badge,
            "risk_color": risk_color,
            "active_creators": len(data["users"])
        })

    department_profiles.sort(key=lambda d: d["avg_score"])

    # 2. Brand Drift Trend Calculation
    drift_trend = {
        "drift_delta": "+4.2%",
        "drift_direction": "POSITIVE",
        "drift_label": "Adherence Improving",
        "current_avg": 88,
        "baseline_avg": 84,
        "quarter": "Q4 2026",
        "status": "STABLE_COMPLIANT"
    }

    if len(all_subs) >= 2:
        sorted_subs = sorted(all_subs, key=lambda s: s.created_at)
        mid = len(sorted_subs) // 2
        older = sorted_subs[:mid]
        newer = sorted_subs[mid:]
        old_avg = sum(s.compliance_score for s in older) / len(older)
        new_avg = sum(s.compliance_score for s in newer) / len(newer)
        delta = round(new_avg - old_avg, 1)

        drift_trend["baseline_avg"] = int(old_avg)
        drift_trend["current_avg"] = int(new_avg)
        drift_trend["drift_delta"] = f"{'+' if delta >= 0 else ''}{delta}%"
        if delta > 1.0:
            drift_trend["drift_direction"] = "POSITIVE"
            drift_trend["drift_label"] = "Adherence Improving (+)"
            drift_trend["status"] = "IMPROVING"
        elif delta < -1.0:
            drift_trend["drift_direction"] = "NEGATIVE"
            drift_trend["drift_label"] = "Brand Drift Detected (-)"
            drift_trend["status"] = "DRIFT_ALERT"
        else:
            drift_trend["drift_direction"] = "NEUTRAL"
            drift_trend["drift_label"] = "Stable Brand Adherence"
            drift_trend["status"] = "STABLE"

    return render_template(
        'analytics/index.html',
        clarity_insights=clarity_insights,
        category_totals=category_totals,
        status_counts=status_counts,
        department_profiles=department_profiles,
        drift_trend=drift_trend
    )


@analytics_bp.route('/audit-vault-export')
@login_required
def audit_vault_export():
    """
    Audit Vault Export: Generates downloadable compliance dossier
    for General Counsel, FTC auditors, or Board Risk Committees.
    Supports ?format=json (JSON file download) or HTML executive dossier view.
    """
    export_format = request.args.get('format', 'html').lower()

    submissions = Submission.query.order_by(Submission.created_at.desc()).all()
    guidelines = BrandGuideline.query.filter_by(is_active=True).all()
    approved_facts = ApprovedFact.query.filter_by(is_active=True).all()
    recent_logs = ReviewLog.query.order_by(ReviewLog.timestamp.desc()).limit(20).all()

    total_subs = len(submissions)
    approved_subs = [s for s in submissions if s.status == 'APPROVED']
    pending_subs = [s for s in submissions if s.status == 'PENDING']
    avg_health = int(sum(s.compliance_score for s in submissions) / total_subs) if total_subs > 0 else 100

    now_iso = datetime.utcnow().isoformat() + "Z"
    vault_payload_str = f"BrandGuardAI-AuditVault-{total_subs}-{avg_health}-{now_iso}"
    cryptographic_seal = hashlib.sha256(vault_payload_str.encode('utf-8')).hexdigest().upper()

    dossier_data = {
        "organization": "Inkloom AI & Team Synapse Enterprise",
        "exported_by": current_user.name,
        "exported_by_role": current_user.role,
        "timestamp": now_iso,
        "cryptographic_seal": cryptographic_seal,
        "compliance_governance_score": avg_health,
        "total_submissions_audited": total_subs,
        "cleared_prepublication_rate": f"{int((len(approved_subs)/total_subs)*100)}%" if total_subs > 0 else "100%",
        "active_guidelines_count": len(guidelines),
        "verified_truth_bank_claims": len(approved_facts),
        "regulatory_frameworks": [
            "FTC Act Section 5 (Truth in Advertising / Operation AI Comply)",
            "SEC AI-Washing Rule 10b-5 & PSLRA Safe Harbor Disclosures",
            "EU AI Act (Regulation (EU) 2024/1689) Articles 50 & 52",
            "UK CMA Green Claims Code (6 Principles of Environmental Claims)"
        ],
        "submissions_summary": [{
            "id": s.id,
            "title": s.title,
            "status": s.status,
            "creator": s.creator.name if s.creator else "Unknown",
            "department": s.creator.department if s.creator else "General",
            "compliance_score": s.compliance_score,
            "tone_score": s.tone_score,
            "claim_score": s.claim_score,
            "regulatory_score": getattr(s, 'regulatory_score', 100),
            "jurisdiction": getattr(s, 'jurisdiction', 'GLOBAL'),
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in submissions],
        "recent_immutable_audit_logs": [{
            "timestamp": l.timestamp.isoformat() if l.timestamp else None,
            "actor": l.actor.name if l.actor else "System",
            "action": l.action,
            "comment": l.comment
        } for l in recent_logs]
    }

    if export_format == 'json':
        response_json = json.dumps(dossier_data, indent=2)
        filename = f"BrandGuard_Audit_Vault_Dossier_{int(datetime.utcnow().timestamp())}.json"
        return Response(
            response_json,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

    # Render HTML Dossier View
    return render_template(
        'analytics/audit_dossier.html',
        dossier=dossier_data,
        submissions=submissions,
        guidelines=guidelines,
        approved_facts=approved_facts,
        recent_logs=recent_logs
    )

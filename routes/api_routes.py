from flask import Blueprint, request, jsonify
from models import BrandGuideline, ApprovedFact
from engines.tone_calibrator import ToneCalibrator
from engines.claims_checker import ClaimsFactChecker

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

import re

class ToneCalibrator:
    """
    Engine 1: Tone & Voice Calibrator
    Evaluates copy against 5 brand polarities and catches robotic AI jargon,
    aggressive/passive-aggressive phrasing, and forbidden terms.
    """

    ROBOTIC_AI_PHRASES = [
        (r"\bdelve(?:s|d|ing)? into\b", "explore", "Avoid clichéd AI filler 'delve into'; use direct, active verbs."),
        (r"\ba testament to\b", "evidence of", "Avoid robotic phrase 'a testament to'; state the specific evidence."),
        (r"\brich tapestry\b", "diverse range", "Avoid clichéd metaphor 'rich tapestry'; be concrete."),
        (r"\bin today'?s fast-?paced (?:world|digital landscape)\b", "currently", "Cut bloated intro cliches; start directly with the value proposition."),
        (r"\bgame-?changer\b", "significant milestone", "Avoid overused marketing buzzwords; use specific outcomes."),
        (r"\bunpack\b", "explain", "Replace conversational jargon with professional clarity."),
        # 10 additional robotic AI / corporate buzzword phrases
        (r"\beverag(?:e|es|ed|ing)\b", "use", "Replace vague corporate verb 'leverage' with direct alternatives like 'use' or 'apply'."),
        (r"\bsynergy\b", "combined effect", "Avoid hollow corporate buzzword 'synergy'; describe the specific benefit."),
        (r"\bpivot\b", "shift", "Replace overused startup jargon 'pivot' with concrete directional language."),
        (r"\bscalable solution\b", "solution built for scale", "Avoid vague 'scalable solution'; describe how and why it scales."),
        (r"\bmove the needle\b", "make measurable progress", "Replace sports metaphor 'move the needle' with specific outcome language."),
        (r"\bcircle back\b", "follow up", "Replace informal 'circle back' with professional 'follow up'."),
        (r"\bbandwidth\b", "capacity", "Replace technical metaphor 'bandwidth' with clearer 'capacity' or 'availability'."),
        (r"\bat the end of the day\b", "ultimately", "Remove clichéd filler phrase 'at the end of the day'; say 'ultimately'."),
        (r"\bparadigm shift\b", "fundamental change", "Replace overused buzzword 'paradigm shift' with concrete description."),
        (r"\bthought leader\b", "industry expert", "Avoid self-congratulatory 'thought leader'; use substantiated 'industry expert' or 'recognized authority'.")
    ]

    AGGRESSIVE_HYPERBOLIC_PHRASES = [
        (r"\bcrush(?:es|ed|ing)? the competition\b", "leads industry benchmarks", "Aggressive tone violates professional brand voice standard."),
        (r"\bobviously\b", "", "Passive-aggressive filler that can condescend to enterprise readers."),
        (r"\bneedless to say\b", "", "Redundant filler; state the point directly."),
        (r"\bclearly you (?:must|should)\b", "we recommend", "Accusatory tone; replace with empathetic consultative phrasing.")
    ]

    def __init__(self, guidelines=None):
        self.guidelines = guidelines or []

    def evaluate(self, text):
        flags = []
        lower_text = text.lower()

        # 1. Robotic AI Jargon checks
        for pattern, replacement, reason in self.ROBOTIC_AI_PHRASES:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for m in matches:
                snippet = m.group(0)
                suggested = re.sub(pattern, replacement, text[max(0, m.start()-20):min(len(text), m.end()+20)], flags=re.IGNORECASE)
                flags.append({
                    'flag_type': 'TONE',
                    'snippet': snippet,
                    'severity': 'SUGGESTION',
                    'explanation': f"Robotic AI Phrasing: {reason}",
                    'suggested_fix': replacement,
                    'rule_code': 'BG-TONE-01',
                    'citation': 'Brand Voice Guide § 2.1 (Clarity & Authenticity)'
                })

        # 2. Aggressive / Flippant Phrasing
        for pattern, replacement, reason in self.AGGRESSIVE_HYPERBOLIC_PHRASES:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for m in matches:
                snippet = m.group(0)
                flags.append({
                    'flag_type': 'TONE',
                    'snippet': snippet,
                    'severity': 'WARNING',
                    'explanation': f"Tone Polarity Violation: {reason}",
                    'suggested_fix': replacement,
                    'rule_code': 'BG-TONE-02',
                    'citation': 'Brand Voice Guide § 2.4 (Empathetic & Consultative Voice)'
                })

        # 3. Dynamic Guidelines matching (from Database)
        for g in self.guidelines:
            if g.category in ['TONE', 'TERMINOLOGY'] and g.forbidden_patterns:
                patterns = [p.strip() for p in re.split(r'[,;\n]', g.forbidden_patterns) if p.strip()]
                for pat in patterns:
                    escaped_pat = r'\b' + re.escape(pat) + r'\b'
                    matches = list(re.finditer(escaped_pat, text, re.IGNORECASE))
                    for m in matches:
                        snippet = m.group(0)
                        fix = g.recommended_replacement or ""
                        flags.append({
                            'flag_type': g.category,
                            'snippet': snippet,
                            'severity': g.severity or 'WARNING',
                            'explanation': f"Rule '{g.rule_title}': {g.rule_description}",
                            'suggested_fix': fix,
                            'rule_code': g.rule_code,
                            'citation': g.citation_ref or f"Brand Guideline {g.rule_code}"
                        })

        # Compute tone score (starts at 100, drops per violation)
        deductions = sum(15 if f['severity'] == 'CRITICAL' else 10 if f['severity'] == 'WARNING' else 5 for f in flags)
        score = max(20, 100 - deductions)

        return {
            'score': score,
            'flags': flags
        }

    def generate_tone_report(self, text):
        """
        Generates a high-level summary of tone profile, dominant issues, and recommendations.
        Returns a dict with keys: dominant_issues, tone_profile, recommendations.
        """
        result = self.evaluate(text)
        flags = result['flags']
        score = result['score']

        # Tally issues by type
        jargon_count = sum(1 for f in flags if 'BG-TONE-01' in f.get('rule_code', ''))
        aggressive_count = sum(1 for f in flags if 'BG-TONE-02' in f.get('rule_code', ''))
        guideline_count = len(flags) - jargon_count - aggressive_count

        # Dominant issues
        dominant_issues = []
        if jargon_count > 0:
            dominant_issues.append(f"{jargon_count} robotic AI jargon phrase(s) detected")
        if aggressive_count > 0:
            dominant_issues.append(f"{aggressive_count} aggressive or passive-aggressive phrasing instance(s)")
        if guideline_count > 0:
            dominant_issues.append(f"{guideline_count} custom guideline violation(s)")
        if not dominant_issues:
            dominant_issues.append("No significant tone violations detected")

        # Tone profile
        if score >= 90:
            tone_profile = "ENTERPRISE_CONSULTATIVE — Authoritative, clear, and audience-empathetic"
        elif score >= 70:
            tone_profile = "MIXED — Mostly professional with isolated jargon or assertive phrasing"
        elif score >= 50:
            tone_profile = "NEEDS_WORK — Multiple tone violations reducing brand credibility"
        else:
            tone_profile = "NON_COMPLIANT — Significant tone issues require full review before publication"

        # Recommendations
        recommendations = []
        if jargon_count > 0:
            recommendations.append(
                "Replace AI-generated filler phrases (e.g., 'leverage', 'synergy') with direct, specific language."
            )
        if aggressive_count > 0:
            recommendations.append(
                "Reframe combative or condescending phrasing using empathetic, consultative voice."
            )
        if score < 85:
            recommendations.append(
                "Click 'AI Deep Harmonize' to automatically remediate all detected tone issues in one step."
            )
        if not recommendations:
            recommendations.append(
                "Tone is strong. Confirm all numeric claims have supporting citations before publication."
            )

        return {
            "dominant_issues": dominant_issues,
            "tone_profile": tone_profile,
            "recommendations": recommendations,
            "score": score,
            "total_flags": len(flags)
        }

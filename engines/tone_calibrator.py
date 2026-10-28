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
        (r"\bunpack\b", "explain", "Replace conversational jargon with professional clarity.")
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

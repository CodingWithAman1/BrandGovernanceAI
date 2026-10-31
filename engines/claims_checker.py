import re
from datetime import datetime

class ClaimsFactChecker:
    """
    Engine 2: Truth & Claims Fact-Checker
    Cross-references claims against the SQL Approved Facts bank and flags
    unverified superlatives, absolute guarantees, and FTC Section 5 risks.
    """

    UNVERIFIED_SUPERLATIVES = [
        (r"\b#1\b|(?:\bnumber\s+one\b)", "leading", "Unsubstantiated '#1' claim requires independent third-party market audit per FTC guidelines."),
        (r"\bworld'?s\s+(?:best|fastest|greatest|most\s+advanced)\b", "an industry-leading", "Absolute superlative lacks evidentiary proof."),
        (r"\b100%\s+(?:guaranteed|foolproof|risk-?\s*free)\b", "reliable and proven", "Absolute guarantees violate regulatory standards; enterprise software has inherent operational variables."),
        (r"\bunbeatable\b|\bunrivaled\b", "competitive", "Unprovable superlative claim."),
        (r"\bnever\s+fails\b", "consistently delivers", "Absolute claim; replace with measurable uptime or performance SLA."),
        (r"\bmiraculous\b|\bmagic\b", "innovative", "Pseudoscientific hyperbole; use professional engineering descriptions."),
        # 5 additional high-risk claim patterns
        (r"\bzero\s+downtime\b", "high availability", "Absolute uptime claim; no production system guarantees zero downtime. Use SLA-backed language."),
        (r"\binstant\s+results\b", "rapid, measurable results", "Absolute speed claim; performance varies by deployment. Use qualified language."),
        (r"\beffortless\b", "streamlined", "Subjective ease claim may mislead buyers about implementation complexity."),
        (r"\brevolutionary\b", "significantly advanced", "Unsubstantiated superlative; describe the specific innovation instead."),
        (r"\bfirst\s+ever\b", "among the first", "Absolute novelty claim that requires documented historical verification.")
    ]

    def __init__(self, approved_facts=None, guidelines=None):
        self.approved_facts = approved_facts or []
        self.guidelines = guidelines or []

    def evaluate(self, text):
        flags = []
        today_str = datetime.utcnow().strftime("%Y-%m-%d")

        # 1. Unverified Superlative & FTC Section 5 checks
        for pattern, replacement, reason in self.UNVERIFIED_SUPERLATIVES:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            for m in matches:
                snippet = m.group(0)
                flags.append({
                    'flag_type': 'CLAIM',
                    'snippet': snippet,
                    'severity': 'CRITICAL',
                    'explanation': f"FTC Section 5 Risk: {reason}",
                    'suggested_fix': replacement,
                    'rule_code': 'BG-CLAIM-01',
                    'citation': 'FTC Act Section 5 / Operation AI Comply Evidentiary Standard'
                })

        # 2. Database Claim Guidelines
        for g in self.guidelines:
            if g.category == 'CLAIM' and g.forbidden_patterns:
                patterns = [p.strip() for p in re.split(r'[,;\n]', g.forbidden_patterns) if p.strip()]
                for pat in patterns:
                    escaped_pat = r'\b' + re.escape(pat) + r'\b'
                    matches = list(re.finditer(escaped_pat, text, re.IGNORECASE))
                    for m in matches:
                        snippet = m.group(0)
                        flags.append({
                            'flag_type': 'CLAIM',
                            'snippet': snippet,
                            'severity': g.severity or 'CRITICAL',
                            'explanation': f"Claim Rule '{g.rule_title}': {g.rule_description}",
                            'suggested_fix': g.recommended_replacement or "verified metric with citation",
                            'rule_code': g.rule_code,
                            'citation': g.citation_ref or f"Compliance Rule {g.rule_code}"
                        })

        # 3. Check for expired facts in text
        # If text mentions numbers or claims from an expired fact
        for fact in self.approved_facts:
            if fact.expiration_date and fact.expiration_date < today_str:
                # If statement or topic keywords appear in text
                words = [w for w in fact.topic.split() if len(w) > 3]
                if any(w.lower() in text.lower() for w in words):
                    flags.append({
                        'flag_type': 'CLAIM',
                        'snippet': fact.topic,
                        'severity': 'WARNING',
                        'explanation': f"Expired Fact Notice: Approved fact statement '{fact.claim_statement}' expired on {fact.expiration_date}. Please update to current quarterly benchmarks.",
                        'suggested_fix': "Request refreshed audit metrics from Compliance",
                        'rule_code': 'BG-FACT-EXP',
                        'citation': f"Approved Fact #{fact.id} ({fact.approved_source_link or 'Internal Vault'})"
                    })

        deductions = sum(20 if f['severity'] == 'CRITICAL' else 10 if f['severity'] == 'WARNING' else 5 for f in flags)
        score = max(10, 100 - deductions)

        return {
            'score': score,
            'flags': flags
        }

    def generate_risk_summary(self, text):
        """
        Generates a high-level risk summary of claim violations.
        Returns a dict with keys: risk_level, top_violations, ftc_exposure.
        """
        result = self.evaluate(text)
        flags = result['flags']
        score = result['score']

        # Risk level classification
        critical_count = sum(1 for f in flags if f['severity'] == 'CRITICAL')
        warning_count = sum(1 for f in flags if f['severity'] == 'WARNING')

        if critical_count >= 3:
            risk_level = "HIGH"
        elif critical_count >= 1 or warning_count >= 3:
            risk_level = "MEDIUM"
        elif warning_count >= 1:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"

        # Top violations (up to 5, sorted by severity)
        severity_order = {"CRITICAL": 0, "WARNING": 1, "SUGGESTION": 2}
        sorted_flags = sorted(flags, key=lambda f: severity_order.get(f['severity'], 3))
        top_violations = [
            {
                "snippet": f['snippet'],
                "severity": f['severity'],
                "explanation": f['explanation'][:120],
                "suggested_fix": f['suggested_fix']
            }
            for f in sorted_flags[:5]
        ]

        # FTC exposure assessment
        if critical_count == 0:
            ftc_exposure = "LOW — No absolute or unsubstantiated claim patterns detected."
        elif critical_count == 1:
            ftc_exposure = (
                f"MODERATE — 1 FTC Section 5 risk pattern detected. Resolve before publication "
                "to avoid potential enforcement scrutiny."
            )
        else:
            ftc_exposure = (
                f"HIGH — {critical_count} FTC Section 5 risk patterns detected. "
                "This content requires compliance review before any external use. "
                "Unresolved claims may attract FTC inquiry under Operation AI Comply guidelines."
            )

        return {
            "risk_level": risk_level,
            "top_violations": top_violations,
            "ftc_exposure": ftc_exposure,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "score": score
        }

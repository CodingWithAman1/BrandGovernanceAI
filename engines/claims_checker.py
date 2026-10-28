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
        (r"\bmiraculous\b|\bmagic\b", "innovative", "Pseudoscientific hyperbole; use professional engineering descriptions.")
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

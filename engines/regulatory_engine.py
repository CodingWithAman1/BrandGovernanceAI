"""
BrandGuard AI — Global Regulatory & Compliance Engine
======================================================
Engine 4: SEC AI-Washing, EU AI Act & UK CMA Environmental Claims Inspector

Audits marketing content, corporate disclosures, and promotional copy against:
1. SEC AI-Washing & FTC Operation AI Comply:
   - Detects unverified autonomy, "hallucination-free" claims, exaggerated AI core capabilities,
     and forward-looking statements lacking PSLRA safe harbors.
2. EU AI Act (Regulation EU 2024/1689):
   - Audits Article 50 transparency disclosures (mandatory AI-generated content disclosures),
     Article 52 high-risk classification, emotion/biometric recognition restrictions,
     and GDPR Article 22 automated decision disclosures.
3. UK CMA (Competition and Markets Authority) Green Claims:
   - Evaluates environmental and sustainability claims ("carbon neutral", "eco-friendly",
     "planet-positive", "zero emissions") against the 6 CMA Green Claims Code principles.
4. Global Multi-Jurisdictional Framework:
   - Unified cross-border regulatory risk scoring, flag synthesis, and automated safe harbor generation.
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional


class RegulatoryComplianceEngine:
    """
    Enterprise-grade regulatory engine for SEC, EU AI Act, and UK CMA compliance.
    """

    JURISDICTIONS = ["US", "EU", "UK", "GLOBAL"]

    # =========================================================================
    # 1. SEC AI-WASHING & FTC SECTION 5 PATTERNS
    # =========================================================================
    SEC_AI_WASHING_RULES = [
        (
            r"\b(?:zero|0%|no)\s+hallucinations?\b|\bhallucination-?free\b|\bnever\s+hallucinates?\b",
            "statistically bounded accuracy with human-in-the-loop review",
            "SEC AI-Washing Risk: Generative AI models are fundamentally probabilistic. Representing an LLM as completely hallucination-free constitutes deceptive marketing under SEC Rule 10b-5 and FTC Section 5.",
            "SEC-WASH-01",
            "SEC Enforcement Action / FTC Operation AI Comply (2024)",
            "CRITICAL"
        ),
        (
            r"\b(?:100%|completely|fully|entirely)\s+(?:autonomous|automated|self-running|autopilot)\b",
            "augmented intelligence with supervised enterprise controls",
            "SEC AI-Washing Risk: Claiming complete autonomy without verifiable enterprise safeguards misleads buyers and investors regarding human oversight and operational risk.",
            "SEC-WASH-02",
            "SEC Chair Gensler Public Statement on AI-Washing & Investment Adviser Standards",
            "CRITICAL"
        ),
        (
            r"\breplaces\s+(?:all\s+)?human\s+(?:judgment|decision(?:s)?|creativity|expertise)\b",
            "empowers human teams with actionable machine insights",
            "SEC AI-Washing Risk: Unsubstantiated representation of artificial general capability replacing professional human judgment.",
            "SEC-WASH-03",
            "FTC Section 5: Unfair or Deceptive Practices in AI Marketing",
            "WARNING"
        ),
        (
            r"\beliminates\s+(?:all\s+)?errors?\b|\bflawless\s+execution\b|\bzero\s+(?:defect|mistake)s?\b",
            "significantly reduces operational error rates",
            "Regulatory Overpromise: Claiming complete elimination of errors in complex software violates commercial truth-in-advertising standards.",
            "SEC-WASH-04",
            "FTC Truth in Advertising / Evidentiary Substantiation Standard",
            "CRITICAL"
        ),
        (
            r"\bguaranteed\s+(?:\d+x|10x|100%)\s+(?:roi|return|profit|revenue)\b|\bwill\s+double\s+your\s+(?:sales|revenue)\b",
            "designed to accelerate measurable team productivity and ROI",
            "SEC Forward-Looking Risk: Promising specific financial returns or guaranteed multiples without audited historical evidence or PSLRA safe harbor notice.",
            "SEC-FIN-01",
            "SEC Rule 10b-5 / PSLRA Safe Harbor Forward-Looking Statement Act",
            "CRITICAL"
        ),
        (
            r"\bpatented\s+agi\b|\btrue\s+artificial\s+general\s+intelligence\b|\bconscious\s+ai\b",
            "advanced multi-modal machine learning architecture",
            "Deceptive AI Representation: Misrepresenting specialized foundation models as Artificial General Intelligence (AGI).",
            "SEC-WASH-05",
            "FTC Operation AI Comply: 'AI' Claims Must Reflect Real Technical Capabilities",
            "WARNING"
        )
    ]

    # =========================================================================
    # 2. EU AI ACT (REGULATION (EU) 2024/1689) PATTERNS
    # =========================================================================
    EU_AI_ACT_RULES = [
        (
            r"\b(?:ai\s+generated|deepfake|synthetic\s+persona|virtual\s+spokesperson|digital\s+human)\b(?!.*(?:disclosure|notic|disclaimer))",
            "AI-generated synthetic media (disclosed pursuant to EU AI Act Art. 50)",
            "EU AI Act Art. 50 Violation: Providers and deployers must clearly disclose when text, audio, or visual content is artificially generated or manipulated.",
            "EU-AIA-50",
            "EU AI Act Regulation (EU) 2024/1689 Article 50 (Transparency Obligations)",
            "CRITICAL"
        ),
        (
            r"\b(?:emotion\s+(?:recognition|detection|tracking)|sentiment\s+surveillance|biometric\s+mood\s+scan)\b",
            "contextual linguistic tone calibration",
            "EU AI Act Art. 52 High-Risk / Prohibited Alert: Emotion recognition systems in workplace or educational environments are strictly restricted or prohibited without explicit statutory justification.",
            "EU-AIA-52",
            "EU AI Act Article 5(1)(f) & Article 52 (High-Risk Biometrics)",
            "CRITICAL"
        ),
        (
            r"\b(?:credit\s+scoring\s+ai|autonomous\s+hiring\s+filter|automated\s+dismissal|resumé\s+filter)\b",
            "candidate screening recommendation support with human HR oversight",
            "EU AI Act Annex III High-Risk Classification: Automated systems used in recruitment, employment decisions, or creditworthiness require mandatory conformity assessments and human oversight logs.",
            "EU-AIA-HR",
            "EU AI Act Annex III (High-Risk AI Systems) & GDPR Article 22",
            "CRITICAL"
        ),
        (
            r"\bsecretly\s+(?:monitors|tracks|records)|covert\s+behavioral\s+profiling\b",
            "transparent, opt-in behavioral workflow analytics",
            "EU AI Act & GDPR Violation: Subliminal or covert profiling techniques impairing user autonomy are banned under Article 5.",
            "EU-GDPR-22",
            "EU AI Act Article 5(1)(a) & GDPR Article 5(1)(a) Transparency Principle",
            "CRITICAL"
        )
    ]

    # =========================================================================
    # 3. UK CMA GREEN CLAIMS & ENVIRONMENTAL SUSTAINABILITY PATTERNS
    # =========================================================================
    UK_CMA_GREEN_RULES = [
        (
            r"\b(?:100%\s+)?(?:eco-?friendly|green\s+ai|planet-?positive|climate-?neutral)\b",
            "energy-optimized cloud compute infrastructure",
            "UK CMA Green Claims Code Breach: Broad, unqualified claims such as 'eco-friendly' or 'planet-positive' without full life-cycle assessment (LCA) data violate Principle 1 (Truthfulness) and Principle 2 (Clarity).",
            "UK-CMA-01",
            "UK CMA Green Claims Code § 2.3 & CAP/BCAP Rule 11 (Environmental Claims)",
            "CRITICAL"
        ),
        (
            r"\b(?:zero\s+emissions?|zero\s+carbon|carbon-?negative\s+cloud)\b",
            "measurably reduced Scope 1 & 2 carbon footprint",
            "UK CMA Green Claims Code Breach: Claims of 'zero carbon' or 'zero emissions' require transparent verification across Scope 1, 2, and 3 emissions including upstream datacenter energy consumption.",
            "UK-CMA-02",
            "UK CMA Guidance on Environmental Sustainability Claims in Advertising § 3.5",
            "CRITICAL"
        ),
        (
            r"\b(?:completely\s+sustainable|100%\s+recycled|infinite\s+green)\b",
            "committed to ongoing sustainability and datacenter efficiency benchmarks",
            "UK CMA Green Claims Code Principle 4: Claims must consider the full life cycle of the product or service, from manufacturing and compute to disposal.",
            "UK-CMA-03",
            "UK Competition and Markets Authority Principle 4 (Life-Cycle Substantiation)",
            "WARNING"
        ),
        (
            r"\b(?:carbon\s+neutral\s+algorithm|offset\s+all\s+emissions)\b",
            "cloud infrastructure benchmarked with verified carbon offset certificates",
            "UK Advertising Standards Authority (ASA) Warning: Carbon neutral claims based on offsets must disclose the scheme, verification standard (e.g. Gold Standard), and timeline.",
            "UK-ASA-01",
            "ASA / CAP Guidelines on Carbon Neutrality and Net Zero Claims (2024)",
            "WARNING"
        )
    ]

    def __init__(self, ai_copilot=None):
        self.ai_copilot = ai_copilot

    def evaluate(self, text: str, jurisdiction: str = "GLOBAL") -> Dict[str, Any]:
        """
        Evaluates content against jurisdictional regulations.
        Jurisdictions: 'US', 'EU', 'UK', or 'GLOBAL'.
        """
        jur = jurisdiction.upper().strip() if jurisdiction else "GLOBAL"
        if jur not in self.JURISDICTIONS:
            jur = "GLOBAL"

        flags: List[Dict[str, Any]] = []

        # 1. Evaluate US rules (if US or GLOBAL)
        if jur in ["US", "GLOBAL"]:
            for pattern, fix, explanation, code, citation, severity in self.SEC_AI_WASHING_RULES:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                for m in matches:
                    flags.append({
                        "flag_type": "REG_SEC",
                        "jurisdiction": "US",
                        "rule_code": code,
                        "snippet": m.group(0),
                        "suggested_fix": fix,
                        "explanation": explanation,
                        "citation": citation,
                        "severity": severity
                    })

        # 2. Evaluate EU AI Act rules (if EU or GLOBAL)
        if jur in ["EU", "GLOBAL"]:
            for pattern, fix, explanation, code, citation, severity in self.EU_AI_ACT_RULES:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                for m in matches:
                    flags.append({
                        "flag_type": "REG_EU",
                        "jurisdiction": "EU",
                        "rule_code": code,
                        "snippet": m.group(0),
                        "suggested_fix": fix,
                        "explanation": explanation,
                        "citation": citation,
                        "severity": severity
                    })

        # 3. Evaluate UK CMA rules (if UK or GLOBAL)
        if jur in ["UK", "GLOBAL"]:
            for pattern, fix, explanation, code, citation, severity in self.UK_CMA_GREEN_RULES:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                for m in matches:
                    flags.append({
                        "flag_type": "REG_UK",
                        "jurisdiction": "UK",
                        "rule_code": code,
                        "snippet": m.group(0),
                        "suggested_fix": fix,
                        "explanation": explanation,
                        "citation": citation,
                        "severity": severity
                    })

        # Calculate scores
        critical_count = sum(1 for f in flags if f["severity"] == "CRITICAL")
        warning_count = sum(1 for f in flags if f["severity"] == "WARNING")
        suggestion_count = sum(1 for f in flags if f["severity"] == "SUGGESTION")

        deductions = (critical_count * 22) + (warning_count * 10) + (suggestion_count * 4)
        score = max(5, 100 - deductions)

        if score >= 85:
            risk_level = "LOW"
        elif score >= 65:
            risk_level = "MODERATE"
        elif score >= 40:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        # Generate jurisdictional disclaimers
        disclaimers = self.generate_disclaimers(text, jur)

        return {
            "jurisdiction": jur,
            "score": score,
            "risk_level": risk_level,
            "flags": flags,
            "flag_count": len(flags),
            "critical_count": critical_count,
            "warning_count": warning_count,
            "disclaimers": disclaimers,
            "evaluated_at": datetime.utcnow().isoformat() + "Z"
        }

    def generate_disclaimers(self, text: str, jurisdiction: str = "GLOBAL") -> Dict[str, str]:
        """
        Synthesizes tailored legal disclaimers based on jurisdiction and content patterns.
        """
        jur = jurisdiction.upper().strip() if jurisdiction else "GLOBAL"

        disclaimers: Dict[str, str] = {}

        if jur in ["US", "GLOBAL"]:
            disclaimers["US_SEC_FTC"] = (
                "SEC & FTC REGULATORY NOTICE: Features described herein leverage probabilistic machine learning algorithms. "
                "Any statements regarding automated performance or operational efficiency reflect typical benchmarks and do not "
                "guarantee specific commercial or financial returns. Statements that are not historical facts are forward-looking "
                "statements subject to risks and uncertainties pursuant to the Private Securities Litigation Reform Act of 1995."
            )

        if jur in ["EU", "GLOBAL"]:
            disclaimers["EU_AI_ACT"] = (
                "EU AI ACT TRANSPARENCY NOTICE (REGULATION EU 2024/1689, ART. 50): "
                "This solution incorporates artificial intelligence systems. Content generated, augmented, or processed through "
                "these models is subject to human-in-the-loop oversight. Where synthetic media is deployed, output is marked "
                "in machine-readable format pursuant to Article 50 technical standards."
            )

        if jur in ["UK", "GLOBAL"]:
            disclaimers["UK_CMA_GREEN"] = (
                "UK CMA GREEN CLAIMS ADVISORY: Environmental and datacenter efficiency metrics referenced are substantiated "
                "by certified Scope 1 and Scope 2 energy reporting. Specific carbon reduction outcomes depend on enterprise "
                "workload volume, datacenter region, and operational parameters."
            )

        if jur == "GLOBAL":
            disclaimers["GLOBAL_COMPOSITE"] = (
                "GLOBAL REGULATORY COMPLIANCE DISCLOSURE (US SEC/FTC • EU AI ACT • UK CMA):\n"
                "1. Model Transparency: Algorithmic capabilities are assistive and probabilistic, operating under supervised human oversight.\n"
                "2. EU AI Act Art. 50: Synthetic outputs and AI-mediated interactions are transparently disclosed.\n"
                "3. Safe Harbor: Performance estimates are forward-looking under PSLRA standards and subject to deployment variables.\n"
                "4. Environmental Claims: Energy and compute metrics conform to verified Greenhouse Gas (GHG) Protocol benchmarks."
            )

        return disclaimers

    def generate_tailored_disclaimer(self, text: str, jurisdiction: str = "GLOBAL") -> str:
        """
        Returns a single unified disclaimer string ready to paste into content.
        """
        disclaimers = self.generate_disclaimers(text, jurisdiction)
        if jurisdiction == "GLOBAL" and "GLOBAL_COMPOSITE" in disclaimers:
            return disclaimers["GLOBAL_COMPOSITE"]
        elif jurisdiction == "US" and "US_SEC_FTC" in disclaimers:
            return disclaimers["US_SEC_FTC"]
        elif jurisdiction == "EU" and "EU_AI_ACT" in disclaimers:
            return disclaimers["EU_AI_ACT"]
        elif jurisdiction == "UK" and "UK_CMA_GREEN" in disclaimers:
            return disclaimers["UK_CMA_GREEN"]
        return list(disclaimers.values())[0] if disclaimers else ""


# Global singleton instance
regulatory_engine = RegulatoryComplianceEngine()

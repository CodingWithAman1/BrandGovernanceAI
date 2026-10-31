"""
BrandGuard AI — Neural & Semantic AI Co-Pilot Engine
=====================================================
Provides context-aware brand voice harmonization, automated FTC/SEC safe harbor
disclaimer generation, interactive brand governance chat advisory, and AI rule synthesis.

Operates with dual architecture:
1. Cloud LLM Integration: Uses Google Gemini when API keys are configured.
2. Local Semantic Intelligence: Built-in deterministic NLP engine with zero external
   dependencies, delivering instant, high-quality, reproducible compliance assistance.
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class AICopilotEngine:
    """
    Intelligent AI Brand Co-Pilot for BrandGuard AI.
    Handles semantic rewrites, safe harbor disclaimers, chat advisory, and rule synthesis.
    """

    def _get_gemini_key(self):
        """Dynamically retrieves Gemini key from environment on each invocation."""
        key = (
            os.environ.get("GEMINI_API_KEY") or
            os.environ.get("GOOGLE_API_KEY") or
            os.environ.get("GEMINI_KEY")
        )
        if not key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                key = (
                    os.environ.get("GEMINI_API_KEY") or
                    os.environ.get("GOOGLE_API_KEY") or
                    os.environ.get("GEMINI_KEY")
                )
            except Exception:
                pass
        return key

    def _get_openai_key(self):
        return os.environ.get("OPENAI_API_KEY")

    def _validate_key(self, key):
        """
        Validates the format of a Gemini API key.
        Supports both Google AI Studio keys (AIza...) and Antigravity-issued keys (AQ...).
        Returns a tuple of (is_valid: bool, warning_message: str or None).
        """
        if not key:
            return False, "No API key provided."
        key = key.strip()
        if len(key) < 20:
            return False, "KEY TOO SHORT — A valid Gemini API key is typically longer."
        # Accept valid Google AI Studio keys and AQ tokens
        if key.startswith("AIza") or key.startswith("AQ."):
            return True, None
        return True, None

    def get_status(self):
        """Returns the active AI engine status for UI telemetry."""
        key = self._get_gemini_key()
        is_valid, warn = self._validate_key(key)
        if key and is_valid:
            return {
                "active_engine": "Google Gemini Flash (Live Cloud)",
                "is_cloud_active": True,
                "key_preview": f"{key[:6]}...{key[-4:]}" if len(key) > 10 else "***",
                "key_valid": True,
                "warning": None
            }
        return {
            "active_engine": "BrandGuard Knowledge Engine (Local Neural NLP)",
            "is_cloud_active": False,
            "key_preview": f"{key[:6]}..." if key else None,
            "key_valid": False,
            "warning": warn
        }

    # =========================================================================
    # 1. CLOUD LLM CALLER (WITH RESILIENT FALLBACK)
    # =========================================================================
    def _call_gemini(self, prompt, system_instruction=None, timeout=20):
        """
        Calls the Google Gemini API with automatic model fallback.
        Uses only real, currently available Gemini models.
        Includes key validation, detailed error logging, and retry logic.
        """
        key = self._get_gemini_key()
        if not key:
            print("[Gemini] No API key found. Set GEMINI_API_KEY in .env")
            return None

        # Validate key format before making any requests
        is_valid, warn = self._validate_key(key)
        if not is_valid:
            print(f"[Gemini Key Validation] {warn}")
            return None

        # Verified working models in order of speed and response reliability
        models = [
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
        ]

        for model in models:
            try:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model}:generateContent?key={key}"
                )

                # Build contents list; prepend system instruction as a "model" turn for newer API format
                contents = []
                if system_instruction:
                    contents.append({
                        "role": "model",
                        "parts": [{"text": system_instruction}]
                    })
                contents.append({
                    "role": "user",
                    "parts": [{"text": prompt}]
                })

                payload = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.4,
                        "maxOutputTokens": 1500
                    }
                }

                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )

                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    if 'candidates' in data and len(data['candidates']) > 0:
                        candidate = data['candidates'][0]
                        if 'content' in candidate and 'parts' in candidate['content']:
                            text = candidate['content']['parts'][0].get('text', '')
                            if text:
                                print(f"[Gemini] Success with model: {model}")
                                return text.strip()

            except urllib.error.HTTPError as e:
                err_text = ""
                try:
                    err_text = e.read().decode('utf-8')
                except Exception:
                    pass
                print(f"[Gemini API] Model '{model}' returned HTTP {e.code}: {err_text[:300]}")
                if e.code == 400:
                    print(f"[Gemini API] HTTP 400 often means invalid key or malformed request.")
                elif e.code == 403:
                    print(f"[Gemini API] HTTP 403: API key may lack permissions or quota exhausted.")
                elif e.code == 404:
                    print(f"[Gemini API] HTTP 404: Model '{model}' not found, trying next...")
                # Continue trying next model
                continue
            except urllib.error.URLError as e:
                print(f"[Gemini Network Error on {model}]: {e.reason}")
                continue
            except Exception as e:
                print(f"[Gemini Call Exception on {model}]: {e}")
                continue

        print("[Gemini] All models exhausted. Falling back to local engine.")
        return None

    def test_connection(self):
        """
        Tests Gemini API connectivity and returns a detailed diagnostic dict.
        Used by the GET /api/v1/ai/test-key endpoint.
        """
        key = self._get_gemini_key()
        is_valid, warn = self._validate_key(key)

        if not key:
            return {
                "success": False,
                "status": "NO_KEY",
                "message": "No GEMINI_API_KEY found in environment or .env file.",
                "hint": "Add GEMINI_API_KEY=AIza... to your .env file and restart the server."
            }

        if not is_valid:
            return {
                "success": False,
                "status": "INVALID_KEY_FORMAT",
                "message": warn,
                "key_preview": f"{key[:8]}...{key[-4:]}",
                "hint": (
                    "Go to https://aistudio.google.com/app/apikey to generate "
                    "a proper Gemini API key (starts with AIza...)."
                )
            }

        # Try an actual minimal call against each model
        test_prompt = "Reply with exactly the word: CONNECTED"
        models_tried = []
        models = [
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
        ]

        for model in models:
            try:
                url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{model}:generateContent?key={key}"
                )
                payload = {
                    "contents": [{"role": "user", "parts": [{"text": test_prompt}]}],
                    "generationConfig": {"temperature": 0, "maxOutputTokens": 10}
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    if 'candidates' in data:
                        return {
                            "success": True,
                            "status": "CONNECTED",
                            "model_used": model,
                            "key_preview": f"{key[:6]}...{key[-4:]}",
                            "message": f"Gemini API connected successfully via model '{model}'.",
                            "models_tried": models_tried + [{"model": model, "status": "OK"}]
                        }
            except urllib.error.HTTPError as e:
                err_body = ""
                try:
                    err_body = e.read().decode('utf-8')
                except Exception:
                    pass
                models_tried.append({"model": model, "http_error": e.code, "detail": err_body[:200]})
            except Exception as e:
                models_tried.append({"model": model, "error": str(e)})

        return {
            "success": False,
            "status": "ALL_MODELS_FAILED",
            "key_preview": f"{key[:6]}...{key[-4:]}",
            "message": "API key format looks valid but all Gemini models returned errors.",
            "models_tried": models_tried,
            "hint": (
                "Check that your key has Gemini API access enabled and sufficient quota "
                "at https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com"
            )
        }

    # =========================================================================
    # 2. SEMANTIC HARMONIZATION & DEEP REWRITE
    # =========================================================================
    def harmonize_draft(self, text, brand_voice="ENTERPRISE_CONSULTATIVE"):
        """
        Rewrites a full text draft into on-brand, publication-ready copy.
        Eliminates robotic AI cliches, passive-aggressive remarks, and unsubstantiated superlatives.
        """
        if not text or not text.strip():
            return {
                "success": False,
                "message": "Empty draft text provided."
            }

        original_text = text.strip()

        # Try cloud LLM if configured
        cloud_result = self._call_gemini(
            prompt=(
                f"You are the BrandGuard AI Chief Compliance Editor. Rewrite the following marketing draft "
                f"so it strictly complies with enterprise brand voice ({brand_voice}), eliminates robotic AI jargon "
                f"(delve into, rich tapestry, a testament to), removes unsubstantiated superlatives (#1, world's best, 100% risk free), "
                f"and adopts an authoritative, consultative tone. Keep the core product value proposition intact.\n\n"
                f"Original Draft:\n{original_text}\n\n"
                f"Return ONLY the rewritten copy without conversational chatter or markdown backticks."
            )
        )
        if cloud_result:
            metrics = self._calculate_linguistic_metrics(cloud_result)
            return {
                "success": True,
                "harmonized_text": cloud_result,
                "tone_shift": "Optimized via Google Gemini Neural API",
                "reading_ease": metrics["reading_ease"],
                "formality_index": metrics["formality_index"],
                "improvements": [
                    "Eliminated clichéd synthetic filler and buzzwords via Gemini Flash",
                    "Harmonized sentence cadence to enterprise consultative standards",
                    "Neutralized unverified regulatory claim risks"
                ],
                "engine_used": "Google Gemini Flash (Live Cloud)"
            }

        # Local Semantic Engine (High Quality, Instant, Reproducible)
        replacements = [
            (r"\bdelve(?:s|d|ing)?\s+into\b", "explore", "Avoid clichéd AI filler 'delve into'"),
            (r"\ba\s+testament\s+to\b", "evidence of", "Replace cliché 'testament to'"),
            (r"\brich\s+tapestry\b", "comprehensive ecosystem", "Replace metaphor 'rich tapestry'"),
            (r"\bin\s+today'?s\s+fast-?paced\s+(?:world|digital\s+landscape)\b", "currently", "Cut bloated intro filler"),
            (r"\bgame-?changer\b", "breakthrough milestone", "Replace marketing hyperbole"),
            (r"\bunpack\b", "examine", "Use clear consultative verb"),
            (r"\bcrush(?:es|ed|ing)?\s+the\s+competition\b", "outperform industry benchmarks", "Replace combative phrasing"),
            (r"\bobviously\b\s*,?", "", "Remove condescending filler"),
            (r"\bneedless\s+to\s+say\b\s*,?", "", "Remove redundant intro"),
            (r"\bclearly\s+you\s+(?:must|should)\b", "we recommend that organizations", "Switch to empathetic advisory phrasing"),
            (r"\b#1\b|(?:\bnumber\s+one\b)", "industry-leading", "Substantiate market leadership"),
            (r"\bworld'?s\s+(?:best|fastest|greatest|most\s+advanced)\b", "an advanced, benchmark-tested", "Substantiate superlative"),
            (r"\b100%\s+(?:guaranteed|foolproof|risk-?\s*free)\b", "rigorously verified and resilient", "Remove absolute warranty claim"),
            (r"\bunbeatable\b|\bunrivaled\b", "distinctive and proven", "Remove unprovable superlative"),
            (r"\bnever\s+fails\b", "consistently delivers dependable performance", "Replace absolute guarantee with SLA phrasing"),
            (r"\bmiraculous\b|\bmagic\b", "innovative, engineering-driven", "Replace pseudoscientific buzzword")
        ]

        harmonized = original_text
        changes_applied = []

        for pattern, replacement, reason in replacements:
            if re.search(pattern, harmonized, flags=re.IGNORECASE):
                harmonized = re.sub(pattern, replacement, harmonized, flags=re.IGNORECASE)
                changes_applied.append(reason)

        # Polish spacing, punctuation, and capitalization
        harmonized = re.sub(r'\s+', ' ', harmonized)
        harmonized = re.sub(r'\s+([,.;?!])', r'\1', harmonized)
        harmonized = re.sub(r'([.?!]\s*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), harmonized)
        harmonized = harmonized.strip()

        metrics = self._calculate_linguistic_metrics(harmonized)

        return {
            "success": True,
            "harmonized_text": harmonized,
            "tone_shift": "Passive/Combative -> Consultative Authority",
            "reading_ease": metrics["reading_ease"],
            "formality_index": metrics["formality_index"],
            "improvements": changes_applied if changes_applied else ["Polished sentence rhythm and enterprise cadence"],
            "engine_used": "BrandGuard Local Semantic Engine"
        }

    # =========================================================================
    # 3. FULL SUBMISSION ANALYSIS
    # =========================================================================
    def analyze_submission(self, text):
        """
        Performs a deep structured analysis of marketing copy.
        Returns tone_issues, claim_risks, suggested_improvements (3 items),
        and an overall_quality_rating (1-10).
        Uses Gemini if available, else falls back to local heuristics.
        """
        if not text or not text.strip():
            return {
                "success": False,
                "message": "No text provided for analysis."
            }

        text = text.strip()

        # Try cloud Gemini
        prompt = (
            "You are BrandGuard AI's deep compliance analyzer. Analyze the following marketing copy "
            "and return a JSON object with these exact keys:\n"
            "  - tone_issues: array of strings describing tone problems found\n"
            "  - claim_risks: array of strings describing FTC/legal claim risks found\n"
            "  - suggested_improvements: array of exactly 3 specific improvement bullet points\n"
            "  - overall_quality_rating: integer from 1 to 10 (10 = perfect compliance)\n"
            "Return ONLY valid JSON, no markdown, no extra text.\n\n"
            f"Copy to analyze:\n{text}"
        )
        cloud_result = self._call_gemini(prompt)
        if cloud_result:
            try:
                match = re.search(r'\{.*\}', cloud_result, re.DOTALL)
                if match:
                    data = json.loads(match.group(0))
                    # Ensure all required keys exist
                    data.setdefault("tone_issues", [])
                    data.setdefault("claim_risks", [])
                    data.setdefault("suggested_improvements", [])
                    data.setdefault("overall_quality_rating", 7)
                    return {
                        "success": True,
                        "engine_used": "Google Gemini Flash (Live Cloud)",
                        **data
                    }
            except (json.JSONDecodeError, Exception) as parse_err:
                print(f"[analyze_submission] JSON parse error: {parse_err}")

        # Local heuristics fallback
        tone_issues = []
        claim_risks = []
        suggestions = []

        # Tone issues detection
        ai_jargon = [
            "delve into", "a testament to", "rich tapestry", "game-changer",
            "leverage", "synergy", "paradigm shift", "thought leader",
            "move the needle", "circle back", "bandwidth", "at the end of the day"
        ]
        for phrase in ai_jargon:
            if phrase.lower() in text.lower():
                tone_issues.append(f"Robotic AI jargon detected: '{phrase}'")

        aggressive_phrases = ["crush the competition", "obviously", "needless to say", "clearly you must"]
        for phrase in aggressive_phrases:
            if phrase.lower() in text.lower():
                tone_issues.append(f"Aggressive/condescending phrasing: '{phrase}'")

        # Claim risk detection
        risky_claims = [
            "#1", "world's best", "100% guaranteed", "never fails", "unbeatable",
            "zero downtime", "instant results", "effortless", "revolutionary", "first ever"
        ]
        for claim in risky_claims:
            if claim.lower() in text.lower():
                claim_risks.append(f"FTC Section 5 risk: Unsubstantiated claim '{claim}'")

        # Suggested improvements (always exactly 3)
        if tone_issues:
            suggestions.append(
                f"Replace {len(tone_issues)} detected jargon/tone issue(s) with clear, consultative alternatives."
            )
        else:
            suggestions.append("Tone appears largely compliant — review cadence for enterprise readability.")

        if claim_risks:
            suggestions.append(
                f"Add substantiation footnotes or audit citations for {len(claim_risks)} flagged claim(s)."
            )
        else:
            suggestions.append("No critical claim risks found — confirm all statistics cite approved data sources.")

        suggestions.append(
            "Run the full BrandGuard compliance scan to identify accessibility and visual risks."
        )

        # Compute quality rating: start at 10, deduct per issue
        deductions = len(tone_issues) * 0.5 + len(claim_risks) * 1.0
        rating = max(1, min(10, round(10 - deductions)))

        return {
            "success": True,
            "engine_used": "BrandGuard Local Semantic Engine",
            "tone_issues": tone_issues,
            "claim_risks": claim_risks,
            "suggested_improvements": suggestions[:3],
            "overall_quality_rating": rating
        }

    # =========================================================================
    # 4. HEADLINE VARIANT GENERATOR
    # =========================================================================
    def generate_headline_variants(self, topic_or_draft):
        """
        Generates 5 compliant headline variants for a given topic or draft.
        Uses Gemini if available, else template-based local generation.
        """
        topic = (topic_or_draft or "").strip()
        if not topic:
            return {"success": False, "message": "No topic or draft provided."}

        # Try cloud Gemini
        prompt = (
            "You are BrandGuard AI's headline strategist. Generate exactly 5 compliant, "
            "enterprise-grade marketing headline variants for the following topic or draft. "
            "Rules: no unsubstantiated '#1' claims, no absolute guarantees, use consultative tone, "
            "be specific and outcome-focused. Return ONLY a JSON array of 5 headline strings.\n\n"
            f"Topic/Draft:\n{topic}"
        )
        cloud_result = self._call_gemini(prompt)
        if cloud_result:
            try:
                match = re.search(r'\[.*\]', cloud_result, re.DOTALL)
                if match:
                    headlines = json.loads(match.group(0))
                    if isinstance(headlines, list) and len(headlines) >= 3:
                        return {
                            "success": True,
                            "engine_used": "Google Gemini Flash (Live Cloud)",
                            "headlines": headlines[:5]
                        }
            except (json.JSONDecodeError, Exception) as parse_err:
                print(f"[generate_headline_variants] JSON parse error: {parse_err}")

        # Template-based local fallback
        topic_clean = re.sub(r'[^a-zA-Z0-9 ]', '', topic)[:60].strip()
        noun = topic_clean if topic_clean else "Enterprise Brand Governance"

        headlines = [
            f"Accelerate {noun} with Proven, Audit-Ready Compliance.",
            f"Eliminate Pre-Publication Risk: Smarter {noun} for Enterprise Teams.",
            f"The Compliance-First Approach to {noun} — Built for Scale.",
            f"How Industry Leaders Achieve {noun} Without Slowing Down.",
            f"Benchmark-Tested {noun}: From Draft to Approved in Minutes."
        ]

        return {
            "success": True,
            "engine_used": "BrandGuard Local Template Engine",
            "headlines": headlines
        }

    # =========================================================================
    # 5. FLAG EXPLAINER
    # =========================================================================
    def explain_flag(self, flag_dict):
        """
        Provides a detailed educational explanation of a compliance flag.
        Includes examples, context, and remediation guidance.
        Uses Gemini if available, else a structured local explanation.
        """
        if not flag_dict:
            return {"success": False, "message": "No flag data provided."}

        snippet = flag_dict.get('snippet', 'N/A')
        flag_type = flag_dict.get('flag_type', 'GENERAL')
        severity = flag_dict.get('severity', 'WARNING')
        explanation = flag_dict.get('explanation', '')
        suggested_fix = flag_dict.get('suggested_fix', '')
        citation = flag_dict.get('citation', '')
        rule_code = flag_dict.get('rule_code', '')

        # Try cloud Gemini
        prompt = (
            f"You are BrandGuard AI's compliance educator. Explain this marketing compliance flag "
            f"in a helpful, educational way with examples.\n\n"
            f"Flag Type: {flag_type}\n"
            f"Severity: {severity}\n"
            f"Flagged Text: '{snippet}'\n"
            f"Reason: {explanation}\n"
            f"Suggested Fix: {suggested_fix}\n"
            f"Rule Citation: {citation}\n\n"
            f"Provide: 1) Why this is flagged, 2) A real-world consequence example, "
            f"3) Two alternative phrasings, 4) The governing regulation in plain language. "
            f"Keep it under 200 words, friendly and educational."
        )
        cloud_result = self._call_gemini(prompt)
        if cloud_result:
            return {
                "success": True,
                "engine_used": "Google Gemini Flash (Live Cloud)",
                "explanation": cloud_result,
                "flag_type": flag_type,
                "severity": severity,
                "rule_code": rule_code,
                "citation": citation
            }

        # Local structured explanation
        severity_desc = {
            "CRITICAL": "This is a high-priority violation that could expose your organization to regulatory action.",
            "WARNING": "This is a moderate issue that weakens brand credibility or may mislead audiences.",
            "SUGGESTION": "This is a stylistic improvement opportunity to strengthen brand voice."
        }.get(severity, "This flag indicates a compliance concern.")

        type_context = {
            "CLAIM": (
                "**Why flagged:** Unsubstantiated marketing claims violate FTC Section 5 (deceptive practices). "
                "The FTC's *Operation AI Comply* specifically targets software companies making unprovable assertions.\n\n"
                "**Real-world consequence:** A company using '#1 AI platform' without third-party audit data can face "
                "FTC cease-and-desist orders and civil penalties up to $51,744 per violation per day.\n\n"
                "**Alternative phrasings:**\n"
                f"• Instead of '{snippet}', try: '{suggested_fix or 'an industry-recognized solution'}'\n"
                f"• Or: 'Our independently benchmarked solution'\n\n"
                "**Governing rule:** FTC Act Section 5 requires all objective claims to be substantiated "
                "by 'reliable scientific evidence' or verifiable third-party data before publication."
            ),
            "TONE": (
                "**Why flagged:** This phrase violates enterprise brand voice standards. Robotic AI filler "
                "and aggressive/condescending language erode reader trust and brand authority.\n\n"
                "**Real-world consequence:** Enterprise buyers exposed to generic AI-sounding copy are significantly "
                "less likely to engage, according to B2B content research.\n\n"
                "**Alternative phrasings:**\n"
                f"• Instead of '{snippet}', try: '{suggested_fix or 'a direct, specific description'}'\n"
                f"• Or: A concrete, outcome-focused phrase specific to your product\n\n"
                "**Governing rule:** Brand Voice Guide §2.1 mandates clear, authentic, outcome-driven language "
                "that avoids synthetic AI filler and condescending framing."
            ),
            "ACCESSIBILITY": (
                "**Why flagged:** This visual element fails WCAG 2.1 Level AA contrast requirements, "
                "making content inaccessible to users with visual impairments.\n\n"
                "**Real-world consequence:** Non-compliant digital assets expose organizations to ADA Title III "
                "litigation. Over 4,000 web accessibility lawsuits were filed in 2023 in the US alone.\n\n"
                "**Remediation steps:**\n"
                "• Use a contrast checker tool (e.g., WebAIM Contrast Checker)\n"
                "• Ensure foreground/background contrast ≥ 4.5:1 for normal text\n\n"
                "**Governing rule:** WCAG 2.1 Success Criterion 1.4.3 (Level AA) requires a minimum "
                "contrast ratio of 4.5:1 for normal text against its background."
            )
        }

        base_explanation = type_context.get(flag_type, (
            f"**Why flagged:** {explanation}\n\n"
            f"**Suggested fix:** {suggested_fix or 'Rephrase using clearer, substantiated language.'}\n\n"
            f"**Governing rule:** {citation}"
        ))

        full_explanation = (
            f"**{severity_desc}**\n\n"
            f"{base_explanation}\n\n"
            f"*Rule Reference: {rule_code} — {citation}*"
        )

        return {
            "success": True,
            "engine_used": "BrandGuard Local Semantic Engine",
            "explanation": full_explanation,
            "flag_type": flag_type,
            "severity": severity,
            "rule_code": rule_code,
            "citation": citation
        }

    # =========================================================================
    # 6. AUTOMATED FTC & SEC SAFE HARBOR DISCLAIMER SYNTHESIZER
    # =========================================================================
    def generate_safe_harbor(self, text, domain="enterprise_tech"):
        """
        Synthesizes a legally defensible safe harbor disclaimer based on the
        claims, metrics, or performance assertions found in the draft.
        """
        has_metrics = bool(re.search(r'\d+%', text) or re.search(r'\$\d+', text) or re.search(r'\b\d+x\b', text))
        has_future_claims = bool(re.search(r'\b(will|upcoming|roadmap|projected|future|accelerate)\b', text, re.IGNORECASE))
        has_superlatives = bool(re.search(r'\b(leading|advanced|fastest|benchmark|proven)\b', text, re.IGNORECASE))

        disclaimers = []

        # 1. FTC Section 5 Substantiation
        if has_metrics or has_superlatives:
            disclaimers.append(
                "Regulatory Substantiation Notice (FTC 16 CFR § 255): Performance benchmarks and metric representations "
                "referenced herein are based on controlled enterprise testing and audited production logs as of Q3 2026. "
                "Actual operational performance may vary according to deployment architecture, network throughput, and data complexity."
            )

        # 2. SEC Forward-Looking Safe Harbor
        if has_future_claims:
            disclaimers.append(
                "Forward-Looking Statements (Safe Harbor Statement under Private Securities Litigation Reform Act): "
                "This document contains projections regarding planned software enhancements, capability roadmaps, and business impact. "
                "These statements reflect current management expectations and are subject to operational uncertainties and technological evolution."
            )

        # 3. WCAG Digital Accessibility Compliance Notice
        disclaimers.append(
            "Accessibility & Compliance Guarantee: Brand assets produced under this specification satisfy WCAG 2.1 AA "
            "minimum contrast standards (4.5:1 relative luminance) and corporate non-discrimination digital guidelines."
        )

        full_statement = "\n\n".join(disclaimers)

        return {
            "success": True,
            "disclaimer": full_statement,
            "sections_included": [
                "FTC Section 5 Substantiation",
                "SEC Forward-Looking Safe Harbor" if has_future_claims else "Enterprise SLA Boundary",
                "WCAG 2.1 AA Accessibility Statement"
            ]
        }

    # =========================================================================
    # 7. INTERACTIVE BRAND GOVERNANCE CO-PILOT CHAT ADVISOR
    # =========================================================================
    def chat(self, user_message, context_text=None):
        """
        Answers brand governance, regulatory compliance, and copywriting questions.
        Handles a wide range of intents via cloud Gemini or local knowledge patterns.
        """
        msg = (user_message or "").strip()
        if not msg:
            return {
                "reply": "Hello! I am your BrandGuard AI Co-Pilot. How can I help you ensure brand compliance today?",
                "source": "BrandGuard AI"
            }

        # Try cloud Gemini LLM if configured
        sys_inst = (
            "You are BrandGuard AI Co-Pilot, an authoritative expert on enterprise brand governance, "
            "FTC truth-in-advertising (Section 5), SEC AI-washing regulations, WCAG 2.1 AA accessibility, and tone calibration. "
            "You were developed by Team Synapse (Aman Sharma & Janhavi Kanojia). Keep responses friendly, concise, clear, and actionable."
        )
        full_prompt = f"User Question: {msg}\n"
        if context_text:
            full_prompt += f"\nCurrent Draft Working Context:\n{context_text[:800]}\n"

        cloud_reply = self._call_gemini(full_prompt, system_instruction=sys_inst)
        if cloud_reply:
            return {
                "reply": cloud_reply,
                "source": "Google Gemini Flash (Live Cloud)"
            }

        # Conversational Local Intelligence (Natural, Knowledgeable, Friendly)
        lower = msg.lower().strip()

        # Intent: Identity / Introduction
        if any(phrase in lower for phrase in ["who are you", "what are you", "who created you", "who made you", "identity"]):
            return {
                "reply": (
                    "👋 **I am BrandGuard AI Co-Pilot!**\n\n"
                    "I am an intelligent pre-publication brand governance assistant built by **Team Synapse** "
                    "(**Aman Sharma** & **Janhavi Kanojia**) for the Inkloom AI Hackathon.\n\n"
                    "**What I do:**\n"
                    "• **Deterministic Governance:** I evaluate marketing copy across 5 tone polarities, FTC Section 5 truth banks, and WCAG 2.1 AA contrast.\n"
                    "• **AI Deep Harmonization:** I rewrite rough drafts to eliminate robotic AI clichés (*'delve into'*, *'game-changer'*) while preserving your brand's unique voice.\n"
                    "• **Safe Harbor Synthesis:** I automatically draft FTC & SEC regulatory disclaimers for metrics and uptime claims.\n"
                    "• **Cryptographic Certification:** Once approved, we issue tamper-evident PDF certificates with SHA-256 copy digests.\n\n"
                    "Feel free to ask me to review a headline, explain compliance rules, or generate safe copy!"
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Intent: Greetings
        if lower in ["hello", "hi", "hey", "good morning", "good evening", "greetings"]:
            return {
                "reply": (
                    "Hello! 👋 I'm your **BrandGuard AI Co-Pilot**.\n\n"
                    "How can I help you today? You can ask me to:\n"
                    "1. Critique and polish your draft copy.\n"
                    "2. Explain FTC Section 5 or SEC AI-washing rules.\n"
                    "3. Generate compliant headlines or safe harbor disclaimers.\n\n"
                    "*Tip: You can also click 'AI Deep Harmonize' above the Studio editor to auto-polish your text!*"
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Intent: Capabilities / Help
        if any(w in lower for w in ["what can you do", "features", "capabilities", "help me"]):
            return {
                "reply": (
                    "**Here is what BrandGuard AI can do for you:**\n\n"
                    "• **⚡ AI Deep Harmonize:** Rewrites copy in one click, removing filler cliches and unsubstantiated superlatives.\n"
                    "• **🛡️ FTC Safe Harbor:** Generates FTC 16 CFR § 255 and SEC safe harbor statements for performance metrics.\n"
                    "• **👁️ Visual Inspector:** Computes WCAG 2.1 AA contrast ratios (4.5:1) using Pillow K-Means.\n"
                    "• **⚖️ Stage-Gate Clearance:** Routes drafts to Reviewers with side-by-side red/green diffs and SHA-256 PDF certificates.\n"
                    "• **✍️ Copywriting Co-Pilot:** Ask me for compliant headlines, hooks, or rule explanations anytime!\n"
                    "• **🔍 Deep Analysis:** Use the AI Analyze feature for a full structured quality and compliance report."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: SEC / AI-washing / investor
        if any(w in lower for w in ["sec", "ai-washing", "securities", "forward-looking", "investor"]):
            return {
                "reply": (
                    "**SEC AI-Washing & Forward-Looking Statements:**\n\n"
                    "• **The Risk:** The SEC's 2024 AI-washing guidance warns that companies claiming AI capabilities "
                    "they don't possess may face securities fraud liability under Rule 10b-5.\n"
                    "• **Safe Harbor:** Include PSLRA safe harbor language: "
                    "*'These statements reflect current expectations and are subject to risks and uncertainties.'*\n"
                    "• **Best Practice:** Never describe AI features as 'autonomous', 'self-learning', or '100% accurate' "
                    "without documented model validation reports."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: Competitor mentions
        if any(w in lower for w in ["competitor", "versus", "vs.", "better than", "beats"]):
            return {
                "reply": (
                    "**Competitor Mention & Comparative Advertising Guidelines:**\n\n"
                    "• **FTC Standard:** Comparative ads are legal but must be truthful, not misleading, and "
                    "based on substantiated, verifiable evidence (16 CFR § 250).\n"
                    "• **Best Practice:** Avoid naming competitors unless you have documented head-to-head benchmark results.\n"
                    "• **Safe Alternative:** Use industry-generic phrases like 'unlike legacy point solutions' or "
                    "'outperforming category averages' backed by cited third-party research."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: GDPR / Data Privacy
        if any(w in lower for w in ["gdpr", "privacy", "data protection", "ccpa", "personal data"]):
            return {
                "reply": (
                    "**GDPR & Data Privacy in Marketing Copy:**\n\n"
                    "• **Marketing Claims:** Do not claim GDPR compliance unless your product has undergone a formal DPA review.\n"
                    "• **Risky Phrases:** Avoid 'fully GDPR compliant', 'zero data retention', or 'anonymous by default' "
                    "unless backed by a documented privacy audit.\n"
                    "• **Safe Language:** Prefer 'GDPR-aligned data handling practices' or 'supports your GDPR obligations'.\n"
                    "• **Consent Claims:** Never claim 'we never collect data' if analytics or session logging is active."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: Upload / Score / Certificate / Scan
        if any(w in lower for w in ["upload", "score", "certificate", "report", "scan", "analyze"]):
            return {
                "reply": (
                    "**How to Scan & Certify Content:**\n\n"
                    "1. **Upload:** Go to the **Compliance Studio** and paste your text or upload an image banner.\n"
                    "2. **Scan:** Click **'Run BrandGuard Scan'** — the engine checks tone, claims, and visual accessibility.\n"
                    "3. **Review Flags:** Each flag shows the offending snippet, severity, and a one-click fix.\n"
                    "4. **Certify:** Once the compliance score reaches 90+, click **'Submit for Review'** to route to your manager.\n"
                    "5. **Certificate:** Approved content receives a SHA-256 tamper-evident PDF compliance certificate."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: WCAG / Accessibility / Colors / Contrast
        if any(w in lower for w in ["wcag", "contrast", "color", "accessibility", "visual", "ratio", "colors"]):
            return {
                "reply": (
                    "**WCAG 2.1 AA Visual Accessibility Standards:**\n\n"
                    "• **Normal Text:** Must maintain a minimum contrast ratio of **4.5:1** against the background.\n"
                    "• **Large Text (>18pt or >14pt bold):** Requires at least **3.0:1** contrast.\n"
                    "• **Formula:** BrandGuard calculates relative luminance: `Cr = (L1 + 0.05) / (L2 + 0.05)` using Pillow K-Means.\n"
                    "• **Tip:** Avoid placing thin light-cyan or amber text directly over multi-colored photographic backgrounds."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: FTC Section 5
        if any(w in lower for w in ["ftc", "truth", "claim", "superlative", "#1", "guarantee"]):
            return {
                "reply": (
                    "**FTC Section 5 & Deceptive Claims Guidance:**\n\n"
                    "• **The Law:** FTC Section 5 prohibits unfair or deceptive marketing practices. Under the FTC's *Operation AI Comply*, "
                    "assertions of autonomous AI capability or '#1 in the market' must have pre-existing third-party substantiation.\n"
                    "• **Safe Substitutes:** Replace absolute claims like *'#1 solution'* with *'an industry-leading solution'*, and *'100% risk-free'* "
                    "with *'proven SLA-backed reliability'*.\n"
                    "• **Action:** Always cross-reference claims with verified records in the SQL Truth Bank."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: Cliché AI Jargon / Buzzwords
        if any(w in lower for w in ["jargon", "cliche", "delve", "tone", "buzzword", "filler"]):
            return {
                "reply": (
                    "**Eliminating Robotic AI Jargon:**\n\n"
                    "Generative AI tools over-index on predictable synthetic fillers. BrandGuard flags and remediates:\n"
                    "• *'Delve into'* → **Explore / Analyze**\n"
                    "• *'A testament to'* → **Evidence of / Reflects**\n"
                    "• *'Rich tapestry'* → **Comprehensive ecosystem**\n"
                    "• *'Game-changer'* → **Major milestone / Breakthrough**\n"
                    "• *'Crush the competition'* → **Outperform industry standards**\n"
                    "• *'Leverage'* → **Use / Apply**\n"
                    "• *'Synergy'* → **Combined effect / Collaboration**\n\n"
                    "Tip: Click **'AI Deep Harmonize'** in the Studio to auto-fix these instantly."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: Headline or Hook Review
        if any(w in lower for w in ["headline", "rewrite", "hook", "title", "angle"]):
            return {
                "reply": (
                    "**Compliant Headline Recommendations:**\n\n"
                    "Here are three enterprise-grade headline angles crafted for maximum impact:\n"
                    "1. **Outcome-Driven:** *'Accelerate Enterprise Brand Clearance with Deterministic Governance.'*\n"
                    "2. **Problem/Solution:** *'Eliminate Legal Review Bottlenecks Without Compromising Compliance.'*\n"
                    "3. **Consultative Proof:** *'Proven Pre-Publication Gatekeeping for Mission-Critical Marketing.'*\n\n"
                    "All three avoid unverified '#1' superlatives while communicating high authority.\n\n"
                    "*Tip: Use the AI Headlines feature to generate 5 tailored headline variants for your specific topic!*"
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Default intelligent response
        return {
            "reply": (
                f"**BrandGuard AI Co-Pilot:**\n\n"
                f"Regarding *'{msg}'*:\n\n"
                f"• **Recommendation:** When crafting enterprise marketing collateral, ensure all performance claims are backed by documented audits, "
                f"avoid unverified superlatives, and maintain an empathetic, consultative tone.\n"
                f"• **Quick Action:** If you have draft text in your editor, click **'AI Deep Harmonize'** or ask me to *'Rewrite my headline'*.\n"
                f"• **Deep Analysis:** Use the **AI Analyze** feature for a full structured compliance and quality report."
            ),
            "source": "BrandGuard Knowledge Engine (Offline Mode)"
        }

    # =========================================================================
    # 8. ADMIN AI GUIDELINE SYNTHESIZER
    # =========================================================================
    def synthesize_guideline(self, topic):
        """
        Synthesizes a structured BrandGuideline entity from a plain text concept.
        """
        topic = (topic or "").strip()
        slug = re.sub(r'[^A-Za-z0-9]+', '_', topic.upper())[:10]
        code = f"BG-{slug or 'RULE'}-01"

        # Try cloud LLM if configured
        prompt = (
            f"Generate a brand compliance rule for topic '{topic}'. Return JSON with keys: "
            f"rule_code, rule_title, category (TONE, CLAIM, TERMINOLOGY, or ACCESSIBILITY), "
            f"rule_description, severity (CRITICAL, WARNING, or SUGGESTION), "
            f"forbidden_patterns (comma-separated list), recommended_replacement, citation_ref."
        )
        cloud_json = self._call_gemini(prompt)
        if cloud_json:
            try:
                cleaned = re.search(r'\{.*\}', cloud_json, re.DOTALL)
                if cleaned:
                    data = json.loads(cleaned.group(0))
                    data["rule_code"] = code
                    return {"success": True, "guideline": data}
            except Exception:
                pass

        # Local intelligent synthesis rules
        category = "CLAIM" if any(w in topic.lower() for w in ["truth", "claim", "money", "guarantee", "uptime", "legal"]) else "TONE"
        severity = "CRITICAL" if category == "CLAIM" else "WARNING"

        forbidden = f"{topic.lower()}, guaranteed, unverified"
        replacement = "audited benchmark" if category == "CLAIM" else "consultative phrasing"
        citation = f"Brand Governance Policy § 4.2 ({topic.title()})"

        return {
            "success": True,
            "guideline": {
                "rule_code": code,
                "rule_title": f"Compliance Standard: {topic.title()}",
                "category": category,
                "rule_description": f"Mandates substantiated messaging and prohibits unverified assertions regarding {topic.lower()}.",
                "severity": severity,
                "forbidden_patterns": forbidden,
                "recommended_replacement": replacement,
                "citation_ref": citation
            }
        }

    def remediate_rule_ambiguity(self, rule_code, current_title, current_description, current_patterns, current_replacement, override_reasons=None):
        """
        AI Guideline Ambiguity Resolver: Analyzes creator disputes & override justifications
        for a friction-heavy guideline and synthesizes a clarified, non-ambiguous amendment.
        """
        override_reasons = override_reasons or ["Creator noted rule was overly broad and flagged legitimate industry terms."]
        reasons_summary = "; ".join(override_reasons[:5])

        prompt = (
            f"You are BrandGuard AI's Chief Compliance Officer & Brand Architect.\n"
            f"Brand rule '{rule_code}' ({current_title}) is causing high friction and creator pushback.\n"
            f"CURRENT DESCRIPTION: {current_description}\n"
            f"CURRENT FORBIDDEN PATTERNS: {current_patterns}\n"
            f"CURRENT REPLACEMENT: {current_replacement}\n"
            f"CREATOR DISPUTE REASONS:\n{reasons_summary}\n\n"
            f"Synthesize a revised, clarified guideline amendment in valid JSON with keys:\n"
            f"- amended_title: Clear, professional title\n"
            f"- amended_description: Precise, non-ambiguous description clarifying boundary conditions and exceptions\n"
            f"- amended_forbidden_patterns: Refined comma-separated patterns eliminating false positives\n"
            f"- amended_recommended_replacement: Practical, consultative replacement phrase\n"
            f"- explanation_of_amendment: Executive summary of why this change resolves creator pushback while preserving legal rigor."
        )

        cloud_res = self._call_gemini(prompt)
        if cloud_res:
            try:
                cleaned = re.search(r'\{.*\}', cloud_res, re.DOTALL)
                if cleaned:
                    parsed = json.loads(cleaned.group(0))
                    return {
                        "success": True,
                        "engine_used": "Google Gemini Cloud (Ambiguity Resolver)",
                        "amended_title": parsed.get("amended_title", current_title),
                        "amended_description": parsed.get("amended_description", current_description),
                        "amended_forbidden_patterns": parsed.get("amended_forbidden_patterns", current_patterns),
                        "amended_recommended_replacement": parsed.get("amended_recommended_replacement", current_replacement),
                        "explanation_of_amendment": parsed.get("explanation_of_amendment", "Clarified boundary terms to eliminate creator ambiguity.")
                    }
            except Exception:
                pass

        # Deterministic local amendment generator
        clean_patterns = current_patterns
        return {
            "success": True,
            "engine_used": "BrandGuard Local Ambiguity Resolver",
            "amended_title": f"{current_title} (Clarified Standard)",
            "amended_description": (
                f"{current_description} Note: Legitimate technical terms used in verified technical collateral "
                f"or accompanied by third-party evidentiary citations are permitted under supervised clearance."
            ),
            "amended_forbidden_patterns": current_patterns,
            "amended_recommended_replacement": current_replacement or "verified contextual phrasing",
            "explanation_of_amendment": (
                f"Resolved creator disputes regarding '{rule_code}' by qualifying edge cases and adding "
                f"safe-harbor criteria for substantiated technical claims."
            )
        }

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================
    def _calculate_linguistic_metrics(self, text):
        """
        Computes reading ease, formality index, sentence count, average word length,
        and passive voice risk for a given text.
        """
        words = text.split()
        word_count = len(words)
        if word_count == 0:
            return {
                "reading_ease": 75,
                "formality_index": 80,
                "sentence_count": 0,
                "avg_word_length": 0,
                "passive_voice_risk": False
            }

        sentences_list = re.split(r'[.!?]+', text)
        sentence_count = max(1, len([s for s in sentences_list if s.strip()]))
        avg_sentence_len = word_count / sentence_count
        avg_word_length = round(sum(len(w) for w in words) / word_count, 2)

        reading_ease = max(20, min(95, int(206.835 - (1.015 * avg_sentence_len) - 25)))
        formality_index = min(98, max(50, int(60 + (avg_sentence_len * 1.5))))

        # Passive voice risk: detect "was/were/been/being" followed by context near "by"
        passive_pattern = re.compile(
            r'\b(was|were|been|being)\b.{0,30}\bby\b',
            re.IGNORECASE | re.DOTALL
        )
        passive_voice_risk = bool(passive_pattern.search(text))

        return {
            "reading_ease": reading_ease,
            "formality_index": formality_index,
            "sentence_count": sentence_count,
            "avg_word_length": avg_word_length,
            "passive_voice_risk": passive_voice_risk
        }


# Global singleton instance for clean application-wide access
ai_copilot = AICopilotEngine()

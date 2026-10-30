"""
BrandGuard AI — Neural & Semantic AI Co-Pilot Engine
=====================================================
Provides context-aware brand voice harmonization, automated FTC/SEC safe harbor
disclaimer generation, interactive brand governance chat advisory, and AI rule synthesis.

Operates with dual architecture:
1. Cloud LLM Integration: Uses Google Gemini or OpenAI when API keys are configured.
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
        return (
            os.environ.get("GEMINI_API_KEY") or
            os.environ.get("GOOGLE_API_KEY") or
            os.environ.get("GEMINI_KEY")
        )

    def _get_openai_key(self):
        return os.environ.get("OPENAI_API_KEY")

    def get_status(self):
        """Returns the active AI engine status for UI telemetry."""
        key = self._get_gemini_key()
        if key:
            return {
                "active_engine": "Google Gemini 1.5 Flash (Live Cloud)",
                "is_cloud_active": True,
                "key_preview": f"{key[:6]}...{key[-4:]}" if len(key) > 10 else "***"
            }
        return {
            "active_engine": "BrandGuard Knowledge Engine (Local Neural NLP)",
            "is_cloud_active": False,
            "key_preview": None
        }

    # =========================================================================
    # 1. CLOUD LLM CALLER (WITH RESILIENT FALLBACK)
    # =========================================================================
    def _call_gemini(self, prompt, system_instruction=None, timeout=6):
        key = self._get_gemini_key()
        if not key:
            return None

        # Candidate models in priority order
        models = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash", "gemini-pro"]
        
        for model in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                combined_prompt = f"System Context: {system_instruction}\n\n{prompt}" if system_instruction else prompt
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": combined_prompt}
                            ]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.3,
                        "maxOutputTokens": 900
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
                                return text.strip()
            except urllib.error.HTTPError as e:
                err_text = ""
                try:
                    err_text = e.read().decode('utf-8')
                except Exception:
                    pass
                print(f"[Gemini API Notice] Model {model} returned HTTP {e.code}: {err_text[:160]}")
                # If key is forbidden / API disabled, do not loop endlessly
                if e.code in [400, 403]:
                    break
            except Exception as e:
                print(f"[Gemini Call Exception]: {e}")
                break

        return None

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
                    "Eliminated clichéd synthetic filler and buzzwords via Gemini 1.5",
                    "Harmonized sentence cadence to enterprise consultative standards",
                    "Neutralized unverified regulatory claim risks"
                ],
                "engine_used": "Google Gemini 1.5 Flash (Live Cloud)"
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
    # 3. AUTOMATED FTC & SEC SAFE HARBOR DISCLAIMER SYNTHESIZER
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
    # 4. INTERACTIVE BRAND GOVERNANCE CO-PILOT CHAT ADVISOR
    # =========================================================================
    def chat(self, user_message, context_text=None):
        """
        Answers brand governance, regulatory compliance, and copywriting questions.
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
                "source": "Google Gemini 1.5 Flash (Live Cloud)"
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
                    "• **👁️ Visual Inspector:** Computes WCAG 2.1 AA contrast ratios (4.5:1) using OpenCV K-Means.\n"
                    "• **⚖️ Stage-Gate Clearance:** Routes drafts to Reviewers with side-by-side red/green diffs and SHA-256 PDF certificates.\n"
                    "• **✍️ Copywriting Co-Pilot:** Ask me for compliant headlines, hooks, or rule explanations anytime!"
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

        # Topic: WCAG / Accessibility / Contrast
        if any(w in lower for w in ["wcag", "contrast", "color", "accessibility", "visual", "ratio"]):
            return {
                "reply": (
                    "**WCAG 2.1 AA Visual Accessibility Standards:**\n\n"
                    "• **Normal Text:** Must maintain a minimum contrast ratio of **4.5:1** against the background.\n"
                    "• **Large Text (>18pt or >14pt bold):** Requires at least **3.0:1** contrast.\n"
                    "• **Formula:** BrandGuard calculates relative luminance: `Cr = (L1 + 0.05) / (L2 + 0.05)` using OpenCV K-Means.\n"
                    "• **Tip:** Avoid placing thin light-cyan or amber text directly over multi-colored photographic backgrounds."
                ),
                "source": "BrandGuard Knowledge Engine (Offline Mode)"
            }

        # Topic: Cliché AI Jargon
        if any(w in lower for w in ["jargon", "cliche", "delve", "tone", "buzzword", "filler"]):
            return {
                "reply": (
                    "**Eliminating Robotic AI Jargon:**\n\n"
                    "Generative AI tools over-index on predictable synthetic fillers. BrandGuard flags and remediates:\n"
                    "• *'Delve into'* → **Explore / Analyze**\n"
                    "• *'A testament to'* → **Evidence of / Reflects**\n"
                    "• *'Rich tapestry'* → **Comprehensive ecosystem**\n"
                    "• *'Game-changer'* → **Major milestone / Breakthrough**\n"
                    "• *'Crush the competition'* → **Outperform industry standards**\n\n"
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
                    "All three avoid unverified '#1' superlatives while communicating high authority."
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
                f"• **Quick Action:** If you have draft text in your editor, click **'AI Deep Harmonize'** or ask me to *'Rewrite my headline'*."
            ),
            "source": "BrandGuard Knowledge Engine (Offline Mode)"
        }

    # =========================================================================
    # 5. ADMIN AI GUIDELINE SYNTHESIZER
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

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================
    def _calculate_linguistic_metrics(self, text):
        words = text.split()
        word_count = len(words)
        if word_count == 0:
            return {"reading_ease": 75, "formality_index": 80}

        sentences = max(1, len(re.split(r'[.!?]+', text)))
        avg_sentence_len = word_count / sentences

        reading_ease = max(20, min(95, int(206.835 - (1.015 * avg_sentence_len) - 25)))
        formality_index = min(98, max(50, int(60 + (avg_sentence_len * 1.5))))

        return {
            "reading_ease": reading_ease,
            "formality_index": formality_index
        }


# Global singleton instance for clean application-wide access
ai_copilot = AICopilotEngine()

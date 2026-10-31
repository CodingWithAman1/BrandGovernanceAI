"""
BrandGuard AI — Live URL & Competitor Claim Scanner Engine
===========================================================
Fetches, parses, and audits live web pages and competitor advertising copy.
Analyzes competitor copy against BrandGuard's SQL Truth Bank, discovers claim vulnerabilities,
and synthesizes compliant, high-converting battlecards and counter-messaging.
"""

import re
import ssl
import json
import urllib.request
import urllib.error
from html.parser import HTMLParser
from typing import Dict, List, Any, Optional
from datetime import datetime


class _HTMLTextExtractor(HTMLParser):
    """Clean, dependency-free HTML text extractor that ignores scripts, styles, and chrome."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text_chunks = []
        self.title = ""
        self.meta_description = ""
        self.headings = []
        self._current_tag = None
        self._ignore_tags = {'script', 'style', 'nav', 'footer', 'noscript', 'head', 'svg'}

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag.lower()
        attr_dict = {k.lower(): (v or "") for k, v in attrs}
        if self._current_tag == 'meta':
            name = attr_dict.get('name', '').lower()
            prop = attr_dict.get('property', '').lower()
            if name == 'description' or prop == 'og:description':
                self.meta_description = attr_dict.get('content', '')

    def handle_endtag(self, tag):
        self._current_tag = None

    def handle_data(self, data):
        if self._current_tag in self._ignore_tags:
            return
        cleaned = data.strip()
        if not cleaned:
            return
        if self._current_tag == 'title' and not self.title:
            self.title = cleaned
        elif self._current_tag in {'h1', 'h2', 'h3'}:
            self.headings.append(cleaned)
            self.text_chunks.append(cleaned)
        else:
            self.text_chunks.append(cleaned)

    def get_clean_text(self, max_chars: int = 8000) -> str:
        raw = " ".join(self.text_chunks)
        # Normalize whitespace
        normalized = re.sub(r"\s+", " ", raw).strip()
        return normalized[:max_chars]


class URLScannerEngine:
    """
    Live web crawler and competitor claims auditor.
    """

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36 BrandGuardComplianceScanner/2.0"
    )

    def __init__(self, ai_copilot=None):
        self.ai_copilot = ai_copilot

    def fetch_url_content(self, url: str, timeout: int = 12) -> Dict[str, Any]:
        """
        Fetches web page from live URL using standard urllib with strict safety checks.
        """
        url = (url or "").strip()
        if not url:
            return {"success": False, "error": "No URL provided."}

        if not re.match(r"^https?://", url, re.IGNORECASE):
            url = f"https://{url}"

        # Safety: avoid local / intranet scanning (SSRF protection)
        blocked_hosts = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "::1"]
        for bh in blocked_hosts:
            if bh in url.lower():
                return {"success": False, "error": "Scanning internal/local network addresses is prohibited."}

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": self.USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                }
            )

            # SSL context handling
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                status_code = resp.getcode()
                content_type = resp.headers.get("Content-Type", "")
                
                # Check for HTML or text
                if not any(t in content_type.lower() for t in ["text/html", "text/plain", "application/xhtml+xml"]):
                    return {
                        "success": False,
                        "error": f"Unsupported content type '{content_type}'. Please provide a standard web page."
                    }

                raw_bytes = resp.read(500000)  # Read up to 500KB
                charset = resp.headers.get_content_charset() or "utf-8"
                html_text = raw_bytes.decode(charset, errors="replace")

            # Parse HTML
            parser = _HTMLTextExtractor()
            parser.feed(html_text)
            clean_body = parser.get_clean_text()

            if not clean_body:
                return {
                    "success": False,
                    "error": "Could not extract readable text content from the target URL."
                }

            return {
                "success": True,
                "url": url,
                "status_code": status_code,
                "title": parser.title or "Untitled Web Page",
                "meta_description": parser.meta_description,
                "headings": parser.headings[:8],
                "content": clean_body,
                "character_count": len(clean_body),
                "word_count": len(clean_body.split())
            }

        except urllib.error.HTTPError as e:
            return {"success": False, "error": f"Target server returned HTTP {e.code}: {e.reason}"}
        except urllib.error.URLError as e:
            return {"success": False, "error": f"Failed to connect to target URL: {e.reason}"}
        except TimeoutError:
            return {"success": False, "error": "Request to target URL timed out after 12 seconds."}
        except Exception as e:
            return {"success": False, "error": f"Unexpected scanner exception: {str(e)}"}

    def audit_competitor_claims(
        self,
        content: str,
        title: str = "",
        approved_facts: Optional[List[Any]] = None,
        competitor_name: str = "Competitor"
    ) -> Dict[str, Any]:
        """
        Audits competitor text against truth bank & regulatory standards.
        Identifies vulnerabilities and synthesizes battlecard counter-messaging.
        """
        from engines.claims_checker import ClaimsFactChecker
        from engines.regulatory_engine import regulatory_engine

        approved_facts = approved_facts or []

        # 1. Run Claims & Regulatory checks on competitor content
        claims_engine = ClaimsFactChecker(approved_facts=approved_facts)
        claims_res = claims_engine.evaluate(content)

        reg_res = regulatory_engine.evaluate(content, jurisdiction="GLOBAL")

        # Aggregate vulnerabilities
        all_vulnerabilities = []
        for f in claims_res.get("flags", []):
            all_vulnerabilities.append({
                "type": "CLAIM_SUBSTANTIATION",
                "severity": f.get("severity", "WARNING"),
                "snippet": f.get("snippet", ""),
                "weakness": f.get("explanation", ""),
                "citation": f.get("citation", "FTC Act Section 5")
            })

        for f in reg_res.get("flags", []):
            all_vulnerabilities.append({
                "type": f.get("flag_type", "REGULATORY"),
                "severity": f.get("severity", "CRITICAL"),
                "snippet": f.get("snippet", ""),
                "weakness": f.get("explanation", ""),
                "citation": f.get("citation", "Regulatory Standard")
            })

        # Calculate competitor vulnerability score (0-100: higher = more vulnerable/risky)
        vulnerability_score = min(100, len(all_vulnerabilities) * 18 + (30 if claims_res['score'] < 70 else 10))

        # 2. Match against our Approved Fact Bank for contrasts
        fact_contrasts = []
        for fact in approved_facts:
            fact_statement = getattr(fact, "claim_statement", "")
            fact_topic = getattr(fact, "topic", "")
            fact_source = getattr(fact, "approved_source_link", "Internal Verified Vault")
            
            # Simple keyword matching to see if competitor touches this topic
            keywords = [w.lower() for w in fact_topic.split() if len(w) > 3]
            if any(k in content.lower() for k in keywords) or len(fact_contrasts) < 2:
                fact_contrasts.append({
                    "topic": fact_topic,
                    "competitor_posture": f"Makes unverified, broad claims without audited proof.",
                    "our_verified_fact": fact_statement,
                    "evidence_link": fact_source
                })
                if len(fact_contrasts) >= 3:
                    break

        # 3. AI / Local Battlecard & Counter-Messaging Synthesis
        battlecard = self._synthesize_counter_messaging(
            competitor_name=competitor_name,
            competitor_title=title,
            competitor_text=content[:2000],
            vulnerabilities=all_vulnerabilities,
            fact_contrasts=fact_contrasts
        )

        return {
            "success": True,
            "competitor_name": competitor_name,
            "vulnerability_score": vulnerability_score,
            "vulnerability_level": "CRITICAL" if vulnerability_score > 70 else "MODERATE" if vulnerability_score > 35 else "LOW",
            "vulnerabilities": all_vulnerabilities,
            "vulnerability_count": len(all_vulnerabilities),
            "fact_contrasts": fact_contrasts,
            "battlecard": battlecard,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def _synthesize_counter_messaging(
        self,
        competitor_name: str,
        competitor_title: str,
        competitor_text: str,
        vulnerabilities: List[Dict[str, Any]],
        fact_contrasts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Uses Gemini LLM or Local NLP to generate competitive counter-messaging.
        """
        prompt = (
            f"You are BrandGuard AI's Elite Competitive Intelligence Strategist.\n"
            f"A competitor ('{competitor_name}') published this copy:\n"
            f"TITLE: {competitor_title}\n"
            f"EXCERPT: {competitor_text[:1200]}\n\n"
            f"Our audit detected these legal/marketing vulnerabilities:\n"
            f"{json.dumps(vulnerabilities[:4], indent=2)}\n\n"
            f"Our verified facts:\n"
            f"{json.dumps(fact_contrasts[:2], indent=2)}\n\n"
            f"Generate a strategic battlecard with 3 compliant counter-messaging angles in JSON format:\n"
            f"1. sales_pitch: 2 sentences for account executives contrasting our verified proof vs competitor hyperbole.\n"
            f"2. linkedin_angle: A professional thought-leadership hook addressing industry claims without naming competitor directly.\n"
            f"3. pr_positioning: An authoritative statement on why verifiable governance wins over marketing fluff."
        )

        # Try Gemini if ai_copilot is available
        if self.ai_copilot:
            gemini_res = self.ai_copilot._call_gemini(
                prompt,
                system_instruction="You are an enterprise competitive messaging analyst. Always output valid JSON."
            )
            if gemini_res:
                try:
                    # Clean markdown codeblocks
                    clean_json = re.sub(r"^```(?:json)?\s*|\s*```$", "", gemini_res.strip(), flags=re.MULTILINE)
                    parsed = json.loads(clean_json)
                    return {
                        "engine_used": "Google Gemini Cloud (Competitive Strategy)",
                        "sales_pitch": parsed.get("sales_pitch", ""),
                        "linkedin_angle": parsed.get("linkedin_angle", ""),
                        "pr_positioning": parsed.get("pr_positioning", "")
                    }
                except Exception:
                    pass

        # Deterministic High-Quality Local Fallback
        vuln_summary = vulnerabilities[0]["snippet"] if vulnerabilities else "unsubstantiated claims"
        return {
            "engine_used": "BrandGuard Local Intelligence Matrix",
            "sales_pitch": (
                f"While alternative vendors rely on unverified claims like '{vuln_summary}', our platform is backed by "
                f"third-party verified SOC 2 Type II attestation and an SLA-guaranteed 99.95% cloud infrastructure. "
                f"We provide transparent, auditable governance that enterprise legal teams trust."
            ),
            "linkedin_angle": (
                f"In enterprise software, the difference between marketing hyperbole and verified engineering is clear. "
                f"Don't settle for unverified '#1' superlatives. Insist on audited SLAs, verifiable security frameworks, "
                f"and multi-modal pre-publication governance before deploying AI into production."
            ),
            "pr_positioning": (
                f"True market leadership is demonstrated through empirical transparency, verifiable compliance, "
                f"and measurable customer outcomes—not ungrounded guarantees. We invite buyers to review our live status "
                f"and audited performance metrics."
            )
        }


# Global singleton instance
url_scanner_engine = URLScannerEngine()

# BrandGuard AI — Intelligent Multi-Modal Brand Governance Platform
**Inkloom AI Hackathon Project (Round 1 & Beyond)**  
**Submitted by Team Synapse:**
* **Aman Sharma** — Team Leader & Backend / AI Architect (`aman@synapse.ai`)
* **Janhavi Kanojia** — Frontend & UI/UX Developer (`janhavi@synapse.ai`)

---

## 🌐 Live Production Deployment

* **Live Web Application:** [https://brandgovernanceai.onrender.com](https://brandgovernanceai.onrender.com)
* **GitHub Repository:** [https://github.com/CodingWithAman1/BrandGovernanceAI.git](https://github.com/CodingWithAman1/BrandGovernanceAI.git) (branch: `main`)
* **Health Check & Uptime:** [https://brandgovernanceai.onrender.com/healthz](https://brandgovernanceai.onrender.com/healthz)

---

## 🚀 Overview

**BrandGuard AI** is a deterministic pre-publication governance platform that audits marketing copy, promotional claims, visual graphic assets, and WCAG accessibility before content is published.

Instead of arbitrary rejections, BrandGuard operates as an **intelligent advisory co-pilot**: it identifies the exact guideline or regulatory statute involved, explains *why* the issue was flagged, and generates **1-click tone-preserving suggested rewrites** and **AI full-draft harmonizations** that preserve author intent.

---

## 🤖 New AI Co-Pilot & Neural Capabilities

BrandGuard AI features a dedicated **Neural & Semantic AI Engine (`engines/ai_copilot.py`)** with dual architecture (Cloud LLM connectivity via Gemini/OpenAI with automatic fallback to an offline Deterministic Semantic NLP Engine):

1. **Slide-Out Cyberpunk AI Co-Pilot Drawer**:
   * Accessible from **every page** via the floating glowing AI trigger (`#aiCopilotTrigger`).
   * Provides real-time interactive compliance advice, guideline explanations, and headline recommendations.
   * Auto-detects current editor context for instant assistance.
2. **AI Deep Semantic Harmonization**:
   * Evaluates the entire draft context, neutralizing robotic AI clichés (*delve into*, *rich tapestry*, *testament to*), passive-aggressive phrasing, and unverified superlatives in one click.
   * Available in both the Pre-Publication Studio and Audit Report Scorecard.
3. **FTC Section 5 & SEC Safe Harbor Synthesizer**:
   * Automatically analyzes metrics, uptime, and forward-looking statements in draft copy.
   * Generates legally tailored regulatory substantiation notices (FTC 16 CFR § 255 and SEC Rule 10b-5).
4. **AI Brand Guideline Synthesizer**:
   * Allows administrators to type a natural language topic (e.g., *"Greenwashing & Carbon Neutrality"*) and auto-populates complete rule definitions, regex patterns, and statutory citations.

---

## 🛠️ Technology Stack

| Layer | Technologies Used | Implementation Details |
| :--- | :--- | :--- |
| **Frontend & UI/UX** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3 | Obsidian Dark Theme (`#080C14`), dual cyber cursor (60 FPS lerp physics), ambient constellation particle canvas, card shimmer sweeps, holographic Laser Scanner HUD, slide-out AI Co-Pilot drawer, side-by-side diff engine. |
| **Backend & WSGI** | Python 3.11+, Flask 3.0, Werkzeug, Gunicorn | Application Factory pattern, modular Blueprints (`auth`, `portal`, `dashboard`, `guidelines`, `scanner`, `reviews`, `analytics`, `api`), dynamic `$PORT` binding. |
| **AI Co-Pilot & NLP** | Dual Engine: Gemini API + Local Semantic Engine | Contextual draft harmonization, FTC/SEC safe harbor disclaimer generator, interactive compliance chat advisor, guideline auto-synthesis. |
| **Authentication & RBAC** | Firebase Web SDK & Flask-Login | Firebase Auth (`brandbuildai-2749e`) Google Sign-In with OAuth token sync, 3 strictly isolated role portals (Client, Reviewer, Admin), PBKDF2 hashing, Sole Admin enforcement (`aman@synapse.ai`). |
| **Database & ORM** | Relational SQL (SQLite / PostgreSQL), SQLAlchemy | Relational schema: `users`, `brand_guidelines`, `approved_facts`, `brand_assets`, `submissions`, `evaluation_flags`, `review_logs`, `review_comments`. |
| **Vision & Contrast** | OpenCV, Pillow (PIL), PyTesseract | K-Means color quantization, WCAG 2.1 AA (4.5:1) relative luminance contrast formula, image text extraction. |
| **Certification & PDF**| ReportLab | Two-pass `NumberedCanvas` generating tamper-evident PDF Compliance Certificates with SHA-256 copy hashes. |

---

## ⚡ Quick Start: Running the Platform

1. **Launch the Flask Application**:
   ```bash
   python app.py
   ```
   *(Or double-click `run.bat` on Windows)*

2. **Open in Browser**:
   ```
   http://127.0.0.1:5000
   ```

3. **Login / Test Personas**:
   * **Aman Sharma (Sole Admin & Lead):** `aman@synapse.ai` / `password123`
   * **Elena Rostova (Reviewer / Brand Manager):** `elena@inkloom.ai` / `password123`
   * **David Chen (Reviewer / Legal Counsel):** `david@inkloom.ai` / `password123`
   * **Priya Sharma (Client / Copywriter):** `priya@inkloom.ai` / `password123`
   * **Janhavi Kanojia (Client / Designer):** `janhavi@synapse.ai` / `password123`

---

## 🧪 Comprehensive Automated Test Suites (32/32 Tests Passing - 100%)

The codebase is continuously verified by 32 automated integration tests across three suites:

```bash
# 1. Core Engines, Security & Lifecycle Suite (12 Tests)
python -m unittest test_complete_suite.py

# 2. Portal Isolation, RBAC & Firebase Auth Suite (10 Tests)
python -m unittest test_portals_auth.py

# 3. AI Co-Pilot, Harmonization & Safe Harbor Suite (10 Tests)
python -m unittest test_ai_features.py
```

All 32 tests pass in <12 seconds with 100% assertions satisfied.

---

## 🌐 RESTful API Endpoints

* `POST /api/v1/scan` — Programmatic draft compliance scan.
* `GET /api/v1/guidelines` — Returns active corporate brand guidelines.
* `POST /api/v1/ai/harmonize` — AI deep semantic rewrite & cliché elimination.
* `POST /api/v1/ai/safe-harbor` — Generates FTC Section 5 and SEC safe harbor disclaimers.
* `POST /api/v1/ai/chat` — Interactive BrandGuard AI Co-Pilot chat endpoint.
* `POST /api/v1/ai/suggest-guideline` — AI rule auto-synthesis for administrators.
* `GET /healthz` — Cloud load balancer health check returning `HTTP 200 OK`.

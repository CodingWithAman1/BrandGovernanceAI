# BrandGuard AI — Intelligent Multi-Modal Brand Governance Platform
**Inkloom AI Hackathon Project**  
**Submitted by Team Synapse:**
* **Aman Sharma** — Team Leader & Backend / AI Architect
* **Janhavi Kanojia** — Frontend & UI/UX Developer

---

## 🚀 Overview

**BrandGuard AI** is an automated pre-publication governance platform that audits marketing copy, promotional claims, visual graphic assets, and WCAG accessibility before content is published. 

Instead of arbitrary rejections, BrandGuard operates as an **advisory co-pilot**: it identifies the exact guideline or regulatory statute involved, explains *why* the issue was flagged, and generates **1-click tone-preserving suggested rewrites** that preserve author intent.

---

## 🛠️ Technology Stack

| Layer | Technologies Used | Implementation Details |
| :--- | :--- | :--- |
| **Frontend & UI/UX** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3 | Obsidian Dark Theme (`#080C14`), dual cyber cursor (lerp physics & magnetic glow), ambient constellation canvas, card shimmer sweeps, holographic Laser Scanner HUD, side-by-side diff engine. |
| **Backend & WSGI** | Python 3.11+, Flask 3.0, Werkzeug | Modular Flask Blueprints (`auth`, `portal`, `dashboard`, `guidelines`, `scanner`, `reviews`, `analytics`, `api`), secure routing, RESTful JSON API endpoints. |
| **Authentication & RBAC** | Firebase Web SDK & Flask-Login | Firebase Auth (`brandbuildai-2749e`) Google Sign-In, 3 strictly isolated role portals (Client, Reviewer, Admin), PBKDF2 hashing, Sole Admin enforcement (`aman@synapse.ai`). |
| **Database & ORM** | Relational SQL (SQLite / PostgreSQL), SQLAlchemy | Fully modeled relational schema: `users`, `brand_guidelines`, `approved_facts`, `brand_assets`, `submissions`, `evaluation_flags`, `review_logs`, `review_comments`. |
| **AI & Vision Engines** | OpenCV, Pillow (PIL), PyTesseract, LLM Schemas | K-Means color clustering, WCAG 2.1 AA (4.5:1) relative luminance contrast formula, image text extraction, BM25 & semantic claims matching against SQL Truth Bank. |
| **Certification & PDF**| ReportLab | Automated cryptographic Compliance Certificate generation with SHA-256 content verification upon stage-gate approval. |

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
   The database automatically self-seeds with realistic brand rules, verified claim banks, and 5 demo personas. You can log in using any of the following accounts or use the **1-Click Role Switcher** in the top navigation bar:
   * **Priya Sharma (Creator / Copywriter):** `priya@inkloom.ai` / `password123`
   * **Marcus Vance (Designer):** `marcus@inkloom.ai` / `password123`
   * **Elena Rostova (Brand Manager):** `elena@inkloom.ai` / `password123`
   * **David Chen (Legal Counsel):** `david@inkloom.ai` / `password123`
   * **Aman Sharma (Admin / Leader):** `aman@synapse.ai` / `password123`

---

## 🔍 Key Feature Walkthrough

### 1. Pre-Publish Studio (`/scanner/studio`)
* **Multi-Modal Input:** Submit marketing copy or upload graphic banners (`.png`, `.jpg`, `.pdf`).
* **Test Case Presets:** Click *"Load Test Sample Preset"* to instantly populate:
  * *Sample 1 (Risky Ad):* Contains unverified `#1` claims, FTC Section 5 risks, and AI buzzwords.
  * *Sample 2 (Deprecated Jargon):* Contains competitor slurs and forbidden legacy naming.
  * *Sample 3 (Compliant Whitepaper):* Passes with verified facts and active SOC 2 citations.

### 2. Multi-Engine Evaluation & 1-Click Remediator (`/scanner/report/<id>`)
* **Brand Health Score Ring:** Dynamic 0–100 score with sub-scores for Tone, Claims, and Visuals.
* **Granular Citations:** Displays exact rule codes (e.g. `BG-CLAIM-01`, `Brand Voice Guide § 2.1`) and legal rationale.
* **1-Click "Accept Fix":** Dynamically replaces flagged copy in real-time without homogenizing author intent.
* **Side-by-Side Red/Green Diff View:** Live visual comparison between initial draft and remediated copy.

### 3. Stage-Gate Review Queue (`/reviews/queue`)
* Role-based review queue for Managers (Elena) and Legal Officers (David).
* Features threaded comments, revision logs, and action controls:
  * `Approve & Issue Certificate`
  * `Request Changes with Feedback`
  * `Reject Draft`

### 4. Official PDF Compliance Certificate (`/reviews/certificate/<id>`)
* Generated via ReportLab upon stage-gate approval.
* Features a unique verification hash, timestamp, reviewer signature, and score breakdown.

### 5. Guideline Clarity Index (`/analytics`)
* Analyzes creator dispute rates and manual overrides.
* Provides the brand leadership team with a **Friction Heatmap** identifying ambiguous or outdated guidelines.

---

## 🌐 RESTful API Endpoints

* `POST /api/v1/scan`
  * Payload: `{"text": "Your draft content here..."}`
  * Returns: Evaluated flags, overall score, tone score, claim score, and 1-click suggested fixes.
* `GET /api/v1/guidelines`
  * Returns active corporate brand guidelines and severity ratings.

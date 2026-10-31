from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth/Firebase users
    role = db.Column(db.String(30), default='CREATOR')  # CREATOR (Client), REVIEWER (Reviewer/Manager), ADMIN (Sole Admin)
    department = db.Column(db.String(80), default='Marketing')
    organization = db.Column(db.String(100), default='Inkloom AI')
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='creator', lazy=True, foreign_keys='Submission.creator_id')
    review_logs = db.relationship('ReviewLog', backref='actor', lazy=True)
    comments = db.relationship('ReviewComment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        # Strict enforcement: Aman Sharma (aman@synapse.ai) is the sole admin
        return self.role == 'ADMIN' and self.email.lower() == 'aman@synapse.ai'


class BrandGuideline(db.Model):
    __tablename__ = 'brand_guidelines'

    id = db.Column(db.Integer, primary_key=True)
    rule_code = db.Column(db.String(30), unique=True, nullable=False)  # e.g. BG-TONE-01
    category = db.Column(db.String(40), nullable=False)  # TONE, CLAIM, TERMINOLOGY, VISUAL, ACCESSIBILITY
    rule_title = db.Column(db.String(200), nullable=False)
    rule_description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='WARNING')  # CRITICAL, WARNING, SUGGESTION
    forbidden_patterns = db.Column(db.Text)  # Comma or newline-separated patterns
    recommended_replacement = db.Column(db.Text)
    citation_ref = db.Column(db.String(200))  # e.g. Brand Book Sec 3.2 / FTC Sec 5
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    flags = db.relationship('EvaluationFlag', backref='guideline', lazy=True)


class ApprovedFact(db.Model):
    __tablename__ = 'approved_facts'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), nullable=False)
    claim_statement = db.Column(db.Text, nullable=False)
    approved_source_link = db.Column(db.String(255))
    evidence_excerpt = db.Column(db.Text)
    expiration_date = db.Column(db.String(30))  # YYYY-MM-DD
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BrandAsset(db.Model):
    __tablename__ = 'brand_assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    asset_type = db.Column(db.String(40), nullable=False)  # PALETTE, LOGO, FONT, TOKEN
    asset_value = db.Column(db.String(255), nullable=False)
    metadata_json = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Submission(db.Model):
    __tablename__ = 'submissions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(40), default='TEXT')  # TEXT, IMAGE_BANNER, HYBRID
    raw_content = db.Column(db.Text)
    original_content = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(40), default='DRAFT')  # DRAFT, SCANNED, PENDING, CHANGES_REQUESTED, APPROVED, REJECTED
    
    # Scores (0-100)
    compliance_score = db.Column(db.Integer, default=100)
    tone_score = db.Column(db.Integer, default=100)
    claim_score = db.Column(db.Integer, default=100)
    visual_score = db.Column(db.Integer, default=100)
    regulatory_score = db.Column(db.Integer, default=100)
    jurisdiction = db.Column(db.String(30), default='GLOBAL')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    flags = db.relationship('EvaluationFlag', backref='submission', cascade='all, delete-orphan', lazy=True)
    logs = db.relationship('ReviewLog', backref='submission', cascade='all, delete-orphan', lazy=True)
    comments = db.relationship('ReviewComment', backref='submission', cascade='all, delete-orphan', lazy=True)


class EvaluationFlag(db.Model):
    __tablename__ = 'evaluation_flags'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    guideline_id = db.Column(db.Integer, db.ForeignKey('brand_guidelines.id'), nullable=True)
    
    flag_type = db.Column(db.String(50), nullable=False)
    flagged_snippet = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    suggested_fix = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='WARNING')
    status = db.Column(db.String(30), default='PENDING')  # PENDING, ACCEPTED, DISMISSED, OVERRIDDEN
    override_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewComment(db.Model):
    __tablename__ = 'review_comments'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewLog(db.Model):
    __tablename__ = 'review_logs'

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

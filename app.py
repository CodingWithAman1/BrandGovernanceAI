import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.portal_select'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'certificates'), exist_ok=True)

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.portal_routes import portal_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.guidelines_routes import guidelines_bp
    from routes.scanner_routes import scanner_bp
    from routes.review_routes import review_bp
    from routes.analytics_routes import analytics_bp
    from routes.api_routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(guidelines_bp)
    app.register_blueprint(scanner_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp)

    # Health check endpoint for cloud load balancers / Render health checks
    @app.route('/healthz')
    def health_check():
        return {'status': 'healthy', 'service': 'BrandGuard AI'}, 200

    # Smart root redirect based on user role
    @app.route('/')
    def root():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('portal.admin_portal'))
            elif current_user.role in ['REVIEWER', 'MANAGER']:
                return redirect(url_for('portal.reviewer_portal'))
            else:
                return redirect(url_for('portal.client_portal'))
        return redirect(url_for('auth.portal_select'))

    # Context processor to provide demo personas and Firebase config globally
    @app.context_processor
    def inject_global_data():
        try:
            demo_users = User.query.filter_by(is_active_account=True).all()
        except Exception:
            demo_users = []
        return dict(
            all_demo_users=demo_users,
            firebase_config=app.config.get('FIREBASE_CONFIG', {}),
            sole_admin_email="aman@synapse.ai"
        )

    # Auto-seed database if empty
    from seed_data import seed_database
    seed_database(app)

    return app

# Expose WSGI application at module level for Gunicorn / Render production deployments
app = create_app()

if __name__ == '__main__':
    print("=" * 65)
    print("[+] BRANDGUARD AI -- Pre-Publication Governance Platform Active")
    print("[*] Running locally on: http://localhost:5000 (Firebase Authorized Domain)")
    print("[*] Also available at: http://127.0.0.1:5000")
    print("[*] Sole Administrator: Aman Sharma (aman@synapse.ai)")
    print("=" * 65)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

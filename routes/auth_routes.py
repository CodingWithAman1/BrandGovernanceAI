import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, db

auth_bp = Blueprint('auth', __name__)

# Sole Admin Email Constant
SOLE_ADMIN_EMAIL = "aman@synapse.ai"

@auth_bp.route('/portals')
@auth_bp.route('/login')
def portal_select():
    """Universal Portal Gateway: Choose Client, Reviewer, or Admin portal."""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('portal.admin_portal'))
        elif current_user.role in ['REVIEWER', 'MANAGER']:
            return redirect(url_for('portal.reviewer_portal'))
        else:
            return redirect(url_for('portal.client_portal'))
    return render_template('auth/portal_select.html', admin_email=SOLE_ADMIN_EMAIL)


# ==================== CLIENT (CREATOR) AUTH ====================

@auth_bp.route('/client/login', methods=['GET', 'POST'])
@auth_bp.route('/auth/client/login', methods=['GET', 'POST'])
def client_login():
    if current_user.is_authenticated:
        return redirect(url_for('portal.client_portal'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome to Client Portal, {user.name}!", "success")
            return redirect(url_for('portal.client_portal'))
        else:
            flash("Invalid client email or password.", "danger")

    return render_template('auth/client_login.html')


@auth_bp.route('/client/signup', methods=['GET', 'POST'])
@auth_bp.route('/auth/client/signup', methods=['GET', 'POST'])
def client_signup():
    if current_user.is_authenticated:
        return redirect(url_for('portal.client_portal'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        organization = request.form.get('organization', 'Growth Agency').strip()
        department = request.form.get('department', 'Content Marketing').strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.client_signup'))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for('auth.client_login'))

        # Create Client user (strictly role CREATOR)
        new_client = User(
            name=name,
            email=email,
            role='CREATOR',
            department=department,
            organization=organization
        )
        new_client.set_password(password)
        db.session.add(new_client)
        db.session.commit()

        login_user(new_client)
        flash(f"Welcome to BrandGuard, {name}! Your Client Creator account is ready.", "success")
        return redirect(url_for('portal.client_portal'))

    return render_template('auth/client_signup.html')


# ==================== REVIEWER / MANAGER AUTH ====================

@auth_bp.route('/reviewer/login', methods=['GET', 'POST'])
@auth_bp.route('/auth/reviewer/login', methods=['GET', 'POST'])
def reviewer_login():
    if current_user.is_authenticated:
        return redirect(url_for('portal.reviewer_portal'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome to Reviewer Desk, {user.name}!", "success")
            return redirect(url_for('portal.reviewer_portal'))
        else:
            flash("Invalid reviewer credentials.", "danger")

    return render_template('auth/reviewer_login.html')


@auth_bp.route('/reviewer/signup', methods=['GET', 'POST'])
@auth_bp.route('/auth/reviewer/signup', methods=['GET', 'POST'])
def reviewer_signup():
    if current_user.is_authenticated:
        return redirect(url_for('portal.reviewer_portal'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        department = request.form.get('department', 'Brand Operations').strip()
        organization = request.form.get('organization', 'Inkloom AI Review Desk').strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth.reviewer_signup'))

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for('auth.reviewer_login'))

        # Reviewer role: REVIEWER (Public signup can NEVER create an ADMIN)
        new_reviewer = User(
            name=name,
            email=email,
            role='REVIEWER',
            department=department,
            organization=organization
        )
        new_reviewer.set_password(password)
        db.session.add(new_reviewer)
        db.session.commit()

        login_user(new_reviewer)
        flash(f"Welcome, {name}! Your Reviewer account has been provisioned.", "success")
        return redirect(url_for('portal.reviewer_portal'))

    return render_template('auth/reviewer_signup.html')


# ==================== ADMIN AUTH (RESTRICTED TO AMAN SHARMA) ====================

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
@auth_bp.route('/auth/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('portal.admin_portal'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Enforce Aman Sharma as the SOLE ADMIN
        if email != SOLE_ADMIN_EMAIL:
            flash("Access Denied: Only Aman Sharma (Sole Administrator) can access the Executive Admin Portal.", "danger")
            return render_template('auth/admin_login.html', admin_email=SOLE_ADMIN_EMAIL)

        admin_user = User.query.filter_by(email=SOLE_ADMIN_EMAIL).first()
        if admin_user and admin_user.check_password(password):
            login_user(admin_user)
            flash("Welcome to Executive Admin Control Plane, Aman Sharma!", "success")
            return redirect(url_for('portal.admin_portal'))
        else:
            flash("Invalid administrator password.", "danger")

    return render_template('auth/admin_login.html', admin_email=SOLE_ADMIN_EMAIL)


# ==================== FIREBASE AUTH SYNC API ====================

@auth_bp.route('/auth/api/firebase-sync', methods=['POST'])
def firebase_sync():
    """
    Receives authenticated user credentials from the Firebase Web SDK,
    provisions or retrieves the user in SQL, and establishes the Flask session.
    Protects Admin privilege: only SOLE_ADMIN_EMAIL can be ADMIN.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    name = data.get('displayName') or data.get('name') or email.split('@')[0]
    firebase_uid = data.get('uid') or data.get('firebase_uid')
    requested_portal = data.get('portal', 'client')  # 'client', 'reviewer', or 'admin'

    if not email:
        return jsonify({'success': False, 'message': 'Missing email in Firebase authentication'}), 400

    # Guard: If attempting to authenticate into Admin portal via Google, verify email is Aman Sharma
    if requested_portal == 'admin' and email != SOLE_ADMIN_EMAIL:
        return jsonify({
            'success': False,
            'message': f'Access Denied: Only Aman Sharma ({SOLE_ADMIN_EMAIL}) is permitted to access the Executive Admin Portal.'
        }), 403

    user = User.query.filter_by(email=email).first()

    if not user:
        # Determine Role
        if email == SOLE_ADMIN_EMAIL:
            assigned_role = 'ADMIN'
            department = 'Executive Leadership'
            organization = 'Team Synapse'
        elif requested_portal == 'reviewer':
            assigned_role = 'REVIEWER'
            department = 'Brand Governance'
            organization = 'Inkloom Review Desk'
        else:
            assigned_role = 'CREATOR'
            department = 'Content Marketing'
            organization = 'Growth Agency'

        user = User(
            name=name,
            email=email,
            role=assigned_role,
            department=department,
            organization=organization,
            firebase_uid=firebase_uid
        )
        user.set_password("firebase-auth-managed")
        db.session.add(user)
        db.session.commit()
    else:
        # Link Firebase UID if not yet linked
        if firebase_uid and not user.firebase_uid:
            user.firebase_uid = firebase_uid
            db.session.commit()

    # Log user in
    login_user(user)

    # Return redirect URL based on role
    redirect_target = (
        url_for('portal.admin_portal') if user.is_admin
        else url_for('portal.reviewer_portal') if user.role in ['REVIEWER', 'MANAGER']
        else url_for('portal.client_portal')
    )

    return jsonify({
        'success': True,
        'user': {
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'is_admin': user.is_admin
        },
        'redirect_url': redirect_target
    })


# ==================== QUICK SWITCH PERSONA (DEMO MODE) ====================

@auth_bp.route('/quick-switch/<int:user_id>')
def quick_switch(user_id):
    user = User.query.get_or_404(user_id)
    login_user(user)
    flash(f"Switched role to {user.name} ({user.role} - {user.department})", "info")
    
    if user.is_admin:
        return redirect(url_for('portal.admin_portal'))
    elif user.role in ['REVIEWER', 'MANAGER']:
        return redirect(url_for('portal.reviewer_portal'))
    else:
        return redirect(url_for('portal.client_portal'))


@auth_bp.route('/client/logout')
def client_logout():
    logout_user()
    flash("Signed out of Client Portal.", "info")
    return redirect(url_for('auth.client_login'))


@auth_bp.route('/reviewer/logout')
def reviewer_logout():
    logout_user()
    flash("Signed out of Reviewer Desk.", "info")
    return redirect(url_for('auth.reviewer_login'))


@auth_bp.route('/admin/logout')
def admin_logout():
    logout_user()
    flash("Signed out of Admin Control Plane.", "info")
    return redirect(url_for('auth.admin_login'))


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for('auth.portal_select'))

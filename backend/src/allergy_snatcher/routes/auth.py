from flask import Blueprint, request, url_for, session, redirect, jsonify, g, Flask, current_app
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.database import db, User, Password, OAuthAccount, UserSession
from ..models.auth import require_session
import secrets
import datetime
import os

oauth = OAuth()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    new_user = User(username=username, email=email) # pyright: ignore[reportCallIssue]
    new_password = Password(password_hash=generate_password_hash(password), user=new_user) # type: ignore
    
    db.session.add(new_user)
    db.session.add(new_password)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.password or not check_password_hash(user.password.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    # Create a new session
    session_token = secrets.token_hex(32)
    refresh_token = secrets.token_hex(32)
    
    # Define expiry times
    session_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    refresh_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)

    new_session = UserSession(
        user_id=user.id, # type: ignore
        session_token=session_token, # type: ignore
        expires_at=session_expiry,# type: ignore
        refresh_token=refresh_token,# type: ignore
        refresh_token_expires_at=refresh_expiry# type: ignore
    )
    db.session.add(new_session)
    db.session.commit()

    response = jsonify({
        'message': 'Logged in successfully'
    })
    response.set_cookie(
        'session_token', 
        session_token, 
        httponly=True, 
        secure=True,
        samesite='Lax',
        expires=session_expiry
    )
    response.set_cookie(
        'refresh_token', 
        refresh_token, 
        httponly=True, 
        secure=True, # Set to False if not using HTTPS in development
        samesite='Lax',
        expires=refresh_expiry
    )
    
    return response

@auth_bp.route('/refresh', methods=['POST'])
def refresh(referrer:str='/'):
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        return jsonify({'error': 'Missing refresh token'}), 401

    user_session = UserSession.query.filter_by(refresh_token=refresh_token).first()

    if not user_session:
        return jsonify({'error': 'Invalid refresh token'}), 401

    if user_session.refresh_token_expires_at < datetime.datetime.now(datetime.timezone.utc):
        # For security, if a compromised refresh token is used after expiry, delete the session.
        db.session.delete(user_session)
        db.session.commit()
        return jsonify({'error': 'Refresh token expired'}), 401

    # --- Token Rotation ---
    # Generate new tokens
    new_session_token = secrets.token_hex(32)
    new_refresh_token = secrets.token_hex(32)
    
    # Define new expiry times
    new_session_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    new_refresh_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)

    # Update the session in the database
    user_session.session_token = new_session_token
    user_session.expires_at = new_session_expiry
    user_session.refresh_token = new_refresh_token
    user_session.refresh_token_expires_at = new_refresh_expiry
    
    db.session.commit()

    # response = jsonify({
    #     'message': 'Token refreshed successfully'
    # })
    response = redirect(referrer, code=302)
    response.set_cookie(
        'session_token', 
        new_session_token, 
        httponly=True, 
        secure=True,
        samesite='Lax',
        expires=new_session_expiry
    )
    response.set_cookie(
        'refresh_token', 
        new_refresh_token, 
        httponly=True, 
        secure=True, # Set to False if not using HTTPS in development
        samesite='Lax',
        expires=new_refresh_expiry
    )
    
    return response

@auth_bp.route('/auth/status', methods=['GET'])
def status():
    """
    Checks if a user is logged in by verifying their session token.
    Returns a 200 OK status in all cases, with a JSON body
    indicating the authentication state.
    """
    auth_header = request.headers.get('Authorization')
    
    # Default response for a non-authenticated user
    not_logged_in_response = jsonify({"logged_in": False, "user": None})

    if not auth_header or not auth_header.startswith('Bearer '):
        return not_logged_in_response, 200

    try:
        session_token = auth_header.split(' ')[1]
    except IndexError:
        return not_logged_in_response, 200

    if not session_token:
        return not_logged_in_response, 200

    user_session = UserSession.query.filter_by(session_token=session_token).first()

    if not user_session:
        return not_logged_in_response, 200
        
    if user_session.expires_at < datetime.datetime.now(datetime.timezone.utc):
        return not_logged_in_response, 200

    # If all checks pass, the user is logged in.
    user = user_session.user
    
    return jsonify({
        "logged_in": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@require_session
def logout():
    # The require_session decorator puts the session object in g
    user_session = g.session 

    db.session.delete(user_session)
    db.session.commit()

    response = jsonify({'message': 'Logged out successfully'})
    # Also instruct the client to clear the refresh token cookie
    response.delete_cookie('refresh_token', path='/', samesite='Lax')
    
    return response

@auth_bp.route('/oauth/<provider>')
def oauth_login(provider):
    redirect_uri = url_for('auth.oauth_callback', provider=provider, _external=True)
    return oauth.create_client(provider).authorize_redirect(redirect_uri) # pyright: ignore[reportOptionalMemberAccess]

@auth_bp.route('/auth/auth_methods')
def get_auth_methods():
    oauth_methods = {}
    for provider, config in current_app.config.get('OAUTH_PROVIDERS', {}).items():
        oauth_methods[provider] = {
            'name': provider,
            'url': f"/oauth/{provider}"
        }
    
    auth_methods = {
        "login_form": True,
        "oauth": oauth_methods
    }

    return jsonify(auth_methods), 400



@auth_bp.route('/admin/password', methods=['GET'])
def get_admin_password():
    """
    Returns the admin password configured on the backend so the frontend
    can validate logins without bundling the secret in its build artifacts.
    """
    password = current_app.config.get('ADMIN_PASSWORD')
    if not password:
        return jsonify({'error': 'Admin password is not configured'}), 500

    return jsonify({'password': password})

@auth_bp.route('/oauth/<provider>/callback')
def oauth_callback(provider):
    client = oauth.create_client(provider)

    
    token = client.authorize_access_token() # pyright: ignore[reportOptionalMemberAccess]
    userinfo = client.userinfo() # pyright: ignore[reportOptionalMemberAccess]

    oauth_account = OAuthAccount.query.filter_by(provider=provider, provider_user_id=userinfo.get('sub')).first()

    if oauth_account:
        user = oauth_account.user
    else:
        user = User.query.filter_by(email=userinfo.get('email')).first()
        if not user:
            user = User(
                email=userinfo.get('email'),# type: ignore
                username=userinfo.get('email'), # Or generate a unique username # type: ignore
            )
            db.session.add(user)
        
        new_oauth_account = OAuthAccount(
            provider=provider, # type: ignore
            provider_user_id=userinfo.get('sub'), # type: ignore
            access_token=token.get('access_token'), # type: ignore
            user=user # type: ignore
        )
        db.session.add(new_oauth_account)
        db.session.commit()

    # Create a new session
    session_token = secrets.token_hex(32)
    refresh_token = secrets.token_hex(32)
    
    # Define expiry times
    session_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    refresh_expiry = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)

    new_session = UserSession(
        user_id=user.id, # type: ignore
        session_token=session_token, # type: ignore
        expires_at=session_expiry, # type: ignore
        refresh_token=refresh_token, # type: ignore
        refresh_token_expires_at=refresh_expiry # type: ignore
    )
    db.session.add(new_session)
    db.session.commit()

    # Redirect to the frontend with the session token
    frontend_url = f"{current_app.config['FRONTEND_URL']}/auth/callback?session_token={session_token}&expires_at={session_expiry.isoformat()}"
    
    # Also set the refresh token as a cookie
    response = redirect(frontend_url)
    response.set_cookie(
        'refresh_token', 
        refresh_token, 
        httponly=True, 
        secure=True, # Set to False if not using HTTPS in development
        samesite='Lax',
        expires=refresh_expiry
    )
    
    return response

@auth_bp.route('/oauth/logout', methods=['POST'])
def oauth_logout():
    """Handles back-channel logout notifications from the OAuth provider."""
    logout_token = request.form.get('logout_token')
    if not logout_token:
        return 'No logout token', 400

    # Find the right provider by iterating through the registered clients
    for provider_name in oauth._clients:
        client = oauth.create_client(provider_name)
        try:
            # The logout token is a JWT, we can parse it like an id_token
            # We pass nonce=None because logout tokens don't have a nonce
            claims = client.parse_id_token(logout_token, nonce=None) # pyright: ignore[reportOptionalMemberAccess]
            
            user_sub = claims.get('sub')
            if user_sub:
                oauth_account = OAuthAccount.query.filter_by(
                    provider=provider_name, 
                    provider_user_id=user_sub
                ).first()

                if oauth_account:
                    # Delete all sessions for this user
                    UserSession.query.filter_by(user_id=oauth_account.user_id).delete()
                    db.session.commit()
                    # Break the loop once the user is found and logged out
                    break
        except Exception as e:
            # This provider is not the issuer of the token, continue to the next one
            print(f"Could not validate logout token with {provider_name}: {e}")
            continue

    return 'Logout notification processed', 200

def init_app(app: Flask):
    oauth.init_app(app)
    for provider, config in app.config.get('OAUTH_PROVIDERS', {}).items():
        oauth.register(
            name=provider,
            **config
        )

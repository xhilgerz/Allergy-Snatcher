from flask import Blueprint, request, url_for, session, redirect, jsonify
from authlib.integrations.flask_client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.database import db, User, Password, OAuthAccount

oauth = OAuth()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    new_user = User(username=username, email=email)
    new_password = Password(password_hash=generate_password_hash(password), user=new_user)
    
    db.session.add(new_user)
    db.session.add(new_password)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.password or not check_password_hash(user.password.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Logged in successfully'})

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@auth_bp.route('/oauth/<provider>')
def oauth_login(provider):
    redirect_uri = url_for('auth.oauth_callback', provider=provider, _external=True)
    return oauth.create_client(provider).authorize_redirect(redirect_uri)

@auth_bp.route('/oauth/<provider>/callback')
def oauth_callback(provider):
    client = oauth.create_client(provider)
    token = client.authorize_access_token()
    userinfo = client.get('userinfo').json()

    oauth_account = OAuthAccount.query.filter_by(provider=provider, provider_user_id=userinfo.get('sub')).first()

    if oauth_account:
        session['user_id'] = oauth_account.user_id
        return redirect('/')

    user = User.query.filter_by(email=userinfo.get('email')).first()

    if not user:
        user = User(
            email=userinfo.get('email'),
            username=userinfo.get('email'), # Or generate a unique username
        )
        db.session.add(user)

    new_oauth_account = OAuthAccount(
        provider=provider,
        provider_user_id=userinfo.get('sub'),
        access_token=token.get('access_token'),
        user=user
    )
    db.session.add(new_oauth_account)
    db.session.commit()

    session['user_id'] = user.id
    return redirect('/')

def init_app(app):
    oauth.init_app(app)
    for provider, config in app.config.get('OAUTH_PROVIDERS', {}).items():
        oauth.register(
            name=provider,
            **config
        )

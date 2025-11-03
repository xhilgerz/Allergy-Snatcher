from functools import wraps
from flask import request, g, jsonify
from .database import UserSession, User
import datetime

def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        session_token = auth_header.split(' ')[1]

        if not session_token:
            return jsonify({"error": "Missing session token"}), 401

        user_session = UserSession.query.filter_by(session_token=session_token).first()
        if not user_session:
            return jsonify({"error": "Invalid session token"}), 401

        # You might want to check for session expiry here
        if user_session.expires_at < datetime.datetime.now(datetime.timezone.utc):
            # Log the user out, or if refresh oauth token is available, try to renew the session token
            return jsonify({"error": "Session expired"}), 401
            
        user = User.query.get(user_session.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        g.user = user
        g.session = user_session # Store the session object for easy access
        return f(*args, **kwargs)
    return decorated_function

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user') or g.user.role != role:
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_force(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('confirmation') != 'force':
            return jsonify({"error": "Confirmation required"}), 400
        return f(*args, **kwargs)
    return decorated_function

def optional_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.user = None
        g.session = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            try:
                session_token = auth_header.split(' ')[1]
            except IndexError:
                session_token = None

            if session_token:
                user_session = UserSession.query.filter_by(session_token=session_token).first()
                
                if user_session and user_session.expires_at > datetime.datetime.now(datetime.timezone.utc):
                    user = User.query.get(user_session.user_id)
                    if user:
                        g.user = user
                        g.session = user_session
        
        return f(*args, **kwargs)
    return decorated_function

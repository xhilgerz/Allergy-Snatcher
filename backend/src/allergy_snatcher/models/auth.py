from functools import wraps
from flask import request, g, jsonify
from .database import UserSession, User
import datetime

def _utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

def _is_active(expires_at: datetime.datetime | None) -> bool:
    if not expires_at:
        return False
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=datetime.timezone.utc)
    return expires_at > _utc_now()

def require_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        session_token = request.cookies.get('session_token')
        if not session_token:
            return jsonify({"error": "Missing session token"}), 401

        user_session = UserSession.query.filter_by(session_token=session_token).first()
        if not user_session:
            return jsonify({"error": "Invalid session token"}), 401

        # You might want to check for session expiry here
        if not _is_active(user_session.expires_at):
            # Log the user out, or if refresh oauth token is available, try to renew the session token
            return jsonify({"error": "Session expired"}), 401
            
        user = User.query.get(user_session.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        if user.role == 'disabled':
            return jsonify({"error": "User is disabled"}), 403
        
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
        
        session_token = request.cookies.get('session_token')

        if session_token:
            user_session = UserSession.query.filter_by(session_token=session_token).first()
            
            if user_session and _is_active(user_session.expires_at):
                user = User.query.get(user_session.user_id)
                if user and user.role != 'disabled':
                    g.user = user
                    g.session = user_session
        
        return f(*args, **kwargs)
    return decorated_function

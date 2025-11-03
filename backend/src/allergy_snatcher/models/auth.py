from functools import wraps
from flask import request, g, jsonify
from .database import UserSession, User
from datatime import datetime

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
        if user_session.expires_at < datetime.datetime.now():
            return jsonify({"error": "Session expired"}), 401
            
        user = User.query.get(user_session.user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        g.user = user_session.user
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

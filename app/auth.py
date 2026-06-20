from functools import wraps
from flask import session, redirect, request, jsonify

def require_login(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        if request.path.startswith('/api/'):
            return jsonify({'ok':False,'error':'not_authenticated'}), 401
        return redirect('/login')
    return wrapper

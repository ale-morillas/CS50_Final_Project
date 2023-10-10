from flask import redirect, render_template, session
import string
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def validate_password(password):
    """Helper function: Return true if the password has at least 8 characters
    where at least one must be a number, one a punctuation and one an uppercase letter
    """
    punctuation = string.punctuation
    
    if len(password) < 8:
        return False
    
    for i in password:
        if i.isupper() or i.isdigit() or (i in punctuation) or i.isalpha():
            pass
        else:
            return False
    return True


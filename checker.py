from flask import redirect, session
#import vsearch4web
from functools import wraps

def check_logged_in(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
                if 'logged_in' in session:
                        return func(*args, **kwargs)
                return redirect('/login')
        return wrapper

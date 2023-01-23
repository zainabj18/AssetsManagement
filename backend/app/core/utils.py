from flask import request,current_app
def protected():
 
    def decorated_route(func):
 
        def wrapper(*args, **kwargs):
            token=None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            else:
                return {"msg":"Please provide a token in the header","error":"Missing Token"},401
            func(*args, **kwargs)    
        return wrapper
    return decorated_route
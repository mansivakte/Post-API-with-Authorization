import jwt
from flask import request
from app.user.model import User
from functools import wraps

def loginRequired(fun):
    @wraps(fun)
    def innerFun(*args, **kwargs):
        try:
            token = request.headers['Authorization']
            decode= jwt.decode(token, "MPM", algorithms=["HS256"])
            if decode:
                user = User.query.filter_by(id=decode['id']).first()
                if user:
                    return fun(user.id, *args, **kwargs)
                else:
                    return "1....Unauthorized user"
            else:
                return "2....Unauthorized user"
        except Exception as e: 
            print("error",e)
            return "3....Unauthorized user"
    return innerFun

import inspect

from functools import wraps
from flask import request, jsonify, json


def parse_params(required_params):
    """Depending on the content_type, try to extract the params. We take 
    application/json or multipart (when doing upload).
    
    Note we could strictly use application/json but upload file payload 
    will ~30% bigger due to base64 encoding."""
    params = {}
    if (request.content_type or '').startswith('multipart'):
        params = request.form
    elif request.is_json():
        params = request.get_json()
    missing_params = []
    for name in required_params:
        if params.get(name) is None:
            missing_params.append(name)
    return (params, missing_params)


def route(bp, *args, required_params=[], **kwargs):
    """Hacky helper to parse/validate params and jsonify response."""
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            # route defs with can ask for request params to be parse 
            # by specifying a params function argument
            if 'params' in inspect.getfullargspec(f).args:
                params, missing_params = parse_params(required_params)
                if missing_params:
                   return jsonify(dict(error=f'Missing required params: {missing_params}')), 400
                kwargs['params'] = params
            status = 200
            resp = f(*args, **kwargs)
            if isinstance(resp, tuple):
                resp = resp[0]
                status = resp[1]
            return jsonify(resp), status
        return f
    return decorator


def try_parse_int(s, val=None):
    try:
        return int(s)
    except Exception:
        return val


class JSONSerializer:
    """Marker class"""


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JSONSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)

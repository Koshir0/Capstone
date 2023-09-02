from functools import wraps
from flask import request, jsonify 
from jose import jwt
import json
import requests


# Replace with your Auth0 data
AUTH0_DOMAIN = 'dev-bck285lacrwuo4mg.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'menu'


def requires_auth(permission=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            json_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
            jwks_response = requests.get(json_url)
            jwks_data = jwks_response.json()

            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks_data['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }

            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/',
                )

                if 'permissions' not in payload:
                    # raise AuthError('Permissions not included in JWT', 400)
                    jsonify({'AuthError': 'Permissions not included in JWT'}), 400

                if permission not in payload['permissions']:
                    # raise AuthError('Permission not found', 403)
                    jsonify({'AuthError': 'Permission not found'}), 403


                return f(payload, *args, **kwargs)

            except jwt.ExpiredSignatureError:
                # raise AuthError('Token expired', 401)
                jsonify({'AuthError': 'Token expired'}), 401
            except jwt.JWTClaimsError:
                # raise AuthError('Invalid claims', 401)
                jsonify({'AuthError': 'Invalid claims'}), 401

            except Exception:
                # raise AuthError('Invalid token', 401)
                jsonify({'AuthError': 'Invalid token'}), 401

        return wrapper
    return decorator


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        # raise AuthError('Authorization header is missing', 401)
        jsonify({'AuthError': 'Authorization header is missing'}), 401
    else:
        print(auth_header)

        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            # raise AuthError('Authorization header must start with "Bearer"', 401)
            jsonify({'AuthError': 'Authorization header must start with "Bearer'}), 401
        elif len(parts) == 1:
            # raise AuthError('Token not found', 401)
            jsonify({'AuthError': 'Token not found'}), 401
        elif len(parts) > 2:
            # raise AuthError('Authorization header must be Bearer token', 401)
            jsonify({'AuthError': 'Authorization header must be Bearer token'}), 401

        return parts[1]



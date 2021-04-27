import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from routes import ROUTES
from blocklist import BLOCKLIST

app = Flask(__name__)

ACCESS_EXPIRES = timedelta(hours=1)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.secret_key = 'coolly'
api = Api(app)


jwt = JWTManager(app)


@jwt.user_identity_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback(header, payload):
    return jsonify({
        'description': 'The Token has expired.',
        'error': 'token_expired',
        'header': header,
        'payload': payload,
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verication failed.',
        'error': 'invalid_token',
        'err': error
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required',
        'err': error
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(header, payload):
    return jsonify({
        'description': 'The Token is not fresh.',
        'error': 'fresh_token_required',
        'header': header,
        'payload': payload,
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(header, payload):
    return jsonify({
        'description': 'The Token has been revoked.',
        'error': 'token_revoked',
        'header': header,
        'payload': payload,
    }), 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["identity"] in BLOCKLIST


for route in ROUTES:
    api.add_resource(route['resource'], route['endpoint'])


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)

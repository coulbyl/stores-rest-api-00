import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from routes import ROUTES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db').replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'coolly'
api = Api(app)


jwt = JWTManager(app)

for route in ROUTES:
    api.add_resource(route['resource'], route['endpoint'])


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000, debug=True)

from app import app
from db import db
from token import TokenBlocklist


db.init_app(app)


@app.before_first_request
def run_migration():
    db.create_all()

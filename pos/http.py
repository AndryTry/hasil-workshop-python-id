from flask import Flask
from pos.config import Config
from pos.models import db
from pos.views.products import bp as bp_products
from pos.views.transaction import bp as bp_transaction


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.register_blueprint(bp_products)
    app.register_blueprint(bp_transaction)
    return app

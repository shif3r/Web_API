import logging, os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import Config
from app.jsonEncoder import MyJSONEncoder
 
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.json_encoder = MyJSONEncoder
    app.config.from_object(config_class) #загрузка конфигурации из файла
    db.init_app(app) #активация базы данных для приложения
    ma.init_app(app)
    migrate.init_app(app, db)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp) #активация blueprint для ссылок типа url_prefix='/api'
    return app

from app import models
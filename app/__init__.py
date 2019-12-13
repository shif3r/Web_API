import logging, os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
 
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) #загрузка конфигурации из файла
    db.init_app(app) #активация базы данных для приложения
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp) #активация blueprint для ссылок типа url_prefix='/api'
    return app

#from app import models
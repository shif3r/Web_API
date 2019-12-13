from datetime import datetime
from flask import request, g, jsonify, current_app
from app import db
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'msg': 'Hello World!'})
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def response(status_code):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    response = jsonify(payload)
    response.status_code = status_code
    return response

def response_message(message):
    return jsonify({'message': message})

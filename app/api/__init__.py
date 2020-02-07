from flask import Blueprint

bp = Blueprint('main', __name__)

from app.api import routes_bookings
from app.api import routes_airports
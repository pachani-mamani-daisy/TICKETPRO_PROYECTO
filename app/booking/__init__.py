from flask import Blueprint

booking_bp = Blueprint('booking', __name__, template_folder='templates')

from . import routes
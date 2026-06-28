from flask import Blueprint

movie_bp = Blueprint('movie', __name__, template_folder='templates')

from . import routes
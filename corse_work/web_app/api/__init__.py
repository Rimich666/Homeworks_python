from flask import Blueprint

api_app = Blueprint("api_app", __name__, url_prefix="/api")

from . import orders
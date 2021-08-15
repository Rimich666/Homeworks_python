from flask import Blueprint

login_app = Blueprint("login_app", __name__, url_prefix="/login")

from .login import login

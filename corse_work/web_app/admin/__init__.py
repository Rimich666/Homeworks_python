from flask import Blueprint

#from . import AddDefault

admin_app = Blueprint("admin_app", __name__, url_prefix="/admin")

from . import admin



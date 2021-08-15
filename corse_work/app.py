from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for)
from flask_migrate import Migrate
from web_app.orders import orders_app
from web_app.admin import admin_app
from web_app.login import login_app
from  web_app.api import api_app
from web_app.models import db, login
from config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(admin_app)
app.register_blueprint(login_app)
app.register_blueprint(orders_app)
app.register_blueprint(api_app)

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)


@app.route('/')
def hello_world():
    return redirect(url_for('login_app.login'))
#    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

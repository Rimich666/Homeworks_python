from flask import Flask, request, render_template
from flask_migrate import Migrate
from web_app.models import db
from web_app.views import (
    admin_app)
from config import DevelopmentConfig
app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

app.register_blueprint(admin_app)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

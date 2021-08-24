from flask import (
    Flask,
    redirect,
    url_for)
from flask_migrate import Migrate
from flask_login import current_user
from flask_principal import (
    UserNeed,
    RoleNeed,
    identity_loaded
)


from web_app.orders import orders_app
from web_app.admin import admin_app
from web_app.login import login_app
from  web_app.api import api_app
from web_app.models import (
    db,
    login,
    principals,
    socketio
)
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
principals.init_app(app)
socketio.init_app(app)


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role.role))


@app.route('/')
def hello_world():
    return redirect(url_for('login_app.login'))
#    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

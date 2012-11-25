from flask import Flask
from codingbooth.models import User

from flask.ext.login import LoginManager

# Generally setup the app
app = Flask(__name__)

# Configure it
app.config.from_object('codingbooth.default_config')
#app.config.from_pyfile('config.cfg')

# Setup the login
login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    return User(None, None, userid)


import codingbooth.views

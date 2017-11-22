import flask
web_interface = flask.Flask(__name__)
web_interface.config.from_object('config')
from web import views

# Import flask and template operators
from flask import Flask, render_template, send_from_directory

import logging

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('app.config')

@app.route('/')
def index():
	return render_template('index.html')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_api)
from app.mod_api.controllers import mod_api as api_module

# Register blueprint(s)
app.register_blueprint(api_module)

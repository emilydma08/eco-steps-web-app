from flask import Flask

# Initialize the Flask app
app = Flask(__name__)

# Import routes
from app import routes

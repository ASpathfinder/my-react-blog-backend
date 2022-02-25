from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)

from . view import *

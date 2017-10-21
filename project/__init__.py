from flask import Flask

app = Flask(__name__)

from . import views, sql
from .sql import Url, db
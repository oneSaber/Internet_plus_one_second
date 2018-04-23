from flask import blueprints
main = blueprints('main',__name__)
from . import views
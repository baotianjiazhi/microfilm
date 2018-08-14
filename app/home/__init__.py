"""
Created by Baobaobao123
Thank you 
"""
__author__ = 'Baobaobao123'

from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views

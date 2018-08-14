"""
Created by Baobaobao123
Thank you 
"""
from flask import Blueprint

__author__ = 'Baobaobao123'



admin = Blueprint("admin", __name__)

import app.admin.views
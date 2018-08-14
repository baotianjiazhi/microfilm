"""
Created by Baobaobao123
Thank you 
"""
__author__ = 'Baobaobao123'

from . import home
from flask import render_template

@home.route("/")
def index():
    return render_template("home/index.html")
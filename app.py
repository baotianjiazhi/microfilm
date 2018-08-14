"""
Created by Baobaobao123
Thank you 
"""
__author__ = 'Baobaobao123'

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run()


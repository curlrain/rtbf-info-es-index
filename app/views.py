__author__ = 'fabien'
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Index Page'


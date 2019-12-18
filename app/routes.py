from app import app
from flask import request
import db

@app.route('/')
@app.route('/index')

def index():
    print(request.args.get('test'))
    db.open_connection("../db.config")
    result = db.execute_db("SELECT * FROM courses JOIN slots USING(course_id);")
    db.close_connection()

    return result[0][0]
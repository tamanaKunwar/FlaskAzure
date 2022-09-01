from flask import Flask
from flask import request, Response
from flask import json
from src.student_wrapper import get_student_details, update_student_data

import logging

app = Flask(__name__)


@app.route("/hello")
def hello():
    return Response(json.dumps({"Hello":"World"}), status=200, mimetype='application/json')


@app.route("/StudentDetails/<roll_no>", methods=['GET'])
def student_details(roll_no):
    roll_no = roll_no
    jd = get_student_details(roll_no)
    return Response(jd, status=200, mimetype='application/json')


@app.route("/updateStudentDetails", methods = ["POST"])
def update_details():
    data = request.get_json()
    jd = update_student_data(data)
    return Response(jd, status=200, mimetype='application/json')


if __name__ == '__main__':
    logging.info('IN MAIN OF TAMSERVER FLASK')
    app.run()

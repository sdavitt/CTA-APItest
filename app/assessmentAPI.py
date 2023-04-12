from flask import jsonify, request
from app import app
from functools import wraps
from app.models import Student, db

def token_required(api_route):
    @wraps(api_route)
    def decorator_function():
        token = request.headers.get('access-token')
        if not token:
            return jsonify({'Access denied': 'No API token - please make your auth request to retrieve a token.'}), 401
        try:
            exists = Student.query.get(token)
            if not exists:
                return jsonify({'Invalid API token': 'Please check your API token or request a new one.'}), 403
            # if the token is present and valid, allow the request to go through
            return api_route(exists)
        except:
            return 'Database or server error - message Sam on slack with a screenshot of your call code please', 500
    return decorator_function


@app.route('/authme/<string:cohort>/<string:name>', methods=['GET'])
def authme(cohort, name):
    cs = {'Foxes', 'Sp', 'Padawans', 'Cdn', 'Rangers', 'Kekambas', 'Thieves'}
    if cohort.title() not in cs:
        return 'Invalid Cohort Name', 400
    if not name:
        return 'Name not provided', 400
    if db.query.filter_by(name=name):
        return 'You already have an access token - check your prior calls.', 400
    try:
        ns = Student(name, cohort)
        db.session.add(ns)
        db.session.commit()
        return {'Access Token': ns.id}, 200
    except:
        return 'Database or server error - message Sam on slack with a screenshot of your call code please', 500
    
@app.route('/answer', methods=['POST'])
@token_required
def answer(student):
    data = request.get_json()
    checker = answer_check(data)
    if checker:
        student.success = True
        student.calls += 1
        db.session.commit()
        return 'Success! You completed the assessment! Send Sam your code on slack.', 200
    else:
        student.calls += 1
        db.session.commit()
        return 'Unsuccessful', 406


def answer_check(data):
    return True
        

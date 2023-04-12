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
            return {'Error':'Database or server error - message Sam on slack with a screenshot of your call code please'}, 500
    return decorator_function


@app.route('/authme', methods=['GET'])
def authme():
    data = request.get_json()
    cs = {'Foxes', 'Sp', 'Padawans', 'Cdn', 'Rangers', 'Kekambas', 'Thieves'}
    if data['cohort'].title() not in cs:
        return {'Error':'Invalid Cohort Name'}, 400
    if not data['name']:
        return {'Name not provided'}, 400
    x = Student.query.filter_by(name=data['name']).first()
    print(x)
    if x:
        x.calls += 1
        db.session.commit()
        return {'Error':'You already have an access token - check your prior calls.'}, 400
    try:
        ns = Student(data['name'], data['cohort'])
        db.session.add(ns)
        db.session.commit()
        return {'Access Token': ns.id}, 200
    except:
        return {'Error':'Database or server error - message Sam on slack with a screenshot of your call code please'}, 500
    
@app.route('/forgot/<string:name>', methods=['GET'])
def forgot(name):
    try:
        x = Student.query.filter_by(name=name).first()
        x.calls += 1
        db.session.commit()
        return {'Access Token': x.id}, 200
    except:
        return {'Error': 'Unfortunately this route has bad error messaging... its a challenge!'}, 400
    
@app.route('/answer', methods=['POST'])
@token_required
def answer(student):
    data = request.get_json()
    checker = answer_check(data['UAMs'])
    if checker:
        student.success = True
        db.session.commit()
        return {'Success': 'You completed the assessment! Send Sam your code on slack.'}, 200
    else:
        student.calls += 1
        db.session.commit()
        return {'Unsuccessful': 'Your answer did not pass the tests- try again!'}, 406


def answer_check(data):
    if data == [0,2,0,0,0]:
        return True
    return False

@app.route('/getdata', methods=['GET'])
@token_required
def getdata(student):
    return {'Data': {'logs': [[0,5],[1,2],[0,2],[0,5],[1,3]], 'k': 5}}, 200

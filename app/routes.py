from flask import jsonify, request
from app import app
from app.models import db, Character, Alias

@app.route('/alias/<string:id>', methods=['GET'])
def get_alias(id):
    """
    [GET] Alias ID
    returns JSON data about one Alias
    """
    alias = Alias.query.get(id)
    if alias:
        return alias.to_dict(), 200
    else:
        return {id: 'Alias not found.'}, 404

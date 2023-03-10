from flask import jsonify, request
from app import app
from datetime import date
from app.models import db, Character, Alias

@app.route('/alias/<string:id>', methods=['GET'])
def get_alias(id):
    """
    [GET] Alias ID
    returns JSON data about one Alias
    """
    alias = Alias.query.get(id) # <Alias object>
    if alias:
        return alias.to_dict(), 200
    else:
        return {id: 'Alias not found.'}, 404

@app.route('/character/<string:id>', methods=['GET'])
def get_character(id):
    """
    [GET]
    input: string ID for the character
    output: JSON character info plus all relevant alias info
    """
    # take the input id and use it to query our database for a matching character
    char = Character.query.get(id) # <Character object> or None
    # if the characters exists, convert its relevant info to dictionary format
    if char:
        # return the dictionary with a status code
        return char.to_dict(), 200
    else:
        return {id: 'Character not found.'}, 404

@app.route('/create/alias', methods=['POST'])
def create_alias():
    """
    [POST] create a new alias
    expected JSON body: {
        'name': <str>,
        'real_character': <str character.id>,
        'occupation': <str><optional>,
        'last_seen': <isoformat str YYYY-MM-DD><optional>
    }
    """
    try:
        data = request.json
        print(data)
        # check if this character exists, if it does make the alias otherwise bad request
        if Character.query.get(data['real_character']):
            new_alias = Alias(data.get('name'), data.get('real_character'), data.get('occupation'), data.get('last_seen'))
        else:
            return {'Error': 'no character matching that real_character id'}, 400
    except Exception as e:
        print(e)
        return {'Bad Request': 'improper data provided for alias creation'}, 400
    try:
        db.session.add(new_alias)
        db.session.commit()
        return {'Created': new_alias.to_dict()}, 201
    except:
        return {'Error': 'alias already exists'}, 400

@app.route('/create/character', methods=['POST'])
def create_character():
    """
    [POST] create a new character
    expected JSON body: {
        'name': <str>
    }
    """
    try:
        c = Character(request.json['name'])
        db.session.add(c)
        db.session.commit()
        return {'Created': c.to_dict()}, 200
    except:
        return {'Bad Request'}, 400

@app.route('/update/alias/lastseen', methods=['PUT'])
def update_alias():
    """
    [PUT] updating an alias' last seen date
    expected JSON body: {
        'aliasID': <str>,
        'last seen': <str isoformat date YYYY-MM-DD>
    }
    """
    if request.json:
        a = Alias.query.get(request.json.get('aliasID'))
        if a:
            a.last_seen = date.fromisoformat(request.json.get('last seen'))
            db.session.commit()
            return {'Updated': a.to_dict()}, 200
        else:
            return {'Bad Request': 'no alias with that ID'}, 400
    else:
        return {'Bad Request'}, 400

@app.route('/del/alias/<string:id>', methods=['DELETE'])
def delete_alias(id):
    """
    [DEL] alias by id
    """
    alias = Alias.query.get(id)
    if alias:
        db.session.delete(alias)
        db.session.commit()
        return {'Deleted': alias.to_dict(full=False)}, 200
    return {'Delete failed': 'no alias with that id'}, 400


@app.route('/del/character/<string:id>', methods=['DELETE'])
def delete_character(id):
    """
    [DEL] character by id, will also delete all aliases of that character
    """
    char = Character.query.get(id)
    if char:
        db.session.delete(char)
        db.session.commit()
        return {'Deleted': char.name}, 200
    return {'Delete failed': 'no character with that id'}, 400
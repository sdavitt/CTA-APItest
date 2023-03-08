from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from uuid import uuid4


db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    aliases = db.relationship('Alias', backref='character') # Character.aliases -> entire Alias objects # Alias.character -> entire Character object
    
    def __init__(self, name):
        self.name = name
        self.id = str(uuid4())


class Alias(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    occupation = db.Column(db.String(200))
    real_character = db.Column(db.String(40), db.ForeignKey('character.id')) # Alias.real_character -> just the string ID from the alias table
    last_seen = db.Column(db.DateTime)

    def __init__(self, name, charID, occupation=None, last_seen=None):
        self.id = str(uuid4())
        self.name = name
        self.real_character = charID
        self.occupation = occupation
        if last_seen:
            try:
                self.last_seen = date.fromisoformat(last_seen)
            except:
                pass

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'real_character_id': self.real_character,
            'real_character_name': self.character.name,
            'last seen': date.isoformat(self.last_seen)
        }
            

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from uuid import uuid4


db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    aliases = db.relationship('Alias', backref='character', cascade='all, delete-orphan') # Character.aliases -> entire Alias objects # Alias.character -> entire Character object
    
    def __init__(self, name):
        self.name = name
        self.id = str(uuid4())

    def to_dict(self):
        d = {
            'id': self.id,
            'name': self.name,
            'last known alias': self.calc_last_alias(),
            'created': date.isoformat(self.created), # 'YYYY-MM-DD'
            'aliases': None # maybe grab the aliases here, maybe do it in the routing
        }
        if self.aliases:
            d['aliases'] = [x.to_dict(full=False) for x in self.aliases]
        return d

    def calc_last_alias(self):
        lsa = None
        for alias in self.aliases:
            # lsa.last_seen - alias.last_seen
            if lsa and alias.last_seen:
                td = lsa.last_seen - alias.last_seen
                if td.days < 0:
                    lsa = alias
            elif alias.last_seen:
                lsa = alias
        return lsa.name if lsa else None
            
                
        

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

    def to_dict(self, full=True):
        x = self.last_seen
        if x:
            x = date.isoformat(self.last_seen)
        return {
            'id': self.id,
            'name': self.name,
            'real_character_id': self.real_character,
            'real_character_name': self.character.name,
            'last seen': x
        } if full else {
            'id': self.id,
            'name': self.name,
            'last seen': x
        }
            
class Student:
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    cohort = db.Column(db.String(200), nullable=False)
    calls = db.Column(db.Integer)
    success = db.Column(db.boolean)

    def __init__(self, name, cohort):
        self.id = str(uuid4())
        self.name = name
        self.cohort = cohort
        self.calls = 1
        self.success = False


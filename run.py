from app import app
from app.models import db, Character, Alias

@app.shell_context_processor
def shell_context():
    return {'db': db, 'C': Character, 'A': Alias}
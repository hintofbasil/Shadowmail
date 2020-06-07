from main import db

class VirtualAlias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias_email = db.Column(db.String(100), unique=True)
    real_email = db.Column(db.String(100))
    enabled = db.Column(db.Boolean, default=True)

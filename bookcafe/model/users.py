from ..extentions import db, ma
from flask_login import UserMixin
from datetime import datetime
import uuid

def uuid_gen():
    return str(uuid.uuid4())

#create a User model
class User(db.Model, UserMixin):
    id = db.Column(db.String(200), primary_key = True, default=uuid_gen) 
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    category = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(120), nullable = False)
    # password2 = db.Column(db.String(120), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, username, email, category, password):
        self.username = username
        self.email = email
        self.category = category
        self.password = password

    def __repr__(self):
        return self.id


class UserSchema(ma.Schema):
    class meta:
        model = User
        load_instance = True

    
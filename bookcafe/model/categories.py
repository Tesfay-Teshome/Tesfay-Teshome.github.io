from ..extentions import db,ma
from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy
# from bookcafe.model.books import Book

def uuid_gen():
    return str(uuid.uuid4())
#create a Category model
class Category(db.Model):

    id = db.Column(db.String(200), primary_key = True, default=uuid_gen) 
    category = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    books = db.relationship('Book', backref='categoryofbook')


    def __repr__(self):
        return self.id


class CategorySchema(ma.Schema):
    class meta:
        fields = ('category')
        load_instance = True
from ..extentions import db,ma
import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bookcafe.model.categories import Category


def uuid_gen():
    return str(uuid.uuid4())

#create a Book model
class Book(db.Model):

    id = db.Column(db.String(200), primary_key = True, default=uuid_gen) 
    title = db.Column(db.String(200))
    author = db.Column(db.String(120))
    # category = db.Column(db.String(120))
    category_id = db.Column(db.String, db.ForeignKey('category.id'))
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,title,author,category,description):
        self.title=title
        self.author=author 
        self.category=category 
        self.description=description
    def __repr__(self):
        return self.id




class BookSchema(ma.Schema):
    class meta:
        fields = ('title','author','category','description')

book_schema = BookSchema(many=False)
books_schema = BookSchema(many=True)

        

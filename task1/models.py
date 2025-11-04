# models.py
from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, connect
import datetime

class Author(Document):
    meta = {'collection': 'authors'}
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    meta = {'collection': 'quotes'}
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
    tags = ListField(StringField())

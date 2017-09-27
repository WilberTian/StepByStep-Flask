from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class DbHelper():
    def add(self, resource):
        db.session.add(resource)
        db.session.commit

    def update(self):
        db.session.commit()

    def delete(self, resource):
        db.session.delete()
        db.session.commit()


class Category(db.Model, DbHelper):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.categoryresource', id='<id>', _external=True)
    blogs = fields.Nested('BlogSchema', many=True, exclude=('category',))

class Blog(db.Model, DbHelper):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    content = db.Column(db.String(500), unique=True, nullable=False)
    author = db.Column(db.String(50), unique=True, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('blogs', lazy='dynamic', order_by='Blog.title'))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

class BlogSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(3))
    content = fields.String(required=True, validate=validate.Length(3))
    author = fields.String(required=True, validate=validate.Length(3))
    creation_date = fields.DateTime()
    category = fields.Nested(CategorySchema, only=['id', 'url', 'name'], required=True)
    url = ma.URLFor('api.blogresource', id='<id>', _external=True)

    @pre_load
    def process_category(self, data):
        category = data.get('category')
        if category:
            if isinstance(category, dict):
                category_name = category.get('name')
            else:
                category_name = category
            category_dict = dict(name=category_name)                
        else:
            category_dict = {}
        data['category'] = category_dict
        return data

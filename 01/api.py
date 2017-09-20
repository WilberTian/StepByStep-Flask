from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import BlogModel
import status
from pytz import utc

class BlogManager():
    last_id = 0

    def __init__(self):
        self.blogs = {}

    def add_blog(self, blog): 
        self.__class__.last_id += 1
        blog.id = self.__class__.last_id
        self.blogs[self.__class__.last_id] = blog

    def get_blog(self, id):
        return self.blogs[id]

    def delete_blog(self, id):
        del self.blogs[id]


blog_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'author': fields.String,
    'creation_date': fields.DateTime
}


blog_manager = BlogManager()

class BlogResource(Resource):
    def abort_if_blog_doesnt_exist(self, id):
        if id not in blog_manager.blogs:
            abort(
                status.HTTP_404_NOT_FOUND, 
                message="Blog {0} doesn't exist".format(id))

    @marshal_with(blog_fields)
    def get(self, id):
        self.abort_if_blog_doesnt_exist(id)
        return blog_manager.get_blog(id)

    def delete(self, id):
        self.abort_if_blog_doesnt_exist(id)
        blog_manager.delete_blog(id)
        return '', status.HTTP_204_NO_CONTENT

    @marshal_with(blog_fields)
    def patch(self, id):
        self.abort_if_blog_doesnt_exist(id)
        blog = blog_manager.get_blog(id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('content', type=str)
        parser.add_argument('author', type=str)
        args = parser.parse_args()
        if 'title' in args:
            blog.title = args['title']
        if 'content' in args:
            blog.content = args['content']
        if 'author' in args:
            blog.author = args['author']
        return blog

class BlogListResource(Resource):
    @marshal_with(blog_fields)
    def get(self):
        return [v for v in blog_manager.blogs.values()]

    @marshal_with(blog_fields)
    def post(self):
        parser = reqparse.RequestParser();
        parser.add_argument('title', type=str, required=True, help='Title cannot be blank!')
        parser.add_argument('content', type=str, required=True, help='Content cannot be blank!')
        parser.add_argument('author', type=str, required=True, help='Author cannot be blank!')
        args = parser.parse_args()

        blog = BlogModel(
            title=args['title'],
            content=args['content'],
            author=args['anthor'],
            creation_date=datetime.now(utc)
        )
        blog_manager.add_blog(blog)
        return blog, status.HTTP_201_CREATED


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(BlogListResource, '/api/blogs/')
    api.add_resource(BlogResource, '/api/blogs/<int:id>', endpoint='blog_endpoint')

    return app


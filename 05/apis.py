from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, Category, CategorySchema, Blog, BlogSchema
from sqlalchemy.exc import SQLAlchemyError
import status

api_bp = Blueprint('api', __name__)
category_schema = CategorySchema()
blog_schema = BlogSchema()
api = Api(api_bp)

class BlogResource(Resource):
    def get(self, id):
        blog = Blog.query.get_or_404(id)
        result = blog_schema.dump(blog).data
        return result

    def patch(self, id):
        blog = Blog.query.get_or_404(id)
        blog_dict = request.get_json(force=True)
        if 'title' in blog_dict:
            blog.title = blog_dict['title']
        if 'content' in blog_dict:
            blog.content = blog_dict['content']
        if 'author' in blog_dict:
            blog.author = blog_dict['author']

        dumped_blog, dump_errors = blog_schema.dump(blog)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = blog_schema.validate(dumped_blog)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            blog.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_400_BAD_REQUEST

    def delete(self, id):
        blog = Blog.query.get_or_404(id)
        try:
            delete = blog.delete(blog)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_401_UNAUTHORIZED

class BlogListResource(Resource):
    def get(self):
        blogs = Blog.query.all()
        result = blog_schema.dump(blogs, many=True).data
        return result             

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = blog_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            category_name = request_dict['category']['name']
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                # Create a new Category
                category = Category(name=category_name)
                db.session.add(category)
            # Now that we are sure we have a category
            # create a new Message
            blog = Blog(
                title=request_dict['title'],
                content=request_dict['content'],
                author=request_dict['author'],
                category=category)
            blog.add(blog)
            query = Blog.query.get(blog.id)
            result = blog_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

class CategoryResource(Resource):
    def get(self, id):
        category = Category.query.get_or_404(id)
        result = category_schema.dump(category).data
        return result

    def patch(self, id):
        category = Category.query.get_or_404(id)
        category_dict = request.get_json()
        if not category_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(category_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in category_dict:
                category.name = category_dict['name']
            category.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_400_BAD_REQUEST
         
    def delete(self, id):
        category = Category.query.get_or_404(id)
        try:
            category.delete(category)
            response = make_response()
            return response, status.HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, status.HTTP_401_UNAUTHORIZED


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        results = category_schema.dump(categories, many=True).data
        return results

    def post  (self):
        request_dict = request.get_json()
        if not request_dict:
            resp = {'message': 'No input data provided'}
            return resp, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_dict)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            category = Category(request_dict['name'])
            category.add(category)
            query = Category.query.get(category.id)
            result = category_schema.dump(query).data
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, status.HTTP_400_BAD_REQUEST



api.add_resource(BlogResource, '/blogs/<int:id>')    
api.add_resource(BlogListResource, '/blogs')         
api.add_resource(CategoryListResource, '/categories/')
api.add_resource(CategoryResource, '/categories/<int:id>')      
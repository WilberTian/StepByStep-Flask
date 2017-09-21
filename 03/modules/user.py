from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/')
def admin_index():
	return 'Welcome user index page'
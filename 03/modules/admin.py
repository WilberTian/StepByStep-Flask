from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/')
def admin_index():
	return 'Welcome admin index page'
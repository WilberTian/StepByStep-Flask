from flask import Flask
from modules.admin import admin
from modules.user import user

app = Flask(__name__)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

app.run(debug=True)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///msk.db"
app.config['UPLOADED_PHOTOS_DEST'] = 'main/static/uploads'
app.config['SECRET_KEY'] = '41b861badaf7e71692ec3b89exit()'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # user password Hashing
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager. login_message_category = "info"

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from main import routes

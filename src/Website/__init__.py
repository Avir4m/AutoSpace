from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import timeago, datetime
from flask_socketio import SocketIO

from .func import get_secret_key

db = SQLAlchemy()
socketio = SocketIO()

DB_NAME = "database.db"
UPLOAD_FOLDER = "/src/website/static/images/upload_folder"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = get_secret_key()
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 1000 * 1000 * 16 # 16 Megabyte
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    socketio.init_app(app)
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .users import users
    from .posts import posts
    from .comments import comments
    from .spaces import spaces
    from .reports import reports
    from .chat import chat
    from .admin import admin

    from .errors import errors
    
    from .api import api
    
    app.register_blueprint(views, url_prefix='/') # views
    app.register_blueprint(auth, url_prefix='/') # auth
    app.register_blueprint(users, url_prefix='/') # users
    app.register_blueprint(posts, url_prefix='/') # posts
    app.register_blueprint(comments, url_prefix='/') # comments
    app.register_blueprint(spaces, url_prefix='/') # spaces
    app.register_blueprint(reports, url_prefix='/') # reports 
    app.register_blueprint(chat, url_prefix='/') # chats
    app.register_blueprint(admin, url_prefix='/admin') # admin
    
    app.register_blueprint(errors, url_prefix='/')
    
    app.register_blueprint(api, url_prefix='/api')
    
    from .models import User
    
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.template_filter('timeago')   
    def fromnow(date):
        return timeago.format(date, datetime.datetime.now())
    
    return app
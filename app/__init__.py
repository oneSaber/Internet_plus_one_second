from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
login_manager = LoginManager()


# 工厂函数
def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)
    login_manager.init_app(app)
    #注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint,url_prefix='/api')
    return app



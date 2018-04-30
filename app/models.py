from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from flask import current_app


#User Info
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    # role_id 用户角色
    # picture = db.relationship('Picture', backref='artist', lazy='dynamic')
    # star_pic 点赞图片
    # c_picture 收藏的图片
    # follow 关注的人
    # follwed 关注我的人

    # 用户具体信息，不用注册时填写，注册后用以修改信息
    # 用户的位置，可自填
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    age = db.Column(db.Integer)
    # 性别
    sex = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

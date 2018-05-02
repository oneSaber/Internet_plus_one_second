from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime

class Permission:
    FOLLOW = 1
    COLLECT = 2
    ARTIST = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=True, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COLLECT, Permission.ARTIST],
            'Artist': [Permission.FOLLOW, Permission.COLLECT, Permission.ARTIST, Permission.MODERATE],
            'Admin': [Permission.ADMIN, Permission.COLLECT, Permission.FOLLOW, Permission.MODERATE, Permission.ARTIST]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0


class Star(db.Model):
    __tablename__ = 'stars'
    staruser_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    starpic_id = db.Column(db.Integer, db.ForeignKey(
        'pictures.id'), primary_key=True)


class Collection(db.Model):
    __tablename__ = 'collections'
    collector_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), primary_key=True)
    collectedpic_id = db.Column(
        db.Integer, db.ForeignKey('pictures.id'), primary_key=True)


class Picture(db.Model):
    __tablename__ = 'pictures'
    id = db.Column(db.Integer, primary_key=True)
    picture_name = db.Column(db.String(64), index=True)
    artist_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    src = db.Column(db.String(64), index=True)
    startuser = db.relationship(
        'Star',
        foreign_keys = [
            Star.starpic_id,
            Star.staruser_id],
        backref=db.backref('starpic',lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    collector = db.relationship(
        'Collection',
        foreign_keys=[
            Collection.collector_id,
            Collection.collectedpic_id
        ],
        backref=db.backref(
            'collectionpic',
            lazy='joined'
        ),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # 图片的点赞数
    def star_count(self):
        return self.startuser.filter_by(staredpic_id=self.id).count()
    # 图片的被收藏数
    def collect_count(self):
        return self.collector.filter_by(collectedpic_id=self.id).count()

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

# User Info
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    # role_id 用户角色
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 用户上传的图片
    picture = db.relationship('Picture', backref='artist', lazy='dynamic')
    # star_pic 点赞图片
    starpic = db.relationship('Star',
                              foreign_keys=[Star.staruser_id],
                              backref=db.backref('staruser', lazy='joined'),
                              lazy='dynamic', cascade='all, delete-orphan')
    # c_picture 收藏的图片
    c_picture = db.relationship('Collection',
                                foreign_keys=[Collection.collector_id],
                                backref=db.backref('collector',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    # follow 关注我的人
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    # follwed 关注的人
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    # 用户具体信息，不用注册时填写，注册后用以修改信息
    # 用户的位置，可自填
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    age = db.Column(db.Integer)
    # 性别
    sex = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.phone_number in current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            else:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser

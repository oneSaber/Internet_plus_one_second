from ..models import User, AnonymousUser
from .. import app, db,login_manager
from . import main
from flask import request, make_response, jsonify
import json
from flask_login import logout_user, login_user,current_user,login_required

login_manager.login_view = 'main.login'
@main.route('/')
def index():
    User_num = len(User.query.all())
    if current_user.is_authenticated:
        return '<b>Hello {}</b>'.format(current_user.username)
    else:
        return '<b>Hello Stranger</b>'


@main.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.data)
        phone_number = data['phone_number']
        if User.query.filter_by(phone_number=phone_number).first() is None:
            username = data['username']
            password = data['password']
            user = User(phone_number=phone_number, username=username, password=password)
            db.session.add(user)
            try:
                db.session.commit()
                return jsonify({'message': 'successful'})
            except:
                return jsonify({'message': 'db error'})
        else:
            return jsonify({'message': 'phone used'})


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        phone_number = data['phone_number']
        password = data['password']
        user = User.query.filter_by(phone_number=phone_number).first()
        if user is None:
            return jsonify({'message': 'no user'})
        else:
            if password == user.password:
                login_user(user, data['remember_me'])
                return jsonify({'message': 'login successful'})
            else:
                return jsonify({'message': 'password wrong'})


@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'logout successful'})
from ..models import User
from .. import app, db
from . import api
from flask_login import login_required, current_user
from flask import request,jsonify
import json


@api.route('/user_info',methods=['POST'])
@login_required
def user_info():
    if request.method == 'POST':
        data = json.loads(request.data)
        phone_number = data['phone_number']
        user = User.query.filter_by(phone_number=phone_number).first()
        if user is not None:
            user.location = data['location']
            user.about_me = data['about_me']
            user.age = data['age']
            user.sex = data['sex']
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'edit successful'})
        return jsonify({'message': 'No user'}), 404

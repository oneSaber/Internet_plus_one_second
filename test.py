import requests
import json
se = requests.session()

def register_test():
    register_info = json.dumps({'phone_number': '18798318100', 'username': 'skil', 'password': '123456'})
    r = requests.post('http://127.0.0.1:5000/register', data=register_info)
    print(r.text)


def login_test():
    login_info = json.dumps({'phone_number':'18798318100', 'password': '123456', 'remember_me': 'True'})
    r = se.post('http://127.0.0.1:5000/login', data=login_info)
    print(r.text, r.cookies)
    return r.cookies


def Edit_test():
    cookies = login_test()
    index = se.get('http://127.0.0.1:5000/').text
    print(index)
    user_info = json.dumps({'phone_number': '18798318100', 'location': 'Beijing',
                            'about_me': 'player one', 'age': 24, 'sex': 'male'})
    r = se.post('http://127.0.0.1:5000/api/user_info', data=user_info)
    print(r.text)
    index = se.get('http://127.0.0.1:5000/').text
    print(index)

register_test()
Edit_test()
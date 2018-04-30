import requests
import json


def register_test():
    register_info = json.dumps({'phone_number': '18798318100', 'username': 'skil', 'password': '123456'})
    r = requests.post('http://127.0.0.1:5000/register', data=register_info)
    print(r.text)


def login_test():
    login_info = json.dumps({'phone_number':'18798318100', 'password': '123456', 'remember_me': 'True'})
    r = requests.post('http://127.0.0.1:5000/login', data=login_info)
    print(r.text, r.cookies)
    return r.cookies


def logout_test():
    cookies = login_test()
    r = requests.get('http://127.0.0.1:5000/logout',cookies=cookies)
    print(r.text)

logout_test()
from app.libs.redprint import Redprint
from flask import jsonify

api = Redprint('user')

@api.route('',methods=['GET'])
def get_user():
    user = {"name":"ycj"}
    return jsonify(user)
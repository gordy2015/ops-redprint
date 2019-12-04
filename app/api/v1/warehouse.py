from app.libs.redprint import Redprint
from flask import jsonify
from flask_restful import reqparse, marshal, fields
import time
from app.api.v1.models import db, Host

api = Redprint('warehouse')

@api.route('',methods=['GET'])
def gethost():
    w = Host.query.all()
    data = []
    for i in w:
        # print(i.bakname)
        data.append({"hostip": i.hostip, "dist": i.dist})
    return jsonify(data)


#虚拟机主机硬件配置，OS等记录
@api.route('/createhost', methods=['POST'])
def createhost():
    resource_field = {  # 先定义好返回哪些参数
        'hostip': fields.String,  # 参数的数据类型
        'hostname': fields.String,
        'dist': fields.String,
        'uname': fields.String,
        'sysdisk': fields.Integer,
        'datadisk': fields.Integer,
        'memtotal': fields.Integer,
        'cpucore': fields.Integer,
        'mark': fields.String,
        'addtime': fields.String
    }

    parser = reqparse.RequestParser()
    parser.add_argument('hostip', type=str)
    parser.add_argument('hostname', type=str)
    parser.add_argument('dist', type=str)
    parser.add_argument('uname', type=str)
    parser.add_argument('sysdisk', type=int)
    parser.add_argument('datadisk', type=int)
    parser.add_argument('memtotal', type=int)
    parser.add_argument('cpucore', type=int)
    parser.add_argument('mark', type=str)
    parser.add_argument('addtime', type=str)

    args = parser.parse_args(strict=True)
    # j = args.__repr__()
    data = {}
    for k, v in args.items():
        if k == "addtime":
            timeArray = time.localtime(int(v))
            v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data[k] = v
    # print(type(data),marshal(dic, resource_field))

    record = Host(hostip=data['hostip'], hostname=data['hostname'],dist=data['dist'],
                  uname=data['uname'], sysdisk=data['sysdisk'],datadisk=data['datadisk'],
                  memtotal=data['memtotal'], cpucore=data['cpucore'], mark=data['mark'], addtime=data['addtime'])
    print(record)
    try:
        db.session.add(record)
        db.session.commit()
        code = 200
        result = "SUCCESS"
    except:
        result = "FAILE"
        code = 600
    # res = result + jsonify(marshal(data, resource_field))
    return jsonify(marshal(data, resource_field))
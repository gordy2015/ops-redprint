from app.libs.redprint import Redprint
from flask import jsonify, request
from flask_restful import reqparse, marshal, fields, Resource
import time,sys
from app.api.v1.models import db, Host
from app.api.v1.args import HostArgs, DetailProcessArgs
from app.libs.tomongo import to_mongodb
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
@api.route('/checkhost', methods=['POST'])
def checkhost():
    args = HostArgs.dataparser()
    # j = args.__repr__()
    data = {}
    for k, v in args.items():
        if v:
            if k == "addtime":
                timeArray = time.localtime(int(v))
                v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            data[k] = v

    w = Host.query.filter_by(hostip=data['hostip'])
    if w.count() > 0:
        w.update(data)
        result = {"code":"200", "update":"%s %s"%(w.count(), data['hostip'])}
    else:
        # record = Host(hostip=data['hostip'], hostname=data['hostname'],dist=data['dist'],uname=data['uname'], sysdisk=data['sysdisk'],datadisk=data['datadisk'],memtotal=data['memtotal'], cpucore=data['cpucore'], mark=data['mark'], addtime=data['addtime'])
        record = Host(hostip=data['hostip'])
        try:
            db.session.add(record)
            db.session.commit()
            Host.query.filter_by(hostip=data['hostip']).update(data)
            result = {"code": "200", "create": "%s %s" % (w.count(), data['hostip'])}
        except:
            result = {"code": "600", "msg": "CREATE FAILE"}
    #jsonify(marshal(data, HostArgs.resource_field))
    return jsonify(result)


@api.route('/getmon',methods=['GET'])
def getmon():
    result = to_mongodb.find_one({"user" : "rpc"})
    print(type(result))
    return "abc2"


@api.route('/createdetail',methods=['POST'])
def createdetail():
    # args = DetailProcessArgs.dataparser()
    # data = {}
    # for k, v in args.items():
    #     if v:
    #         if k == "addtime":
    #             timeArray = time.localtime(int(v))
    #             v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    #         data[k] = v

    data = request.json.get('data')
    r = request.args.get('data')
    print(type(data))
    print(type(r ),r)
    # for i in data:
    #     print(i)
    #result = to_mongodb.insert_one(data)
    result = "abc2"
    return result
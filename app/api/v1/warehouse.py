from app.libs.redprint import Redprint
from flask import jsonify
from flask_restful import reqparse, marshal, fields, Resource
import time,sys
from app.api.v1.models import db, Host
from app.api.v1.args import HostArgs

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
    args = HostArgs.hostparser()
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
        return jsonify(result)
    else:
        record = Host(hostip=data['hostip'], hostname=data['hostname'],dist=data['dist'],uname=data['uname'], sysdisk=data['sysdisk'],datadisk=data['datadisk'],memtotal=data['memtotal'], cpucore=data['cpucore'], mark=data['mark'], addtime=data['addtime'])
        try:
            db.session.add(record)
            db.session.commit()
            code = 200
            result = "SUCCESS"
        except:
            result = "FAILE"
            code = 600
    return jsonify(marshal(data, HostArgs.resource_field))
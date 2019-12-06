from app.libs.redprint import Redprint
from flask import jsonify, request
from flask_restful import reqparse, marshal, fields, Resource
import time, sys, json
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
    data = data.replace('[', '').replace(']', '')
    # print(type(data), data)
    data = data.split('},')
    print(type(data), data)
    newlist = []
    for i in data:
        if not i.endswith('}'):
            i = i + '}'
            # newline = json.loads(newline.replace('\'','\"'))
        newlist.append(i)
    print("---------",type(newlist), json.loads(newlist[0].replace('\'','\"'))['hostip'])
    getip = json.loads(newlist[0].replace('\'','\"'))['hostip']
    result = to_mongodb.update_many({"hostip": getip}, {'$set': {"latest": "0"}})
    print("+++++++++++++++",result)
    for i in newlist:
        print(type(i),i)
        record = json.loads(i.replace('\'','\"'))
        # print("**********",type(record), record['port'])

        print("**********", result)
        w = to_mongodb.find({"hostip":record['hostip'],"port":record["port"],"protocol":record["protocol"],"pid":record["pid"],"process":record["process"]})
        if w.count() == 0:
            record['change'] = "0"

            result = to_mongodb.insert_one(record)
            print("===========",result)
        else:
            print(w.count())
            i = to_mongodb.find_one({"hostip":record['hostip'],"port":record["port"],"protocol":record["protocol"],"pid":record["pid"],"process":record["process"]})
            a = to_mongodb.find({"hostip": record['hostip'], "port": record["port"], "protocol": record["protocol"],"pid": record["pid"], "process": record["process"], "process_cpu_usage":record["process_cpu_usage"], "process_mem_usage":record["process_mem_usage"]})

            if a.count() == 0:
                newchange = str(int(i["change"]) + int(1))
            else:
                newchange = i["change"]
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&", newchange)
            result = to_mongodb.update_one({"hostip":record['hostip'],"port":record["port"],"protocol":record["protocol"],"pid":record["pid"],"process":record["process"]}, {'$set': {"latest": "1", "process_cpu_usage":record["process_cpu_usage"], "process_mem_usage":record["process_mem_usage"], "change":newchange}})
            print("**********", result)


    # result = to_mongodb.insert_many(newlist)
    # print(result)
    return "abc2"
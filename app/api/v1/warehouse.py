from app.libs.redprint import Redprint
from flask import jsonify, request
from flask_restful import reqparse, marshal, fields, Resource
import time, sys, json
from app.api.v1.models import db, Host
from app.api.v1.args import HostArgs
from app.libs.tomongo import to_mongodb, to_mongodb_ports
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
    data = request.json.get('data')
    data = data.split('},')
    # print(type(data), data)

    #取hostip，并在开始前更新老的state为0
    data1 = data[0]
    if not data1.endswith('}'):
        data1 = data1 + '}'
    if data1.startswith('[{'):
        data1 = data1.split('[')[1]
    if data1.endswith(']}'):
        data1 = data1.split(']')[0]

    #获取hostip
    getip = json.loads(data1.replace('\'','\"'))['hostip']

    #开始前，把老的所有记录的state更新为0
    result = to_mongodb.update_many({"hostip": getip}, {'$set': {"state": "0"}})

    #逐个对比后insert，若有老的记录存在，state更新为1，不存在继续为0
    for i in data:
        if not i.endswith('}'):
            i = i + '}'
        if i.startswith('[{'):
            i = i.split('[')[1]
        if i.endswith(']}'):
            i = i.split(']')[0]
        # print("========",type(i),type(json.loads(i.replace('\'','\"'))))
        record = json.loads(i.replace('\'','\"'))

        w = to_mongodb.find(
            {"hostip": record['hostip'], "port": record["port"], "protocol": record["protocol"], "pid": record["pid"],
             "process": record["process"]})
        if w.count() == 0:
            record['change_usage'] = "0"
            record['change_state'] = "0"
            record['check_state'] = "1"
            # record['checktime'] = record['addtime']
            result = to_mongodb.insert_one(record)
            # print("===========", result)
        else:
            # print(w.count())
            getlast = to_mongodb.find_one(
                {"hostip": record['hostip'], "port": record["port"], "protocol": record["protocol"], "pid": record["pid"],
                "process": record["process"]})

            #对比CPU和内存使用率
            diffusage = to_mongodb.find(
                {"hostip": record['hostip'], "port": record["port"], "protocol": record["protocol"], "pid": record["pid"],
                 "process": record["process"], "process_cpu_usage": record["process_cpu_usage"],
                 "process_mem_usage": record["process_mem_usage"]})
            # print(a.count())

            # 若有cpu或内存使用率的变更，change_usage值加1
            newchange_usage = getlast["change_usage"]
            if diffusage.count() == 0:
                newchange_usage = str(int(getlast["change_usage"]) + int(1))

            #对比上次的check_state，如果上次为0，则change_state值加1
            newchange_state = getlast['change_state']
            # print("------>", getlast['check_state'])
            if getlast["check_state"] == "0":
                newchange_state = str(int(getlast['change_state']) + int(1))

            newcheck_state = "1"

            result = to_mongodb.update_one(
                {"hostip": record['hostip'], "port": record["port"], "protocol": record["protocol"], "pid": record["pid"],
                 "process": record["process"]}, {'$set': {"state": "1", "process_cpu_usage": record["process_cpu_usage"],
                                                          "process_mem_usage": record["process_mem_usage"],
                                                          "change_usage": newchange_usage, "checktime": record['checktime'],
                                                          "change_state": newchange_state, "check_state": newcheck_state}})
            # print("**********", result)

    #最后检查state为0的
    checkdown = to_mongodb.find(
        {"hostip": record['hostip'], "state": "0"})
    for i in checkdown:
        # print(i)
        #对比上次的check_state，如果上次为1，则change_state值加1
        newchange_state = i["change_state"]
        # print("======>", i['check_state'])
        if i['check_state'] == "1":
            newchange_state = str(int(i["change_state"]) + int(1))
        to_mongodb.update_one({"hostip": getip, "state": "0", "port": i["port"], "protocol": i["protocol"], "pid": i["pid"],
                 "process": i["process"]}, {'$set': {"check_state": "0", "change_state": newchange_state}})

    # sys.exit()

    return "detailprocess"


@api.route('/hostports',methods=['POST'])
def hostports():
    hostip = request.json.get('hostip')
    #有传入ip则只查传入IP的所有端口返回，没传入ip则查全部IP的所有端口记录到mongodb
    if hostip:
        data = to_mongodb.find({"hostip": hostip, "state": "1"})
        # print(data.count())
        ports = []
        for i in data:
            result = i['port']
            # print(type(result), result)
            if result not in ports:
                ports.append(result)

        ports = ", ".join(ports)
        result = hostip + ": " + ports
    else:
        data = to_mongodb.find()
        # print(data.count())
        ip = []
        for i in data:
            result = i['hostip']
            if result not in ip:
                ip.append(result)

        for i in ip:
            data = to_mongodb.find({"hostip": i, "state": "1"})
            print(data.count())
            ports = []
            for m in data:
                result = m['port']
                # print(type(result), result)
                if result not in ports:
                    ports.append(result)
            ports = ", ".join(ports)
            result = i + ": " + ports
            # print(type(i), type(ports), i, ports)

            record = {"hostip":i, "ports":ports}
            # print(type(record),record)
            s = to_mongodb_ports.find(record)
            if s.count() == 0:
                to_mongodb_ports.delete_one({"hostip":i})
                result = to_mongodb_ports.insert_one(record)
    return "hostports"


#根据ip和端口查此端口的详细信息（prometheus-pushgateway格式)
@api.route('/hostportdetail',methods=['POST'])
def hostportdetail():
    hostip = request.json.get('hostip')
    port = request.json.get('port')
    data = to_mongodb.find({"hostip": hostip, "port": port})
    # print(data.count())
    portdetail = []
    for i in data:
        result = 'ports{user="%s", process="%s", pid="%s", port="%s", addtime="%s"} %s'%(i['user'], i['process'], i['pid'], i['port'], i['addtime'], i['state'])
        # print(type(result), result)
        if result not in portdetail:
            portdetail.append(result)
        portdetail = "\\n".join(portdetail)
    return portdetail
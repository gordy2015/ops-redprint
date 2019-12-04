# from flask import Blueprint
import json, time, sys, os
from flask import jsonify
from flask_restful import reqparse, Resource
from flask_restful import fields, marshal_with, marshal
from app.libs.redprint import Redprint
from app.api.v1.models import db, Dbbak, Myrestore, Morestore
from app.api.v1.args import DbbakArgs, MyrestoreArgs, MorestoreArgs

api = Redprint('dbjob')


@api.route('/getdbbak',methods=['GET'])
def getdbbak():
    w = Dbbak.query.all()
    data = []
    for i in w:
        # print(i.bakname)
        data.append({"ip":i.ip, "bakname":i.bakname})
    return jsonify(data)


@api.route('/getmyrestore', methods=['GET'])
def getmyrestore():
    w = Myrestore.query.all()
    data = []
    for i in w:
        data.append({"restorefile":i.restorefile, "sqllines":i.sqllines})
    return jsonify(data)


#Mysql备份记录
@api.route('/createdbbak', methods=['POST'])
def createdbbak():
    args = DbbakArgs.dbbakparser()
    # j = args.__repr__()
    data = {}
    for k,v in args.items():
        if k == "starttime" or k == "stoptime":
            timeArray = time.localtime(int(v))
            v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data[k] = v
    # print(type(data),marshal(dic, resource_field))

    record = Dbbak(ip=data['ip'],bakname=data['bakname'], bakdir=data['bakdir'], md5sum=data['md5sum'], filesize=data['filesize'], starttime=data['starttime'],
                             stoptime=data['stoptime'], costtime=data['costtime'], baktype=data['baktype'], has_restore=data['has_restore'], incsize=data['incsize'], to_f01_costtime=data['to_f01_costtime'], to_f01=data['to_f01'], mark=data['mark'], dbname=data['dbname'])
    # print(record)
    try:
        db.session.add(record)
        db.session.commit()
        code = 200
        result = "SUCCESS"
    except:
        result = "FAILE"
        code = 600
    # res = result + jsonify(marshal(data, resource_field))
    return jsonify(marshal(data, DbbakArgs.resource_field))


#MySQL还原记录
@api.route('/createmyrestore', methods=['POST'])
def createmyrestore():
    args = MyrestoreArgs.myrestoreparser()
    data = {}
    for k,v in args.items():
        # print('=======',k,v)
        if k == "starttime" or k == "stoptime":
            timeArray = time.localtime(int(v))
            v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data[k] = v
    print(data)

    record = Myrestore(restorefile=data['restorefile'],dbname=data['dbname'], data_length=data['data_length'], index_data_length=data['index_data_length'], sqllines=data['sqllines'], starttime=data['starttime'],
                             stoptime=data['stoptime'], costtime=data['costtime'])
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
    return jsonify(marshal(data, MyrestoreArgs.resource_field))


#Mongodb还原记录
@api.route('/createmorestore', methods=['POST'])
def createmorestore():
    args = MorestoreArgs.morestoreparser()
    data = {}
    for k,v in args.items():
        if k == "starttime" or k == "stoptime":
            timeArray = time.localtime(int(v))
            v = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        data[k] = v
    # print(type(data),marshal(dic, resource_field))

    record = Morestore(restorefile=data['restorefile'], kj_count=data['kj_count'], kj_storagesize=data['kj_storagesize'], starttime=data['starttime'], stoptime=data['stoptime'], costtime=data['costtime'])
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
    return jsonify(marshal(data, MorestoreArgs.resource_field))
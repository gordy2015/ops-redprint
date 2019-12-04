
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Dbbak(db.Model):
    __tablename__ = 'ops_dbbak'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ip = db.Column(db.String(20))
    bakname = db.Column(db.String(50))
    bakdir = db.Column(db.String(150))
    md5sum = db.Column(db.String(50))
    filesize = db.Column(db.BigInteger)
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    costtime = db.Column(db.Integer)
    baktype = db.Column(db.Integer,default=1) #1全量 0增量
    incsize = db.Column(db.BigInteger,nullable=True)
    has_restore = db.Column(db.Integer,default=0) #1有定期还原 0无还原
    to_f01 = db.Column(db.Integer) #1成功 0失败
    to_f01_costtime = db.Column(db.BigInteger,nullable=True)
    mark = db.Column(db.String(20))
    dbname = db.Column(db.String(20))


class Morestore(db.Model):
    __tablename__ = 'ops_morestore'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    restorefile = db.Column(db.String(150))
    kj_count = db.Column(db.Integer)
    kj_storagesize = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    costtime = db.Column(db.Integer)


class Myrestore(db.Model):
    __tablename__ = 'ops_myrestore'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    restorefile = db.Column(db.String(150))
    dbname = db.Column(db.String(20))
    data_length = db.Column(db.Integer)
    index_data_length = db.Column(db.Integer)
    sqllines =db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    stoptime = db.Column(db.DateTime)
    costtime = db.Column(db.Integer)


class Map(db.Model):
    __tablename__ = 'ops_map'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    mark = db.Column(db.String(40))
    access = db.Column(db.String(40))
    ext_ip = db.Column(db.String(40))
    ext_port = db.Column(db.String(30))
    int_ip = db.Column(db.String(40))
    int_port = db.Column(db.String(10))
    is_proxy = db.Column(db.Integer)
    realip = db.Column(db.String(40))
    is_used = db.Column(db.Integer)
    addtime = db.Column(db.DateTime)


class Host(db.Model):
    __tablename__ = 'ops_host'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    hostip = db.Column(db.String(40))
    hostname = db.Column(db.String(30))
    dist = db.Column(db.String(30))
    uname = db.Column(db.String(60))
    sysdisk =db.Column(db.Integer)
    datadisk = db.Column(db.Integer)
    memtotal = db.Column(db.DateTime)
    cpucore = db.Column(db.Integer)
    mark = db.Column(db.String(50))
    addtime = db.Column(db.DateTime)



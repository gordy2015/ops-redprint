from flask_restful import reqparse, fields

class DbbakArgs(object):
    resource_field = {  # 先定义好返回哪些参数
        'ip': fields.String,  # 参数的数据类型
        'bakname': fields.String,
        'bakdir': fields.String,
        'md5sum': fields.String,
        'filesize': fields.Integer,
        'starttime': fields.String,
        'stoptime': fields.String,
        'costtime': fields.Integer,
        'baktype': fields.String,
        'incsize': fields.Integer,
        'has_restore': fields.Integer,
        'to_f01': fields.Integer,
        'to_f01_costtime': fields.Integer,
        'mark': fields.String,
        'dbname': fields.String,
    }
    def dataparser():
        parser = reqparse.RequestParser()
        parser.add_argument('ip', type=str, help='ip must x.x.x.x')
        parser.add_argument('bakname', type=str)
        parser.add_argument('bakdir', type=str)
        parser.add_argument('md5sum', type=str)
        parser.add_argument('filesize', type=int)
        parser.add_argument('starttime', type=str)
        parser.add_argument('stoptime', type=str)
        parser.add_argument('costtime', type=int)
        parser.add_argument('baktype', type=int)
        parser.add_argument('incsize', type=int)
        parser.add_argument('has_restore', type=int)
        parser.add_argument('to_f01', type=int)
        parser.add_argument('to_f01_costtime', type=int)
        parser.add_argument('mark', type=str)
        parser.add_argument('dbname', type=str)
        return parser.parse_args(strict=True)


class MyrestoreArgs(object):
    resource_field = {  # 先定义好返回哪些参数
        'restorefile': fields.String,  # 参数的数据类型
        'dbname': fields.String,
        'data_length': fields.Integer,
        'index_data_length': fields.Integer,
        'sqllines': fields.Integer,
        'starttime': fields.String,
        'stoptime': fields.String,
        'costtime': fields.Integer
    }
    def dataparser():
        parser = reqparse.RequestParser()
        parser.add_argument('restorefile', type=str)
        parser.add_argument('dbname', type=str)
        parser.add_argument('data_length', type=int)
        parser.add_argument('index_data_length', type=int)
        parser.add_argument('sqllines', type=int)
        parser.add_argument('starttime', type=str)
        parser.add_argument('stoptime', type=str)
        parser.add_argument('costtime', type=int)
        return parser.parse_args(strict=True)


class MorestoreArgs(object):
    resource_field = {  # 先定义好返回哪些参数
        'restorefile': fields.String,  # 参数的数据类型
        'kj_count': fields.Integer,
        'kj_storagesize': fields.Integer,
        'starttime': fields.String,
        'stoptime': fields.String,
        'costtime': fields.Integer
    }
    def dataparser():
        parser = reqparse.RequestParser()
        parser.add_argument('restorefile', type=str)
        parser.add_argument('kj_count', type=int)
        parser.add_argument('kj_storagesize', type=int)
        parser.add_argument('starttime', type=str)
        parser.add_argument('stoptime', type=str)
        parser.add_argument('costtime', type=int)
        return parser.parse_args(strict=True)


class HostArgs(object):
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
    def dataparser():
        parser = reqparse.RequestParser()
        parser.add_argument('hostip', type=str, required=True)
        parser.add_argument('hostname', type=str)
        parser.add_argument('dist', type=str)
        parser.add_argument('uname', type=str)
        parser.add_argument('sysdisk', type=int)
        parser.add_argument('datadisk', type=int)
        parser.add_argument('memtotal', type=int)
        parser.add_argument('cpucore', type=int)
        parser.add_argument('mark', type=str)
        parser.add_argument('addtime', type=str)
        return parser.parse_args(strict=True)


#用不上，使用request.json.get获取了post数据
# class DetailProcessArgs(object):
    # resource_field = {  # 先定义好返回哪些参数
    #     'hostip': fields.String,  # 参数的数据类型
    #     'user': fields.String,
    #     'pid': fields.Integer,
    #     'protocol': fields.String,
    #     'port': fields.Integer,
    #     'process': fields.String,
    #     'process_cpu_usage': fields.Float,
    #     'process_mem_usage': fields.Float,
    #     'latest': fields.Integer,
    #     'addtime': fields.String
    # }
    # def dataparser():
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('hostip', type=str, required=True)
    #     parser.add_argument('user', type=str)
    #     parser.add_argument('pid', type=int)
    #     parser.add_argument('protocol', type=str)
    #     parser.add_argument('port', type=int)
    #     parser.add_argument('process', type=str)
    #     parser.add_argument('process_cpu_usage', type=float)
    #     parser.add_argument('process_mem_usage', type=float)
    #     parser.add_argument('latest', type=int)
    #     parser.add_argument('addtime', type=str)
    #     return parser.parse_args(strict=True)

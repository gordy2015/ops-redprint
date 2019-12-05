from app.app import create_app
from flask_restful import Api, Resource
# from flask_pymongo import PyMongo

# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from app.api.v1.models import db, Dbbak, Myrestore, Host, Map

app = create_app()
api = Api(app)
#mongo = PyMongo(app)

#flask-admin
# admin = Admin(app, name='ops', template_mode='bootstrap3')
# dbs = [Dbbak, Myrestore, Host, Map]
# admin.add_view(ModelView(Dbbak, db.session, name="Mysql", category="数据库备份"))
# admin.add_view(ModelView(Myrestore, db.session, name="Mysql", category="数据库还原"))
# admin.add_view(ModelView(Host, db.session, name="主机信息", category="运维信息记录"))
# admin.add_view(ModelView(Map, db.session, name="公网映射", category="运维信息记录"))

if __name__ == '__main__':
    app.run(host="0.0.0.0")


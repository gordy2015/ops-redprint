from flask import Blueprint
from app.api.v1 import user, dbjob, warehouse


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    dbjob.api.register(bp_v1)
    warehouse.api.register(bp_v1)

    return bp_v1

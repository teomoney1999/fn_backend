from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager

from application.models.model import Transaction


async def pre_create_transaction(request=None, data=None, **kw): 
    # print("data", data)
    pass


async def post_create_transaction(request=None, result=None, **kw): 
    # print("result", result)
    pass

async def pre_get_transaction(request, data=None, **kw): 
    pass


apimanager.create_api(collection_name='transaction', model=Transaction,
                      methods=['GET', 'POST', 'DELETE', 'PUT'],
                      url_prefix='/api/v1',
                      preprocess=dict(GET_SINGLE=[pre_get_transaction], GET_MANY=[pre_get_transaction], POST=[pre_create_transaction], PUT_SINGLE=[]),
                      postprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[post_create_transaction], PUT_SINGLE=[])
                      )
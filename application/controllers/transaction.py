from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager

from application.models.model import Transaction

# GET
async def pre_get_transaction(request=None, search_params=None, **kw): 
    user_id = request.args.get('user_id')
    if user_id:
        search_params['filters'] = {"user_id": {"$eq" : user_id}}


apimanager.create_api(collection_name='transaction', model=Transaction,
                      methods=['GET', 'POST', 'DELETE', 'PUT'],
                      url_prefix='/api/v1',
                      preprocess=dict(GET_SINGLE=[], GET_MANY=[pre_get_transaction], POST=[], PUT_SINGLE=[]),
                      postprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[], PUT_SINGLE=[])
                      )
from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager

from application.models.model import Balance

async def pre_get_many_balance(request=None, search_params=None, **kw): 
    # GET THE CURRENT BALANCE 
    # TODO: NEED TO SAVE CURRENT BALANCE IN REDIS SERVER TO INCREASE PERFORMANCE
    get_latest = request.args.get("get_latest")
    if get_latest: 
        # EXPENSIVE OPERATION
        current_balance = db.session.query(Balance).order_by(Balance.created_at.desc()).first()
        if current_balance: 
            search_params['filters'] = {"id": {"$eq": current_balance.id}}
        else: 
            return json({"error_code": "PARAM_ERROR", "error_message": "Không có dữ liệu"}, status=520)


async def pre_post_balance(request=None, data=None, **kw): 
    print('\ndata', data)

apimanager.create_api(collection_name='balance', model=Balance,
                      methods=['GET', 'POST', 'DELETE', 'PUT'],
                      url_prefix='/api/v1',
                      preprocess=dict(GET_SINGLE=[], GET_MANY=[pre_get_many_balance], POST=[pre_post_balance], PUT_SINGLE=[]),
                      )
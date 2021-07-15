from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager

from application.models.model import User, Role, UserInfo, Balance

from .helpers.auth_helper import generator_salt
from .helpers.format_helper import to_dict

from application.config import Message

@app.route("/user_test")
async def user_test(request):
    return text("user_test api")

@app.route("/api/v1/login", methods=["POST", "GET"])
async def user_login(request):
    param = request.json
    username = param.get("username")
    password = param.get("password")
    if (username is not None) and (password is not None):
        user = db.session.query(User).filter(User.username == username).first()
        if (user is not None) and auth.verify_password(password, user.password, user.salt):
            auth.login_user(request, user)

            return json({"id": str(user.id), "username": user.username})
        return json({"error_code": "LOGIN_FAILED","error_message": Message.LOGIN_FAILED}, status=520)

    else:
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)
    return text("user_login api")

@app.route("/user/logout", methods=["GET"])
async def user_logout(request):
    auth.logout_user(request)
    return json({})

@app.route("/api/v1/current_user", methods=["GET"])
async def user_current_user(request):
    token = request.args.get('token')
    print("===token", token)
    if token: 
        curr_user = db.session.query(UserInfo).filter(UserInfo.user_id == token).first()
        if curr_user: 
            print(to_dict(curr_user))
            return json({
                # "email": curr
            })
            return json(to_dict(curr_user))
        # return 

    # user = User.query.filter(User.id == user_id).first()
    # if user is not None:
    #     return json({"id": str(user.id), "username": user.username})
    # else:
    #     return json({"error_code": "NOT_FOUND", "error_message": "User not found"}, status=520)
    # return json({"error_code": "UNKNOWN", "error_message": "Unknown error"}, status=520)



async def pre_create_user(request=None, data=None, **kw): 
    print("data", data)
    # Roles
    role_user = Role.query.filter(Role.name == "user").first(); 
    if "roles" in data:
        roles_list = []   
        if len(data["roles"]) == 0:
            #  default account has role user
            roles_list.append(role_user)

        for role in data['roles']: 
            if role['name'] == role_user.name: 
                roles_list.append(role_user)
        
        data['roles'] = roles_list
    else: 
        data['roles'] = [role_user]
    
    # Encrypt password
    if "password" in data and data["password"] is not None: 
        data["salt"] = generator_salt()
        data["password"] = auth.encrypt_password(data["password"], data["salt"])
    

    print("CREATED USER", data)
    

async def post_create_user(request=None, result=None, **kw): 
    # CREATE USER INFO
    print("POST CREATE USER")
    info = request.json.get('info')
    print("info", info)
    if info:
        # for item in info: 
        user_info = UserInfo()

        for key in info: 
            if hasattr(user_info, key): 
                setattr(user_info, key, item.get(key))
        
        user_info.user_id = result.get("id")

        db.session.add(user_info) 
        db.session.flush()

        print("USER INFO IS CREATED")


    # CREATE BALANCE
    user_id = result.get("id")

    balance = Balance()

    balance.amount = 0
    balance.user_id = user_id

    db.session.add(balance)
    db.session.flush()

    db.session.commit()

    print("BALANCE IS CREATED, AMOUNT: 0")

apimanager.create_api(collection_name='user', model=User,
                      methods=['GET', 'POST', 'DELETE', 'PUT'],
                      url_prefix='/api/v1',
                      preprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[pre_create_user], PUT_SINGLE=[]),
                      postprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[post_create_user], PUT_SINGLE=[]),
                      exclude_columns=["password", "salt"]
                      )


apimanager.create_api(collection_name="role", model= Role,
                      methods=["GET", "POST", "DELETE", "PUT"],
                      url_prefix="/api/v1",
                      preprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[], PUT_SINGLE=[]),
                      postprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[], PUT_SINGLE=[])                
                      )


async def post_create_userinfo(request=None, result=None, **kw): 
    print("result", result)
    # Excluding columns
    exclude_columns = ["password", "salt"]
    if "user" in result:
        user = result["user"]
        for col in exclude_columns: 
            if col in user: 
                del user[col]
    
async def pre_get_userinfo(request=None, search_params=None, **kw): 
    token = request.args.get('token')
    # print("request", request.headers)
    if token: 
        user_info = UserInfo.query.filter(UserInfo.user_id == token).first()
        search_params['filter'] = {"id": {"$eq" : user_info.id}}

async def post_get_userinfo(request=None, result=None, **kw): 
    # Excluding columns
    exclude_columns = ["password", "salt"]
    user_info = result.get('objects')
    if user_info: 
        for info in user_info: 
            if "user" in info:
                user = info["user"]
                for col in exclude_columns: 
                    if col in user: 
                        del user[col]
    

apimanager.create_api(collection_name='userinfo', model=UserInfo,
                      methods=['GET', 'POST', 'DELETE', 'PUT'],
                      url_prefix='/api/v1',
                      preprocess=dict(GET_SINGLE=[], GET_MANY=[], POST=[], PUT_SINGLE=[]),
                      postprocess=dict(GET_SINGLE=[], GET_MANY=[post_get_userinfo], POST=[post_create_userinfo], PUT_SINGLE=[])
                      )
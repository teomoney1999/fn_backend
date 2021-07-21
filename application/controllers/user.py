from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager

from application.models.model import User, Role, Balance

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
        curr_user = db.session.query(User).filter(User.user_id == token).first()
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

exclude_columns = ["password", "salt"]
# POST
async def pre_create_user(request=None, data=None, **kw): 
    # Roles
    role_user = Role.query.filter(Role.name == "user").first(); 
    # default account has role user
    if "roles" not in data: 
        data['roles'] = [role_user]
     
    # Password
    if "password" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)

    if len(data["password"]) < 5: 
        return json({"error_code": "PARAM_ERROR", "error_message": "Mật khẩu có định dạng chưa đúng"}, status=520)

    data["salt"] = generator_salt()
    data["password"] = auth.encrypt_password(data["password"], data["salt"])
    
    # Username
    if "username" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)

    if len(data["username"]) < 5: 
        return json({"error_code": "PARAM_ERROR", "error_message": "Tên đăng nhập có định dạng chưa đúng"}, status=520)

    checking_duplicate_user = db.session.query(User).filter(User.username == data['username']).first()
    print("checking_duplicate_user", checking_duplicate_user)
    if checking_duplicate_user: 
        return json({"error_code": "PARAM_ERROR", "error_message": "Tên đăng nhập không được trùng nhau"}, status=520)

    if "fullname" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)

    if "gender" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)

    # Email
    if "email" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)
    
    email_checking = db.session.query(User).filter(User.email == data['email']).first()
    if email_checking: 
        return json({"error_code": "PARAM_ERROR", "error_message": "Email không được trùng nhau"}, status=520)

    # Phone
    if "phone" not in data: 
        return json({"error_code": "PARAM_ERROR", "error_message": Message.PARAM_ERROR}, status=520)

    phone_checking = db.session.query(User).filter(User.phone == data['phone']).first()
    if phone_checking: 
        return json({"error_code": "PARAM_ERROR", "error_message": "Số điện thoại không được trùng nhau"}, status=520)

    
async def post_create_user(request=None, result=None, **kw): 
    user_id = result.get('id')

    # CREATE BALANCE
    balance = Balance()

    balance.amount = 0
    balance.is_current = True
    balance.user_id = user_id

    db.session.add(balance)
    db.session.flush()

    print("BALANCE IS CREATED, AMOUNT: 0")

    db.session.commit()
# PUT

# GET
def pre_get_many_user(request=None, search_params=None, **kw): 
    pass

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
# POST
async def pre_create_user(request=None, data=None, **kw): 
    pass

# PUT

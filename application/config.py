class Config(object):
    DEBUG = True
    STATIC_URL = "static"
    SQLALCHEMY_DATABASE_URI = 'postgresql://financial_management_user:123456abcA@localhost:5432/financial_management_db'
    AUTH_LOGIN_ENDPOINT = 'login'
    AUTH_PASSWORD_HASH = 'sha512_crypt'
    AUTH_PASSWORD_SALT = 'ruewhndjsa17heaw'
    SECRET_KEY = 'e2q8dhaushdauwd7qye'
    SESSION_COOKIE_SALT = 'dhuasud819wubadhysagd'


class Message(object): 
    LOGIN_FAILED = "Tài khoản không tồn tại hoặc thông tin đăng nhập không đúng"
    PARAM_ERROR = "Vui lòng kiểm tra lại thông tin trước khi lưu"

class AuthMessage(object): 
    PASSWORD_LENGTH_ERROR = "", 
    USERNAME_DUPLICATION_ERROR = "",
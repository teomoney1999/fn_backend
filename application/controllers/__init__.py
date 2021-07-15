# Register Blueprints/Views.
from gatco.response import text, json
from application.extensions import jinja

def init_views(app):
    import application.controllers.user
    import application.controllers.balance
    import application.controllers.transaction

    
    # @app.route('/')
    # def index(request):
    #     #return text("Index")
    #     return jinja.render('index.html', request)
    
    
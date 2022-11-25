import os
from flask import Flask
from . import db, auth, blog

# we create application factory function

def create_app():
    # create and configure the app
    # instance_relative_config if True, it tells app that conf file relative to instance folder 
    # we take secret_key from instance folder, so if instance_relative_config is False, app will not able check instance folder for secret key
    app = Flask(__name__, instance_relative_config=True)

    # update some default configuration which app will use like database path, ignores if not upper case
    app.config.from_mapping(
        # inside instance folder creates flaskr.sqlite for storing db
        # app.instance_path, it is path to instance folder , it doesn't matter we created instance folder or not
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # this method will get config thing like secretkey, API key and others from instance folder config.py, if it dosn't exit, silent=True will not create error
    app.config.from_pyfile('config.py', silent=True)
   

    # this will ensure that instance folder created
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

   
    # we call this function in order register some commmand with app
    db.init_app(app)
    
    # we register auth blueprint and blog blueprint to app
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    # blog doesnt have url_prefix, so we use add_url_rule, in order to create url and which index view's url will be this url,
    # url_for('index') and url_for('blog.index') urls will be '/' 
    app.add_url_rule('/', endpoint='index')

    return app
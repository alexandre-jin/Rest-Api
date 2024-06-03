from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'test123'
    app.config['MYSQL_DB'] = 'ecommerce'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    mysql.init_app(app)
    
    from app.users.routes import users
    from app.products.routes import products
    from app.carts.routes import carts
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(carts)
    
    return app

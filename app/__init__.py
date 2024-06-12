from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # local test
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'root'
    # app.config['MYSQL_PASSWORD'] = 'test123'
    # app.config['MYSQL_DB'] = 'ecommerce'
    # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    # global test 
    # app.config['MYSQL_HOST'] = 'votre-serveur-mariadb' 
    # app.config['MYSQL_PORT'] = 3306  # Le port par défaut de MariaDB est 3306
    # app.config['MYSQL_USER'] = 'votre-utilisateur' 
    # app.config['MYSQL_PASSWORD'] = 'votre-mot-de-passe'
    # app.config['MYSQL_DB'] = 'Nom_de_la_DB'  
    # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    mysql.init_app(app)
    
    from app.users.routes import users
    from app.products.routes import products
    from app.carts.routes import carts
    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(carts)
    
    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS


# load_dotenv(find_dotenv())

app = Flask(__name__)

# recursos = {   
#             r"/leads/*": {"origins":"*"},
#             # r"/leads/*": {"origins": "https://www.vizilotes.com.br/"},
#             r"/empreendimento/*":{"origins":"*"}
#             }


# cors = CORS(app, resources=recursos)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(os.getenv('login_sql_tech'), os.getenv('senha_sql_tech'), os.getenv('host_sql_tech'), os.getenv('database_sql_tech'))
# app.config['SQLALCHEMY_BINDS'] = {
#     'gc':        'postgresql://{}:{}@{}/{}'.format(os.getenv('login_sql_gc'), os.getenv('senha_sql_gc'), os.getenv('host_sql_gc'), os.getenv('database_sql_gc'))
# }
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


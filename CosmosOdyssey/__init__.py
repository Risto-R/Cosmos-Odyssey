from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from CosmosOdyssey.Config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE
db = SQLAlchemy(app)
from CosmosOdyssey import routes

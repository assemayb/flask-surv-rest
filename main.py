import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
import routes, models
migrate = Migrate(app, db)

from flask import Flask
from os import getenv

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
app.secret_key = getenv("SECRET_KEY")

import routes


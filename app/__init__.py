import os
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super_clave_secreta_bookhub")

bcrypt = Bcrypt(app)
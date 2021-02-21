#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:35:49 2020

@author: jbt
"""

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import LoginManager
from dotenv import load_dotenv
import os

### imports modules
try:
    import sys
    sys.path.append('..') #Permet d'acceder aux dossiers parents
    from config.config import (
        mon_email,
        mon_password_email,
        utilisateur,
        mot_de_passe,
        nom_bdd,
        le_host,
        le_port,
        l_URI,
        CLE_SECRETE)
except:
    from config.config import (
        mon_email,
        mon_password_email,
        utilisateur,
        mot_de_passe,
        nom_bdd,
        le_host,
        le_port,
        l_URI,
        CLE_SECRETE)

user = utilisateur
password = mot_de_passe
bd_name = nom_bdd
host = le_host
port = le_port
URI = l_URI


name = os.getenv('NAME')
# pour utiliser le to_sql()
engine = create_engine(URI, echo=False)
# PENSER A BIEN NOTER -----> app.config['SQLALCHEMY_DATABASE_URI'] = {bdd}
app = Flask(__name__)
app.config['SECRET_KEY'] = CLE_SECRETE
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

# Login
login = LoginManager(app)
login.login_view = 'login' # permet d'utiliser le login_required

# Email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mon_email
app.config['MAIL_PASSWORD'] = mon_password_email
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


from ou_je_voyage import routes


# db.drop_all()
# db.session.commit()
db.create_all()
db.session.commit()



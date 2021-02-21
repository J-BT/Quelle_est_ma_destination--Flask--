#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:35:52 2020

@author: jbt
"""
from ou_je_voyage import login
from flask_login import UserMixin
from werkzeug.security import (generate_password_hash, check_password_hash)
from enum import unique
from ou_je_voyage import db
from datetime import datetime


class Weather_5days(db.Model):
    id_weather_5days = db.Column(db.Integer, primary_key=True)
    weather_5days_country = db.Column(db.String(120))
    weather_5days_city = db.Column(db.String(120))
    weather_5days_date = db.Column(db.DateTime)
    weather_5days_w_id = db.Column(db.Integer)
    weather_5days_w_main = db.Column(db.String(120))
    weather_5days_w_descrip = db.Column(db.String(120))
    temp_5days_relation = db.relationship(
        'Country', backref='weather_5j_etudie', lazy='joined')
    def __repr__(self):
        return 'f<Weather_5days {self.weather_5days_country,\
            self.weather_5days_date, self.weather_5days_w_main }>'

class Temperature_5days(db.Model):
    id_temp_5days = db.Column(db.Integer, primary_key=True)
    temp_5days_country = db.Column(db.String(120))
    temp_5days_city = db.Column(db.String(120))
    temp_5days_date = db.Column(db.DateTime)
    temp_5days_value = db.Column(db.Float)
    temp_5days_relation = db.relationship(
        'Country', backref='temp_5j_etudiee', lazy='joined')
    def __repr__(self):
        return 'f<Temperature_5days {self.temp_5days_country,\
            self.temp_5days_date, self.temp_5days_value }>'

class Temperature(db.Model):
    id_temperature = db.Column(db.Integer, primary_key=True)
    temp_country = db.Column(db.String(120))
    temp_today = db.Column(db.DateTime)
    temp_value = db.Column(db.Float)
    pop_relation = db.relationship(
        'Country', backref='temp_etudie', lazy='joined')
    def __repr__(self):
        return 'f<Temperature {self.temp_country,\
            self.temp_today, self.temp_value }>'

class Population(db.Model):
    id_population = db.Column(db.Integer, primary_key=True)
    pop_country = db.Column(db.String(120))
    pop_year = db.Column(db.Integer)
    pop_value = db.Column(db.Integer)
    pop_relation = db.relationship(
        'Country', backref='pop_etudie', lazy='joined')
    def __repr__(self):
        return 'f<Population {self.pop_country,\
            self.pop_year, self.pop_value }>'


class Life_expectancy(db.Model):
    id_life_expe = db.Column(db.Integer, primary_key=True)
    l_e_country = db.Column(db.String(120))
    l_e_year = db.Column(db.Integer)
    l_e_value = db.Column(db.Float)
    l_e_relation = db.relationship(
        'Country', backref='espe_etudiee', lazy='joined')
    def __repr__(self):
        return 'f<Life_expectancy {self.l_e_country,\
            self.l_e_year, self.l_e_value }>'

class Unemployment_rate(db.Model):
    id_unemp_rate = db.Column(db.Integer, primary_key=True)
    u_r_country = db.Column(db.String(120))
    u_r_year = db.Column(db.Integer)
    u_r_value = db.Column(db.Float)
    u_r_relation = db.relationship(
        'Country', backref='chom_etudie', lazy='joined')
    def __repr__(self):
        return 'f<Unemployment_rate {self.u_r_country,\
            self.u_r_year, self.u_r_value }>'
    
class Country(db.Model):
    id_country = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(120), index=True)
    country_pop = db.Column(db.Integer, db.ForeignKey(
        'population.id_population'))
    country_life_exp = db.Column(db.Integer, db.ForeignKey(
        'life_expectancy.id_life_expe'))
    country_unem_rate = db.Column(db.Integer, db.ForeignKey(
        'unemployment_rate.id_unemp_rate'))
    country_temp = db.Column(db.Integer, db.ForeignKey(
        'temperature.id_temperature'))
    country_temp_5d = db.Column(db.Integer, db.ForeignKey(
        'temperature_5days.id_temp_5days'))
    country_weather_5d = db.Column(db.Integer, db.ForeignKey(
        'weather_5days.id_weather_5days'))
    
    def __repr__(self):
        return 'f<Country {self.country_name}>' 
   
class Message_user(db.Model):
    id_msg_u = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    contenu = db.Column(db.String(2000))

    def __repr__(self):
        return 'f<Message_User {self.username}, {self.contenu}>' 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(280))
    msg_user = db.Column(db.Integer, db.ForeignKey(
        'message_user.id_msg_u'))
    
    def __repr__(self):
        return 'f<User {self.username}>' 
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:51:02 2020

@author: jbt
"""

from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField,
                     SelectField, SubmitField, FloatField)
from wtforms.validators import (DataRequired, NumberRange)


class Choix_utilisateur(FlaskForm):
    nombre_population = SelectField(
        'Population') 
    esperance_vie = SelectField(
        'Esperance de Vie')
    taux_chomage = SelectField(
        'Taux de Chômage')  
    temperature = SelectField(
        'Temperature')  
    meteo = SelectField(
        'Météo') 
    choix_submit = SubmitField(
        'Soumettre')
    
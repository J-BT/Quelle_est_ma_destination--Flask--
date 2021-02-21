#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 20:35:51 2020

@author: jbt
"""

from flask_wtf import FlaskForm
from wtforms import (StringField,IntegerField,SelectField,SubmitField)
from wtforms.validators import (DataRequired,NumberRange)
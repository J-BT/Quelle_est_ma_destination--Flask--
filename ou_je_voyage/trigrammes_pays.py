#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1) Nous allons importer code des pays (xls) étudiés par l'OCDE via Pandas - OK
2) en faire une liste - OK
3) transformer cette liste en chaine de caractères dont elements séparés
    un signe "+"
"""

import pandas as pd

try:
    pays = pd.read_excel('ou_je_voyage/static/excel/oecd_country_code.xls') 

except:
    pays = pd.read_excel('static/excel/oecd_country_code.xls') 

nom_des_pays = pays['Country']
nom_des_pays = nom_des_pays.values.tolist()
# print(nom_des_pays)

code_pays = pays['CODE']
code_pays = code_pays.values.tolist()

# print(code_pays)

code_pays_oecd = '+'.join(code_pays)
# print(code_pays_oecd)

# # tous_les_pays contient les trigrammes de tous les pays que nous étudierons 
# tous_les_pays = "AUS+AUT+BEL+CAN+CHL+COL+CZE+DNK"
# tous_les_pays += "EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL"
# tous_les_pays += "ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX"
# tous_les_pays += "NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP"
# tous_les_pays += "SWE+CHE+TUR+GBR+USA+WLD+NMEC+BRA"
# tous_les_pays += "CHN+CRI+IND+IDN+PER+RUS+ZAF"


# pays_espe_vie =  "AUS+AUT+BEL+CAN+CHL+COL+CZE+DNK"
# pays_espe_vie += "EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL"
# pays_espe_vie += "ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX"
# pays_espe_vie += "NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP"
# pays_espe_vie += "SWE+CHE+TUR+GBR+USA+NMEC+BRA+CHN"
# pays_espe_vie += "CRI+IND+IDN+RUS+ZAF"


# tous_les_pays_new =  "AUS+AUT+BEL+CAN+CHL+COL+CZE"
# tous_les_pays_new += "DNK+EST+FIN+FRA+DEU+GRC+HUN" 
# tous_les_pays_new += "ISL+IRL+ISR+ITA+JPN+KOR+LVA"
# tous_les_pays_new += "LTU+LUX+MEX+NLD+NZL+NOR+POL"
# tous_les_pays_new += "PRT+SVK+SVN+ESP+SWE+CHE+TUR"
# tous_les_pays_new += "GBR+USA+NMEC+ARG+BRA+BGR+CHN"
# tous_les_pays_new += "CRI+HRV+CYP+IND+IDN+MLT+ROU"
# tous_les_pays_new += "RUS+SAU+SGP+ZAF"

# pays_tx_chom =  "AUS+AUT+BEL+CAN+CHL+COL+CZE+DNK"
# pays_tx_chom += "EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL"
# pays_tx_chom += "ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX"
# pays_tx_chom += "NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP"
# pays_tx_chom += "SWE+CHE+TUR+GBR+USA+CRI+BRA+BGR"
# pays_tx_chom += "CHN+HRV+CYP+MKD+IND+IDN+MLT+ROU"
# pays_tx_chom += "RUS+ZAF"

# tous_les_pays_popu =  "AUS+AUT+BEL+CAN+CHL+COL+CZE"
# tous_les_pays_popu += "DNK+EST+FIN+FRA+DEU+GRC+HUN"
# tous_les_pays_popu += "ISL+IRL+ISR+ITA+JPN+KOR+LVA"
# tous_les_pays_popu += "LTU+LUX+MEX+NLD+NZL+NOR+POL"
# tous_les_pays_popu += "PRT+SVK+SVN+ESP+SWE+CHE+TUR"
# tous_les_pays_popu += "GBR+USA+EU28+G20+OECD+WLD"
# tous_les_pays_popu += "NMEC+ARG+BRA+BGR+CHN+CRI+HRV"
# tous_les_pays_popu += "CYP+IND+IDN+MLT+ROU+RUS+SAU"
# tous_les_pays_popu += "SGP+ZAF"
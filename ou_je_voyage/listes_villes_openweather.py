#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1)Nous allons extraires les noms des differentes villes traitées 
par openweathermap au format json
2) en lister seulement les capitales
3) garder seulement les capitales des pays analysés par l'OCDE'
"""

import json
import pprint
from countryinfo import CountryInfo

### imports modules
try:
    from ou_je_voyage.trigrammes_pays import (nom_des_pays)
except :
    from trigrammes_pays import (nom_des_pays)

def capitales_etudiee_oecd():
    try:
        with open('city.list.json') as f:
          data = json.load(f)
    except:
        with open('ou_je_voyage/city.list.json') as f:
          data = json.load(f)
    
    # villes_monde = pprint.pprint(data)
    
    capitales_oecd = {}
    nom_pays_ocde_majuscules = []
    nom_pays_open_weather_majuscules = []
    pays_communs_pour_projet = []
    
    for pays in nom_des_pays:
        nom_pays_ocde_majuscules.append(pays.upper())
    # for pays_maj in nom_pays_ocde_majuscules:
    #     print(pays_maj)
    
    
    infos_pays = CountryInfo()
    infos_pays = infos_pays.all()
    # print(infos_pays["japan"])
    infos_pays = dict(infos_pays)
    for pays in infos_pays.keys():
        nom_pays_open_weather_majuscules.append(pays.upper())
    
    
    ### Creation set pour trouver elements similaire entre 2 listes villes
    pays_ocde = set(nom_pays_ocde_majuscules)
    pays_open_weather = set(nom_pays_open_weather_majuscules)
    
    pays_communs_pour_projet = pays_ocde.intersection(pays_open_weather)
    
    ### On transforme ce set en list
    pays_communs_pour_projet = list(pays_communs_pour_projet)
    pays_communs_pour_projet.sort(reverse=False)
    
    for pays in pays_communs_pour_projet:
        country = CountryInfo(pays)
        # nom_pays = country.native_name()
        capitale = country.capital()
        capitales_oecd[pays] = capitale    
        
    return capitales_oecd

if __name__=='__main__': 
    capitales_oecd = capitales_etudiee_oecd()
    for capitale in capitales_oecd.items():
        print(capitale) 
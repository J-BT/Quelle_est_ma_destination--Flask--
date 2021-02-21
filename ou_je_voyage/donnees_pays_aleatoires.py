#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Afin de preparer l'application à recevoir les données des divers sources
d'information telles que la bdd de l'UNESCO, notamment via des API permettant
de recupérer les donnéees sous format JSON, nous allons synthétiser des 
données aléatoires sur chaque pays.

Le 1er Objectif etant de créer des dataframes
Le 2ème sera de peupler la bdd 'informations_pays' grâce à ces df.

*******Dataframes Créees*********
I)  Esperance de Vie 


*******Dataframes à Créer*********
1) Chomage
2) Temperature
3) Pays
"""
import numpy as np
import pandas as pd
from datetime import datetime


pays_analyses=['Afghanistan',
 'Albania',
 'Algeria',
 'American Samoa',
 'Andorra',
 'Angola',
 'Anguilla',
 'Antigua and Barbuda',
 'Argentina',
 'Armenia',
 'Aruba',
 'Australia',
 'Austria',
 'Azerbaijan',
 'Bahamas',
 'Bahrain',
 'Bangladesh',
 'Barbados',
 'Belarus',
 'Belgium',
 'Belize',
 'Benin',
 'Bermuda',
 'Bhutan',
 'Bolivia (Plurinational State of)',
 'Bosnia and Herzegovina',
 'Botswana',
 'Brazil',
 'British Virgin Islands',
 'Brunei Darussalam',
 'Bulgaria',
 'Burkina Faso',
 'Burundi',
 'Cambodia',
 'Cameroon',
 'Canada',
 'Cabo Verde',
 'Cayman Islands',
 'Central African Republic',
 'Chad',
 'Channel Islands',
 'Chile',
 'China',
 'China Hong Kong Special Administrative Region',
 'China Macao Special Administrative Region',
 'Colombia',
 'Comoros',
 'Congo',
 'Cook Islands',
 'Costa Rica',
 "Côte d'Ivoire",
 'Croatia',
 'Cuba',
 'Curaçao',
 'Cyprus',
 'Czechia',
 "Democratic People's Republic of Korea",
 'Democratic Republic of the Congo',
 'Denmark',
 'Djibouti',
 'Dominica',
 'Dominican Republic',
 'Ecuador',
 'Egypt',
 'El Salvador',
 'Equatorial Guinea',
 'Eritrea',
 'Estonia',
 'Eswatini',
 'Ethiopia',
 'Faeroe Islands',
 'Falkland Islands (Malvinas)',
 'Fiji',
 'Finland',
 'France',
 'French Guiana',
 'French Polynesia',
 'Gabon',
 'Gambia',
 'Georgia',
 'Germany',
 'Ghana',
 'Gibraltar',
 'Greece',
 'Greenland',
 'Grenada',
 'Guadeloupe',
 'Guam',
 'Guatemala',
 'Guinea',
 'Guinea-Bissau',
 'Guyana',
 'Haiti',
 'Holy See',
 'Honduras',
 'Hungary',
 'Iceland',
 'India',
 'Indonesia',
 'Iran (Islamic Republic of)',
 'Iraq',
 'Ireland',
 'Isle of Man',
 'Israel',
 'Italy',
 'Jamaica',
 'Japan',
 'Jordan',
 'Kazakhstan',
 'Kenya',
 'Kiribati',
 'Kuwait',
 'Kyrgyzstan',
 "Lao People's Democratic Republic",
 'Latvia',
 'Lebanon',
 'Lesotho',
 'Liberia',
 'Libya',
 'Liechtenstein',
 'Lithuania',
 'Luxembourg',
 'Madagascar',
 'Malawi',
 'Malaysia',
 'Maldives',
 'Mali',
 'Malta',
 'Marshall Islands',
 'Martinique',
 'Mauritania',
 'Mauritius',
 'Mayotte',
 'Mexico',
 'Micronesia (Federated States of)',
 'Monaco',
 'Mongolia',
 'Montenegro',
 'Montserrat',
 'Morocco',
 'Mozambique',
 'Myanmar',
 'Namibia',
 'Nauru',
 'Nepal',
 'Netherlands',
 'New Caledonia',
 'New Zealand',
 'Nicaragua',
 'Niger',
 'Nigeria',
 'Niue',
 'North Macedonia',
 'Northern Mariana Islands',
 'Norway',
 'Oman',
 'Pakistan',
 'Palau',
 'Palestine',
 'Panama',
 'Papua New Guinea',
 'Paraguay',
 'Peru',
 'Philippines',
 'Poland',
 'Portugal',
 'Puerto Rico',
 'Qatar',
 'Republic of Korea',
 'Republic of Moldova',
 'Réunion',
 'Romania',
 'Russian Federation',
 'Rwanda',
 'Saint Helena',
 'Saint Kitts and Nevis',
 'Saint Lucia',
 'Saint Pierre and Miquelon',
 'Saint Vincent and the Grenadines',
 'Saint-Barthélemy',
 'Saint-Martin (French part)',
 'Samoa',
 'San Marino',
 'Sao Tome and Principe',
 'Saudi Arabia',
 'Senegal',
 'Serbia',
 'Seychelles',
 'Sierra Leone',
 'Singapore',
 'Sint Maarten (Dutch part)',
 'Slovakia',
 'Slovenia',
 'Solomon Islands',
 'Somalia',
 'South Africa',
 'South Sudan',
 'Spain',
 'Sri Lanka',
 'Sudan',
 'Suriname',
 'Sweden',
 'Switzerland',
 'Syrian Arab Republic',
 'Tajikistan',
 'Thailand',
 'Timor-Leste',
 'Togo',
 'Tokelau',
 'Tonga',
 'Trinidad and Tobago',
 'Tunisia',
 'Turkey',
 'Turkmenistan',
 'Turks and Caicos Islands',
 'Tuvalu',
 'Uganda',
 'Ukraine',
 'United Arab Emirates',
 'United Kingdom of Great Britain and Northern Ireland',
 'United Republic of Tanzania',
 'United States of America',
 'United States Virgin Islands',
 'Uruguay',
 'Uzbekistan',
 'Vanuatu',
 'Venezuela (Bolivarian Republic of)',
 'Viet Nam',
 'Wallis and Futuna Islands',
 'Western Sahara',
 'Yemen',
 'Zambia',
 'Zimbabwe']

### valeurs min/max random
valeurs_random_espe = {"mini": 50 , "maxi": 85}
# Pandas n'aime pas les valeures < 1!!
valeurs_random_chomage = {"mini": 9 , "maxi": 30}
valeurs_random_temperature = {"mini": 13 , "maxi": 27}

def generation_donnees_random (
        valeur_min_random, valeur_max_random, source_info):

    les_pays = pays_analyses
    les_sources_d_info = [source_info]
    np.random.seed(0) #<---quand == 0, ne reset pas donnéees aléatoires
    id_pays_provisoire = 0
    ligne_pour_bdd = []
    donnees_sur_pays = {}
    
    for pays in les_pays:
        for source in les_sources_d_info:
            ligne_pour_bdd = []
            annee_2016 = float(np.random.randint(
                valeur_min_random, valeur_max_random, 1))
            annee_2017 = float(np.random.randint(
                annee_2016-2, annee_2016+2, 1)) 
            annee_2018 = float(np.random.randint(
                annee_2017-2, annee_2017+2, 1))
            annee_2019 = float(np.random.randint(
                annee_2018-2, annee_2018+2, 1))
            ligne_pour_bdd.append(pays)
            ligne_pour_bdd.append(annee_2016)
            ligne_pour_bdd.append(annee_2017)
            ligne_pour_bdd.append(annee_2018)
            ligne_pour_bdd.append(annee_2019)
            ligne_pour_bdd.append(source)
            ligne_pour_bdd.append(datetime.utcnow())
            
            donnees_sur_pays[id_pays_provisoire] = ligne_pour_bdd
            id_pays_provisoire += 1
                
    return pd.DataFrame.from_dict(
        donnees_sur_pays, orient='index')

if __name__=='__main__':
    ### Tests
    GENERER_ESPERANCE_DE_VIE = True
    GENERER_TAUX_CHOMAGE = True
    GENERER_TEMPERATURES = True
### Générer Espe vie   
    if GENERER_ESPERANCE_DE_VIE:
        espe_a_inserer_dans_bdd = generation_donnees_random(
            valeurs_random_espe["mini"],
            valeurs_random_espe["maxi"], 
            'UNESCO')
        # ---Ajouter colonne à df-----
        espe_a_inserer_dans_bdd.columns = [
            "espe_pays_concerne",
            "espe_2016",
            "espe_2017",
            "espe_2018",
            "espe_2019",
            "espe_source_info",
            "espe_timestamp"]
        print(espe_a_inserer_dans_bdd)
### Générer Chomage        
    if GENERER_TAUX_CHOMAGE:
        chomage_a_inserer_dans_bdd = generation_donnees_random(
            valeurs_random_chomage["mini"],
            valeurs_random_chomage["maxi"], 
            'UNESCO')
        # ---Ajouter colonne à df-----
        chomage_a_inserer_dans_bdd.columns = [
            "chomage_pays_concerne",
            "chomage_2016",
            "chomage_2017",
            "chomage_2018",
            "chomage_2019",
            "chomage_source_info",
            "chomage_timestamp"]
        print(chomage_a_inserer_dans_bdd)
### Générer Temperatures    
    if GENERER_TEMPERATURES:
        temperatures_a_inserer_dans_bdd = generation_donnees_random(
            valeurs_random_temperature["mini"],
            valeurs_random_temperature["maxi"],
            'ACCUWEATHER')
        # ---Ajouter colonne à df-----
        temperatures_a_inserer_dans_bdd.columns = [
            "temperature_pays_concerne",
            "temperature_2016",
            "temperature_2017",
            "temperature_2018",
            "temperature_2019",
            "temperature_source_info",
            "temperature_timestamp"]
        print(temperatures_a_inserer_dans_bdd)


    

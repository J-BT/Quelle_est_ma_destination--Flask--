#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nous allons créeer plusieurs fonctions pour extraires les donnéees
du site stats.oecd.org via l'API Rest mise à disposition.
Ainsi on pourra peupler les tables :
    - Esperance_vie
    - Population
    - Chomage
de la bdd informations_pays

==============================================================================
Un point d'accès à l'API de l'OCDE se presente comme il suit:

    "https://stat.oecd.org/SDMX-JSON/data/DataSetCode/Subject.{tous_les_pays}/
    ?contenttype=csv"
    
Par exemple pour le cas d l'espe_vie :
    DataSetCode --> HEALTH_STAT
    Subject ------> EVIETOTA.EVIDUREV+EVIFHOEV+EVIHFEEV
    
"""

### Imports bibliotheques    
import pandas as pd
import numpy as np
import time, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

### imports modules
try:
    from .__init__ import (engine, app, db)
    from .trigrammes_pays import (code_pays_oecd, nom_des_pays)
except :
    from ou_je_voyage.trigrammes_pays import (code_pays_oecd, nom_des_pays)
    from ou_je_voyage.__init__  import engine

# Pour communiquer avec bdd
Session = sessionmaker(bind=engine)
session = Session()

def get_population():
    def get_from_oecd(sdmx_query):
        """
        Permet d'importer les données de l'API de l'OCDE sous format csv
        """
        return pd.read_csv(
        f"https://stats.oecd.org/SDMX-JSON/data/{sdmx_query}all?"
        +"&dimensionAtObservation=allDimensions&contentType=csv"
        )
    
    demograph = f"HISTPOP/{code_pays_oecd}.T.TOTAL/all"
    get_from_oecd(demograph)    
    total_habitants = get_from_oecd(demograph)    
    masque = (total_habitants["Time"] >= 2000)    
    population = total_habitants[masque]
    population = population.sort_values(by=['Country','Time'], ascending=True)
    population = population[['Country','Time','Value']]
    population['Country'] = population['Country'].apply(lambda x: x.upper())
    population['Value'] = population['Value'].apply(
        lambda x: int(x))
    
    #Reindexons la df
    new_index = [] 
    for index in range(1, len(population.index)+1):
        new_index.append(index)
    population.index = new_index
    
    return population


def get_unemployment_rate():
    def get_from_oecd(sdmx_query):
        """
        Permet d'importer les données de l'API de l'OCDE sous format csv
        """
        return pd.read_csv(
        f"https://stats.oecd.org/SDMX-JSON/data/{sdmx_query}all?"
        +"&dimensionAtObservation=allDimensions&contentType=csv"
        )
    
    ### Taux chomage  ####################################################  
    tx_chom = f"LFS_SEXAGE_I_R/{code_pays_oecd}.MW.900000.UR.A/"
    get_from_oecd(tx_chom)    
    chomage = get_from_oecd(tx_chom)    
    #masque = (chomage["Time"] >= 2000 ) & (chomage["Country"] == "France")
    masque = (chomage["Time"] >= 2000 )
    taux_chomage = chomage[masque]
    taux_chomage = taux_chomage.sort_values(by=['Country','Time'],
                                                              ascending=True)
    taux_chomage = taux_chomage[['Country','Time','Value']]
    taux_chomage['Country'] = taux_chomage['Country'].apply(
        lambda x: x.upper())
    taux_chomage['Value'] = taux_chomage['Value'].apply(
        lambda x: round(x, 2))
    
    
    #Reindexons la df
    new_index = [] 
    for index in range(1, len(taux_chomage.index)+1):
        new_index.append(index)
    taux_chomage.index = new_index
    
    return taux_chomage



def get_life_expectancy():
    def get_from_oecd(sdmx_query):
        """
        Permet d'importer les données de l'API de l'OCDE sous format csv
        """
        return pd.read_csv(
            f"https://stats.oecd.org/SDMX-JSON/data/{sdmx_query}"
            +"?contentType=csv"
        )
    
    ### Esperance de vie ####################################################
    espe_vie = "HEALTH_STAT/EVIETOTA.EVIDUREV+EVIFHOEV+EVIHFEEV."
    espe_vie+= f"{code_pays_oecd}/"
    
    get_from_oecd(espe_vie)
    espe = get_from_oecd(espe_vie)
    # On importe que les données supérieures à 2000
    masque = (espe.Year >= 2000)
    espe_2000_2018 = espe[masque]
    #Classement pour table Esp^
    espe_2000_2018 = espe_2000_2018.sort_values(by=['Country','Year'],
                                                ascending=True)
    espe_2000_2018 = espe_2000_2018[['Country','Year','Value']]
    espe_2000_2018['Country'] = espe_2000_2018['Country'].apply(
        lambda x: x.upper())
    espe_2000_2018['Value'] = espe_2000_2018['Value'].apply(
        lambda x: round(x, 2))
    
    #Reindexons la df
    new_index = [] 
    for index in range(1, len(espe_2000_2018.index)+1):
        new_index.append(index)
    espe_2000_2018.index = new_index
    
    return espe_2000_2018

def get_countries_populated():
    """
    A pour but de peupler la df Country avec les index des differentes
    tables (Life_exceptancy, Pupulation...) qui permettront de d'indiquer les
    foreign key de la table Country
    
    """
    pays_analyses = pd.DataFrame(nom_des_pays, columns =['country_name'])
    pays_analyses['country_name'] = pays_analyses['country_name'].apply(
        lambda x: x.upper())
    pays_analyses = pays_analyses.sort_values(by=['country_name'],
                                              ascending=True)
    #On ajoute les nouvelles colonnes
    pays_analyses['country_pop'] = None
    pays_analyses['country_life_exp'] = None
    pays_analyses['country_unem_rate'] = None
    pays_analyses['country_temp'] = None
    pays_analyses['country_temp_5d'] = None
    pays_analyses['country_weather_5d'] = None
    
    espe_2000_2018 = pd.read_sql_table("life_expectancy", engine)
    population = pd.read_sql_table("population", engine)
    taux_chomage = pd.read_sql_table("unemployment_rate", engine)
    temp_actuelle = pd.read_sql_table("temperature", engine)
    temp_5j_av = pd.read_sql_table("temperature_5days", engine)
    meteo_5j_av = pd.read_sql_table("weather_5days", engine)
           
    mask_2017 = espe_2000_2018["l_e_year"] == 2017
    espe_2017 = espe_2000_2018[mask_2017]
    
    mask_2017 = population["pop_year"] == 2017
    pop_2017 = population[mask_2017]
    
    mask_2017 = taux_chomage["u_r_year"] == 2017
    chom_2017 = taux_chomage[mask_2017]
    
    ###---------------------------------------------------------------
    # Colonnes country_temp_5d & country_weather_5d
    #-----------------------------------------------------------------
    ts_moins_5j =  temp_5j_av['temp_5days_date'][12]

    mask_midi = temp_5j_av['temp_5days_date'] == ts_moins_5j
    temp_5days_av_midi = temp_5j_av[mask_midi]
    
    mask_midi = meteo_5j_av['weather_5days_date'] == ts_moins_5j
    meteo_5days_av_midi = meteo_5j_av[mask_midi]
    
    
    # (pour l'instant) TROP COMPLIQUE POUR MOI
    # #La condition selctionne les pays traité par l'ocde
    condition = pays_analyses['country_name'].isin(
        espe_2000_2018['l_e_country'])
    
 
    ### Peuplement df Country -> population
    for index_pays, ligne_pays in pays_analyses.iterrows():
        # print(f'Index: {index}, ligne_pays: {ligne_pays.values[0]}')
        # ligne_pays.values[1]= 33
        for index_pop, ligne_pop in pop_2017.iterrows():
            # print(f'Index: {index}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_pop[1]:
                ligne_pays[1] = ligne_pop[0]
    ### Peuplement df Country -> life expectancy
        for index_espe_vie, ligne_espe in espe_2017.iterrows():
            # print(f'Index: {index_espe_vie}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_espe[1]:
                ligne_pays[2] = ligne_espe[0]
                
    ### Peuplement df Country -> unemployment_rate
        for index_chom, ligne_chom in chom_2017.iterrows():
            # print(f'Index: {index}, ligne_pays: {ligne_espe.values}')
            if ligne_pays[0] == ligne_chom[1]:
                ligne_pays[3] = ligne_chom[0]
    
    ### TEMPERATURE ACTUELLE
        for index_temp, ligne_temp in temp_actuelle.iterrows():
            if ligne_pays[0] == ligne_temp[1]:
                ligne_pays[4] = ligne_temp[0]
     
    ### TEMPERATURE IL Y A 5J A MIDI 
        for index_temp5j, ligne_temp5j in temp_5days_av_midi.iterrows():
            if ligne_pays[0] == ligne_temp5j[1]:
                ligne_pays[5] = ligne_temp5j[0]
    
    ### METEO IL Y A 5J A MIDI
        for index_meteo5j, ligne_meteo5j in meteo_5days_av_midi.iterrows():
            if ligne_pays[0] == ligne_meteo5j[1]:
                ligne_pays[6] = ligne_meteo5j[0]

    return pays_analyses


### Tests
POP = False
UNEMPLO_RATE = False
LIFE_EXP = False
COUNTRIES = True

if __name__== '__main__':

    if POP:
        population = get_population()
        colonnes_u_r = ['Country',
                        'Year',
                        'Value']
        population.columns = colonnes_u_r
        print(population)
    
    if UNEMPLO_RATE:
        taux_chomage = get_unemployment_rate()
        colonnes_u_r = ['Country',
                        'Year',
                        'Value']
        taux_chomage.columns = colonnes_u_r
        print(taux_chomage)
    if LIFE_EXP:
        espe_2000_2018 = get_life_expectancy()
        colonnes_l_e = ["l_e_country",
                        "l_e_year",
                        "l_e_value"]
        espe_2000_2018.columns = colonnes_l_e
        print(espe_2000_2018)
    
    if COUNTRIES:
        pays_analyses = get_countries_populated()
        nombre_pays = len(pays_analyses.index)
        
        print(pays_analyses)
        # print(pays_analyses[condition])
   
        
    
        
     
        
    
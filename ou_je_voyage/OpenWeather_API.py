#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 22:45:54 2020

@author: jbt
"""
import json
import requests
import pprint
import pandas as pd
from countryinfo import CountryInfo


### imports modules
try:
    import sys
    sys.path.append('..') #Permet d'acceder aux dossiers parents
    from config.config import (
        cle_num_1,
        cle_num_2)
except:
    from config.config import (
        cle_num_1,
        cle_num_2)



try:
    from .listes_villes_openweather import capitales_etudiee_oecd
except:   
    from ou_je_voyage.listes_villes_openweather import capitales_etudiee_oecd


def get_timestamp_for_5_days():
    """
    Crée un dictionnaire de la forme {jour : timestamp} donc les valeurs
    correspondent aux timestamp des 5 derniers jours à la même heure.
    
    ***********************************************************
    *****Le format timestamp correspond aux millisecondes *****
    ***********************************************************
    ___________________________________________________________________
    >>>>>> 432000 = 5*24h | 86400 =  24h | 3600 = 1h <<<<<<<<<<<<<<<<<<
    ------------------------------------------------------------------
    {
    jour-5 : x + 86400*0
    jour-4 : x + 86400*1
    jour-3 : x + 86400*2
    jour-2 : x + 86400*3
    jour-1 : x + 86400*4
    }
    où x = timestamp actuel - 432000
    
    --- exemple ---
    si datetime actuel = Timestamp('2020-11-12 13:52:19.670039')
    on a timestamp actuel = 1605189139
    x = 1605189139 - 5 jours = 1605189139 - 432000 = 1604757139
        L> 1604757139 correspond à 11/07/2020 @ 1:52pm (UTC)
    
    jour-5 : x + 86400*0 = 1604757139  # 07/11/2020 @ 13:52 (UTC)
    jour-4 : x + 86400*1 = 1604843539  # 08/11/2020 @ 13:52 (UTC)
    jour-3 : x + 86400*2 = 1604929939  # 09/11/2020 @ 13:52 (UTC)
    jour-2 : x + 86400*3 = 1605016339  # 10/11_2020 @ 13:52 (UTC)
    jour-1 : x + 86400*4 = 1605102739  # 11/11/2020 @ 13:52 (UTC)

    
    """
    
    datestamps_5_jours = {}
    
    datetime_now_for_humans = pd.Timestamp.now()
    # L> par ex: Timestamp('2020-11-12 13:27:58.668275')
    
    # On converti en format timestamp
    datetime_now_for_machines = pd.Timestamp.timestamp(
        datetime_now_for_humans)
    datetime_now_for_machines = int(datetime_now_for_machines)
    # L> par ex : 1605187678.668275
    m_5days = datetime_now_for_machines - 432000
    
    for i in range(5, 0, -1):
        datestamps_5_jours[f"day_m{i}"] = m_5days + 86400*(5-i)
        
        
    return datestamps_5_jours

def get_latitute_and_longitude():
    """
    Importe les capitales étudiée et donne leur latitute et longitude
    
    ---format----
    { PAYS : ["Capitale", [latitude, longitude]] }
    
    """
    lat_long_capitales ={}
    ville_capitales = capitales_etudiee_oecd()
    for pays, capitale in ville_capitales.items():
        lat_long = CountryInfo(pays)
        try:
            lat_long = lat_long.capital_latlng()
        except:
            lat_long = "erreur"
        lat_long_capitales[pays] = [capitale, lat_long]
        
    return lat_long_capitales


def get_temperature():
    """
    Recupération des températures actuelles au sein des capitales des pays
    analysés par l'ocde'
    """
    capitales_monde = []
    def temperatures_du_monde(villes):
        """
        Permet d'intererroger l'API d'OpenWeather et d'extraire
        les temperatures actuelles des pays selectionnés
        --> Retourne une liste de dictionnaire de la forme :
            {pays} : {temperature}
        """
        def temperature_actuelle_pays(ville):
            API_key_1 = cle_num_1
            url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}"
            url+= f"&appid={API_key_1}"
            reponse = requests.get(url)
            
            resultat = reponse.json()
            infos_pays = {}
            try:
                # nom du pays
                pays = resultat['sys']['country']
            except:
                pays = "erreur"
            # print(pays)
            try:
                # ville 
                la_ville = ville
            except:
                ville = 'erreur'
            try:
                # temperature actuelle en Kelvin
                temperature_kelvin = resultat['main']['temp']
            except:
                temperature_kelvin = 'erreur'
            
            try:
                # temperature actuelle en °C
                temperature_c = round((temperature_kelvin - 273.15), 2)
            except:
                temperature_c = 'erreur'
            infos_pays[pays]= [ville, temperature_kelvin, temperature_c]
            return infos_pays
        
        temperatures_villes = {}
        for ville in villes:
            for cle, valeur in temperature_actuelle_pays(ville).items():
                temperatures_villes[cle] = valeur
                # print(temperatures_villes[rang_ville])
        return temperatures_villes
    
    capitales = capitales_etudiee_oecd()
    capitales_oecd = list(capitales.values())
    
    temperature_pays = temperatures_du_monde(capitales_oecd)
    
    # print(temperature_pays)
    # print(type(temperature_pays))
    
    ### Creation dictionnaire pour df puis table climat
    temperatures_pays_bdd = {}
    
    for code, capitale_kelvin_celcius in temperature_pays.items():
        # print(capitale_kelvin_celcius)
        for pays, capitale in capitales.items():
            if capitale_kelvin_celcius[0] == capitale:
                date_temp = []
                date_temp.append(pd.Timestamp.today())
                date_temp.append(capitale_kelvin_celcius[2])
                temperatures_pays_bdd[pays] = date_temp
    
    temperature_pays = temperatures_pays_bdd
    temp_part1 = pd.DataFrame(temperature_pays.keys())
    todays = []
    temperatures = []
    for today, temperature in temperature_pays.values():
        todays.append(today)
        temperatures.append(temperature)  
    temp_part1[1] = pd.DataFrame(todays)
    temp_part1[2] = pd.DataFrame(temperatures)
    temp_columns = ['temp_country','temp_today','temp_value']
    temp_part1.columns = temp_columns
    countries_temperature = temp_part1
    
### suppression des erreurs df temperatures
    masque = (countries_temperature['temp_country'] != 'erreur') &\
        (countries_temperature['temp_today'] != 'erreur') &\
        (countries_temperature['temp_value'] != 'erreur')
    countries_temperature = countries_temperature[masque]
    print("Appel fonction réussi!")
    return countries_temperature

def get_historical_5_previous_days():
    """
    Afin de créer les 2 DF :
        - Five_days_previous_temperatures  (historique temperatures)
        - Five_days_previous_weather (historique méteo)
    Et recupérer les informations relatives à la temperature et au temps
    heure par heure au au cours des 5 jours précedents l'appel de la 
    fonction, nous allons :
        
    1) Importer les latitutes et longitudes des capitales des pays
    étudiés
    
    2) Invoquer pandas.Timestamp.now pour connaitre la date (av heure & min)
        actuelle au format Timestamp
        
    3) Nous allons soustraire 5 jours au format Timestamp
        le resultat sera nommé timestamp_5_days_b
    4) Nous allons soustraire 4 jours au format Timestamp
        le resultat sera nommé timestamp_4_days_b
    5) Nous allons soustraire 3 jours au format Timestamp
        le resultat sera nommé timestamp_3_days_b
    6) Nous allons soustraire 2 jours au format Timestamp
        le resultat sera nommé timestamp_2_days_b
    7) Nous allons soustraire 1 jour au format Timestamp
        le resultat sera nommé timestamp_1_days_b        
    
    8) Grâce à un systeme de boucle nous allons recupérer les informations 
    souhaitée  grâce à l'entry point :
             _________________________________________________
    _______|| UTILISATION DE L'API pour historique 5 jours ||___________
    
        'http://api.openweathermap.org/data/2.5/onecall/timemachine?'+
        'lat={lat}&lon={long}&dt={timestamp}&appid={API key}'
    ==================================================================== 
    Infos recupérées :
        
        - date jour j / h (TimeStamp) --> [hourly][dt]
        - temperature au jour j / h  ---> [hourly][temp]
        
        - temps au jour(id) j / h ----------> [hourly][weather][id]
            (temps clair : 800)
            (11-25% nuages : 801)
            (25-50% nuages : 802)
        
        - temps au jour j (id) / h ----------> [hourly][weather][id]
        - temps au jour j  / h ----------> [hourly][weather][main]
            ("rain", "snow", "clear")
        - temps au jour j (description) / h 
                -----> [hourly][weather][description]
    =======================================================================
    """
    # recup latitude et longitudes des capitales des pays analysés
    lat_long_capitales = get_latitute_and_longitude()
    # recuperation des timestamps des 5 jours
    datestamp_5j = get_timestamp_for_5_days()
    
    # dico_test = {}
    #crée pour pouvoir indexer dataframe puis tabl
    # index = 1
    ligne = 1
    longitude, latitude, timestamp = 0, 0, 0
    infos_meteo_24h = {}
    infos_temperature_24h = {}
    
    temps_debut_fx = pd.Timestamp.now()
    
    for pays, cap_lat_lon in lat_long_capitales.items():
        for jour, t_stamp in datestamp_5j.items():
            # print(cap_lat_lon)
            latitude = cap_lat_lon[1][0]
            longitude = cap_lat_lon[1][1]
            timestamp = t_stamp
            # dico_test[index] = [pays, latitude, longitude, timestamp]        
            # index += 1
            # print(index, latitude, longitude, pd.to_datetime(timestamp, unit='s'))
            
            API_key_2 = cle_num_2
            url  = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
            url += f"?lat={latitude}&lon={longitude}&dt={timestamp}&units=metric"
            url += f"&appid={API_key_2}"
            try:
                reponse = requests.get(url)
                resultat = reponse.json()
                pays = pays
                ville = cap_lat_lon[0]
                
                for i in range(len(resultat["hourly"])):
                    #on change format datetime ms--->datetime
                    datetime_ts = resultat["hourly"][i]["dt"]
                    #on change format datetime ms--->datetime
                    datetime = pd.to_datetime(datetime_ts, unit='s')
                    temperature = resultat["hourly"][i]["temp"]
                    weather_id = resultat["hourly"][i]["weather"][0]["id"]
                    weather_main = resultat["hourly"][i]["weather"][0]["main"]
                    weather_description = resultat["hourly"][i]["weather"][0]["description"]
                
                    infos_temperature_24h[ligne] = [pays, ville,
                                                    datetime, temperature]
                    infos_meteo_24h[ligne] = [pays, ville, datetime,
                                              weather_id, weather_main,
                                              weather_description]
                    
                    ligne += 1
            except:
                datetime = pd.to_datetime(timestamp, unit='s')
                infos_temperature_24h[ligne] = [pays, ville, datetime, 'NaN']
                infos_meteo_24h[ligne] = [pays, ville, datetime,'NaN',
                                          'NaN', 'NaN']
                ligne += 1
    
    # Creation DF avec historiques temperatures
    historical_temperatures_5days = pd.DataFrame(
        infos_temperature_24h.values())
    colonnes = ["temp_5days_country","temp_5days_city",
                "temp_5days_date", "temp_5days_value" ]
    historical_temperatures_5days.columns = colonnes
    historical_temperatures_5days.sort_values(by=['temp_5days_country',
                                                  'temp_5days_date'],
                                              ascending=True)
    
    # Creation DF avec historiques temps
    historical_weather_5days = pd.DataFrame(infos_meteo_24h.values())
    colonnes = ["weather_5days_country","weather_5days_city",
                "weather_5days_date", "weather_5days_w_id",
                "weather_5days_w_main", "weather_5days_w_descrip" ]
    historical_weather_5days.columns = colonnes
    historical_weather_5days.sort_values(by=['weather_5days_country',
                                             'weather_5days_date'],
                                         ascending=True)
    
    #On retire les 'NaN' pour df temp
    sans_NaN = (historical_temperatures_5days['temp_5days_date'] != 'NaN') &\
            (historical_temperatures_5days['temp_5days_value'] != 'NaN') 
    historical_temperatures_5days = historical_temperatures_5days[sans_NaN]
    
    #On retire les 'NaN' pour df weather
    sans_NaN = (historical_weather_5days['weather_5days_date'] != 'NaN') &\
            (historical_weather_5days['weather_5days_w_id'] != 'NaN') &\
            (historical_weather_5days['weather_5days_w_main'] != 'NaN')&\
            (historical_weather_5days['weather_5days_w_descrip'] != 'NaN')
    historical_weather_5days = historical_weather_5days[sans_NaN]
    
    temps_fin_fx = pd.Timestamp.now()
           
    
    temps_execution_fonction =  temps_fin_fx - temps_debut_fx
    print("temps execution f(x) = ", temps_execution_fonction)
    
    return historical_temperatures_5days, historical_weather_5days

### TESTS
HISTO_PREV_5_DAYS = False
TIMESTAMP_5_DAYS = False
LATITUDE_LONGITUDE = False
ACTUAL_TEMPERATURE = False

if __name__ == '__main__': 
   
    if HISTO_PREV_5_DAYS:
        pass
    
    if TIMESTAMP_5_DAYS:
        datestamp_5j = get_timestamp_for_5_days()
        for jour, datestamp in datestamp_5j.items():
            print(jour, datestamp)
            
    if LATITUDE_LONGITUDE:
        lati_longi = get_latitute_and_longitude()
        for pays, cap_lat_long in lati_longi.items():
            print(pays, cap_lat_long)
            
    if ACTUAL_TEMPERATURE:
        # villes = capitales_etudiee_oecd()
        # print(f"{villes}")
        countries_temperature = get_temperature()
        print(countries_temperature)

    
    
    
    
    


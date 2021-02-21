#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 00:00:24 2020

@author: jbt
"""
### Imports bibliotheques 
import pandas as pd
import numpy as np
import time, datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
plt.style.use('classic')
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

### imports modules
try:
    import sys
    sys.path.append('..') #Permet d'acceder aux dossiers parents
    from __init__ import (engine, app, db)
    from trigrammes_pays import (code_pays_oecd, nom_des_pays)
except :
    from ou_je_voyage.trigrammes_pays import (code_pays_oecd, nom_des_pays)
    from ou_je_voyage.__init__  import engine

# Pour communiquer avec bdd
Session = sessionmaker(bind=engine)
session = Session()


def lineplot_analyse(donnees, abscisse, ordonnee, fichier):
    lineplot = sns.lmplot(x=abscisse, y=ordonnee, data=donnees)
    plt.title("Analyse selon le critère : "+ordonnee, size=15)
    leg_std = mpatches.Patch(color='#c2d1f0',
                              label='Population x 10 Millions')
    leg_mean = mpatches.Patch(color='#3266cd', label='Annee + 2000')
 
    plt.legend(handles=[leg_std, leg_mean],
                loc='lower left',
                bbox_to_anchor=(0., -0.33))
    plt.savefig("ou_je_voyage/static/"+fichier)
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()




def graph_corr(donnees, fichier):
    """
    Possibilité de filtrer la df avant de faire le .corr() pour choisir 
    quelles colonnes inspecter
    """
    
    graphique = sns.clustermap(donnees.corr(method ='pearson'))
    graphique.fig.suptitle(
        'Correlation Temperature/Esp.Vie/Population/Chomage', color="Indigo",
        size=20)
    plt.tight_layout()
    plt.savefig("ou_je_voyage/static/" +fichier)
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()

###TESTS
LINE_CHART = True
CORRELATION_CHART = False

if __name__=="__main__":
    if LINE_CHART:
        population = pd.read_sql_table("population", engine)
        mask = population['pop_country'] == 'FRANCE'
        population_etudiee = population[mask]
        abscisse = "pop_year"
        ordonnee = "pop_value"
        fichier = "graphiques/population.png"
        lineplot_analyse(population_etudiee, abscisse, ordonnee, fichier)
   
    elif CORRELATION_CHART:
        tous_les_pays = pd.read_sql_table("country", engine)
        correlation = tous_les_pays[[
            "country_pop", "country_life_exp",
            "country_unem_rate","country_temp"]]
 
        fichier = "graphiques/corelation.png"
        graph_corr(correlation, fichier)
        



# Projet présenté pour les certifications RS3497 “Développer une base de données”
# RS3508 “Exploiter une base de données” : Ou Je Vais 



## | Description

Le principe est simple, en se basant sur les bases de données de l'OCDE
 (L'Organisation de coopération et de développement économiques) et celle
du service en ligne de prévisions météorologiques, OpenWeatherMap, cette
application vous dresse un classement, en fonction des critères que vous
choisissez, des pays où vous devriez aller pour être satisfait.e.s...

Ce projet etant un prototype, il vous propose de choisir vos préferences
selon 5 critères :

- Le nombre d'habitants : Elevé ou Faible
- L'esperance de vie : Elevée ou Faible
- Le taux de chômage : Elevé ou Faible
- La temperature : Elevée ou Faible
- La météo : Temps clair ou Pluie

Pour l'instant vous ne pourrez pas selectionner plus d'un critère à la fois. 
Il faudra laisser les autres selecteurs sur "Ignorer" lorsque vous
selectionnerez un critère.

Pour cela, cliquez sur l'onglet "J'y vais!", choisissez vos préferences et
cliquez sur soumettre.

L'application vous affichera alors les 10 premiers pays, classés selon
votre choix.

Vous aurez alors : 

- accès aux données de ces premiers pays

[ ET ]

- un graphique montrant l'evolution de la population du 1er pays
 entre 2000 et 2018

- un graphique présentation l'evolution du taux de chômage du premier
pays entre 2000 et 2018

- un graphique présentant le taux de chômage du 1er pays entre 2000 et 2018

- un graphique de corrélation croisant les temperarures, esperances de vie, 
population et taux de chômage du premier pays.
Plus la couleur sera claire et plus il existerait une corrélation entre les
2 facteurs.
(Dans la prochaine version du projet nous affineront les resultats trouvés
pour essayer d'en determiner la raison, quand 2 critères sont réellement
 corrélées).



## | Installation

1. Installer python en allant sur https://www.python.org/downloads/

2. Installer virtual env : `pip install virtualenv`

3. Exécuter dans un terminal à la racine du dossier de l'application:
`virtualenv -p python3 (nom_de_l_environnement_virtuel)`
Cela créera un environnement virtuel s'appellant `nom_de_l_environnement_virtuel`

4. Lancer l'environnement virtuel :
`source (nom_de_l_environnement_virtuel)/bin/activate`

	* nb: pour quitter l'environnement : executer `deactivate`

5. Exécuter `pip install -r requierements.txt` pour installer les bibliothèque nécessaires

6. Mettre à jour `pip` si l'on vous le propose

7. Lancer l'application avec `python3 run.py` depuis la racine du dossier  

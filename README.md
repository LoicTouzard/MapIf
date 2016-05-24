# MapIf
![Mapif-logo](src/static/favicon.png "Mapif-logo")   
Où sont les IIIIIF ?  ICI --> [mapif en ligne](http://mapif-insa.rhcloud.com)  

## Le projet

Ce projet est né de l'esprit de quelques 4IF au moment critique qu'est le stage, veille du départ en échange pour une majorité d'entre eux. Cette épreuve qu'est la séparation n'étant pas facile à vivre, ils ont décidé de développer cette petite application permettant de connaître la position d'autres IF des endroits où se trouvent leurs amis et où ils se trouvent eux mêmes.  

## Contribuer

Si vous avez une idée de fonctionnalité, n'hésitez pas a l'implémenter ou à la partager dans les [issues](https://github.com/LoicTouzard/MapIf/issues).  

## Environnement de développement

### Back

Le code du serveur est développé en [Python 3](https://www.python.org/downloads/) compatible avec la version `3.3` pour permettre son déploiement sur [OpenShift](https://www.openshift.com).  
Le back utilise [Flask](http://flask.pocoo.org/), et d'autres librairies python renseignées dans le fichier [requirements.txt](requirements.txt).  
Installez les dépendance en executant `pip install -r requirements.txt`.  
Vous aurez besoin également de créer le fichier de configuration `mapif.ini` pour ce, prenez exemple sur le fichier [mapif.ini.dist](mapif.ini.dist).
Vous devez également créer au choix le fichier `database/mapif.sqlite` à la racine du projet ou mettre en place une base [PostgreSQL](https://www.postgresql.org).
Pour lancer l'application, un simple `python main.py` devrait suffire.
Vous devriez pouvoir y accéder en cliquant [ici](http://localhost:5000).

### Front

Le front est développé en [HTML5](http://www.w3schools.com/html/html5_intro.asp), [CSS3](http://www.w3schools.com/css/css3_intro.asp), [javascript ECMA5](https://developer.mozilla.org/fr/docs/Web/JavaScript/Language_Resources).  
Le code exploite principalement [jQuery 2.2.3](http://jquery.com/) pour la gestion des évènements et animations, [Leaflet.js](http://leafletjs.com/) pour la gestion de la carte, et [Nominatim d'OpenStreetMap](http://nominatim.openstreetmap.org/) pour la résolution d'adresse.  
Pour le style il s'agit de [Bootstrap 3.3.6](http://getbootstrap.com/), augmenté du [Bootstrap Material Design](http://fezvrasta.github.io/bootstrap-material-design/).  

## Contributeurs / Remerciements

Projet à l'initiative de [Nicolas Bonfante](https://github.com/niosega).  
Réalisation par [Loïc Touzard](https://github.com/LoicTouzard) (Responsable Front), [Paul Dautry](https://github.com/pdautry) (Responsable Back) et [Kévin Bulmé](https://github.com/KevinBulme).  
Remerciements à [Lisa Courant](https://github.com/lisacourant) pour le logo.  

# MapIf
![Mapif-logo](src/static/favicon.png "Mapif-logo")   
Où sont les IF ?  ICI --> [mapif en ligne](https://mapif-insa.rhcloud.com)  

## Le projet

Ce projet est né de l'esprit de quelques 4IF au moment critique qu'est le stage, veille du départ en échange pour une majorité d'entre eux. Cette épreuve qu'est la séparation n'étant pas facile à vivre, ils ont décidé de développer cette petite application permettant de connaître les endroits où se trouvent leurs amis et où ils se trouvent eux mêmes.  

## Contribuer

Allez faire un tour sur le [CONTRIBUTING.md](CONTRIBUTING.md) tout y est expliqué !
Si vous avez une seulement une idée de fonctionnalité n'hésitez pas à la partager dans les [issues](https://github.com/LoicTouzard/MapIf/issues).  

## Environnement de développement

### Back

Le code du serveur est développé en [Python 3](https://www.python.org/downloads/) actuellement en version `3.5.3`.
Le back utilise [Flask](http://flask.pocoo.org/), et d'autres librairies python renseignées dans le fichier [requirements.txt](requirements.txt).  

  1. Installez les dépendances en executant `pip install -r requirements.txt`.
  2. En cas d'erreur de dépendances pip concernant PostgreSQL, exécutez la commande suivante : 
      1. `sudo apt-get install postgresql python-psycopg2 libpq-dev`,
      2. puis relancez l'installation des dépendances `pip install -r requirements.txt`.
  3. Vous aurez besoin également de créer le fichier de configuration `mapif.ini` pour ce, prenez exemple sur le fichier [mapif.ini.dist](mapif.ini.dist).
  4. Pour faire fonctionner reCAPTCHA, il vous faudra entrer votre [clé secrète reCAPTCHA](https://www.google.com/recaptcha/admin#list) dans [mapif.ini.dist](mapif.ini.dist) (votre propre fichier `mapif.ini`, pas le `mapif.ini.dist`), ainsi que la clé de site dans `src/templates/modals/signupModal.html`, dans l'attribut `data-sitekey`.
  5. Vous devez également créer au choix le fichier `database/mapif.sqlite` à la racine du projet ou mettre en place une base [PostgreSQL](https://www.postgresql.org).
  
Concernant le lancement de l'application deux possibilités :
  1. Pour les développeurs : 
      1. Lancer l'application avec un simple `python3 main.py` devrait suffire.  
      2. Vous devriez pouvoir y accéder sur [http://localhost:5000](http://localhost:5000).
      3. Si vous souhaitez que le serveur écoute les connexions extérieures, remplacez `localhost` par `0.0.0.0` dans     
      `src/mapif.py`, et entrez l'adresse IP du serveur suivie de `:5000` dans `src/static/settings.json` (champ SERVER_ADDR).
  2. Pour un déploiement en production utilisez uWSGI via le script [mapif.sh](mapif.sh).

### Front

Le front est développé en [HTML5](http://www.w3schools.com/html/html5_intro.asp), [CSS3](http://www.w3schools.com/css/css3_intro.asp), [javascript ECMA5](https://developer.mozilla.org/fr/docs/Web/JavaScript/Language_Resources).  
Le moteur de template utilisé est [Jinja2](http://jinja.pocoo.org/docs/dev/).  
Le code exploite principalement [jQuery 2.2.3](http://jquery.com/) pour la gestion des évènements et animations, [Leaflet.js](http://leafletjs.com/) pour la gestion de la carte, et [Nominatim d'OpenStreetMap](http://nominatim.openstreetmap.org/) pour la résolution d'adresse.  
Pour le style il s'agit de [Bootstrap 3.3.6](http://getbootstrap.com/), augmenté du [Bootstrap Material Design](http://fezvrasta.github.io/bootstrap-material-design/).  
Le javascript est organisé de la manière suivante :
  * Le code commun à toutes les pages se trouve dans [app.js](src\static\js\app.js)  
  * Le code qui peut etre commun a plusieurs page est organisé par [modules](src\static\js\modules). Ces modules sont des objets qui agissent comme des bibliothèques à fonctions triées par fonctionnalité. Leurs dépendances sont notées en haut des fichiers, si vous en utilisez un veillez à inclure le script des dépendances.
  * Le code particulier à une page se trouve dans les fichiers [pages](src\static\js\pages). Les modules y sont chargés, ainsi que leur dépendances, et initialisés si besoin.

Pour la compatibilité, tout n'a pas été testé, mais cela fonctionne correctement sur la majorité des navigateurs récents.

## Contributeurs / Remerciements

Projet à l'initiative de [Nicolas Bonfante](https://github.com/niosega).  
Réalisation par [Loïc Touzard](https://github.com/LoicTouzard) (Responsable Front), [Paul Dautry](https://github.com/pdautry) (Responsable Back) et [Kévin Bulmé](https://github.com/KevinBulme).  
Remerciements aux contributeurs [Lisa Courant](https://github.com/lisacourant) pour le logo, [Mohamed Haidara](https://github.com/haidaraM/) et [David Wobrock](https://github.com/David-Wobrock).  

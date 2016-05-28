/* MapModule.js
*
* function related to the map wrapper over Leaflet API
*
* Dependancies : 
* 	SETTINGS
*/

var MapModule = {
	map : undefined,
	cluster : L.markerClusterGroup({
		iconCreateFunction: function (cluster) {
			// get all markers of this cluster
			var markers = cluster.getAllChildMarkers();
			var nbIfs = 0;

			// count the number of IFs in this cluster
			for (var i = 0; i < markers.length; i++) {
				nbIfs += markers[i].nbIfs;
			}

			// use default method to set css class
			var className = ' marker-cluster-';
			if (nbIfs < 10) {
				className += 'small';
			} else if (nbIfs < 20) {
				className += 'medium';
			} else {
				className += 'large';
			}

			return new L.DivIcon({
				html: '<div><span>' + nbIfs + '</span></div>',
				className: 'marker-cluster' + className,
				iconSize: new L.Point(40, 40,false)
			});
		}
	}),

	init : function(){
		this.map = L.map('mymap').setView(SETTINGS.GEOPOSITIONS.INSALYON)
			.setMaxBounds([SETTINGS.GEOPOSITIONS.WORLD_SOUTHWEST, SETTINGS.GEOPOSITIONS.WORLD_NORTHEAST])
			.setZoom(2);

		// different maps providers

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
			maxZoom: 18,
			minZoom: 2,
			id: 'ltouzard.0390bjno',
			accessToken: SETTINGS.MAPBOXTOKEN,
			noWrap: true
		}).addTo(this.map);
		// add marker to insa
		//L.marker(SETTINGS.GEOPOSITIONS.INSALYON).addTo(rhis.map)
		//  .bindPopup('Bienvenue à l\'INSA !');
		
		this.map.on('click', function(e) {
			UtilsModule.logger("CLICK : Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
		});
	},

	loadLocations : function(locations){
			// add markers for locations of users
		for (var i = 0; i < locations.length; i++) {
			var location = locations[i].location;
			var users = locations[i].users;

			var popupText = "<h4>"+users.length+" Insalien"+((users.length>1)?"s":"")
				+" à "+location.city+" "+location.country.toUpperCase()+"</h4><div class='popupUsers'>";
			for (var j = 0; j < users.length; j++) {
				popupText += users[j].firstname + " "+users[j].lastname+" "+users[j].promo+"<br>";
			};
			popupText += "</div>";

			var marker = L.marker([location.lat, location.lon]);
			marker.nbIfs = users.length;
			marker.addTo(this.cluster).bindPopup(popupText);

			// ajouter des binds ?
		};

		this.map.addLayer(this.cluster);
	}
};
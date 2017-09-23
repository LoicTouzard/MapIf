/* MapModule.js
*
* function related to the map wrapper over Leaflet API
*
* Dependancies : 
* 	SETTINGS
*/

var MapModule = {
	map : undefined,
	control : L.control.layers(),
	selectedPromos : [],
	clusterGroup : L.markerClusterGroup({
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

	newLocationIcon : function(){
		return new L.DivIcon({
			html: '<i class="material-icons">person_pin</i>',
			className: 'marker-location',
			popupAnchor:new L.Point(0, -40, false),
			iconSize: new L.Point(40, 40, false)
		})
	},

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

		this.control.addTo(this.map);
		$(MapModule.control.getContainer())
			.find(".leaflet-control-layers-overlays")
				.prepend("<h6>Promotions</h6>")
	},

	loadLocations : function(locations){
		var promotions = [];// array containing array of positions groupped by promotion
		// add markers for locations of users

		for (var i = 0; i < locations.length; i++) {

			var marker = this.createMarker(locations[i]);
			marker.addTo(this.clusterGroup)
		};
		
		this.map.addLayer(this.clusterGroup);
	},

	reloadLocations : function(locations){
		this.clusterGroup.clearLayers()
		this.loadLocations(locations);
	},

	getSelectedLocations : function(){
		var _module = this;
		var loc = [];
		locations.forEach(function(val1, key1, arr1){
			loc[key1] = {
				location: val1.location,
				users: val1.users.filter(function(user, key2, arr2){
			    	return _module.selectedPromos.indexOf(user.promo) !== -1;
				})
			};
		});
		return loc.filter(function(val1, key1, arr1){
			return arr1[key1].users.length > 0;
		});
	},

	createMarker : function(locationItem){
		var location = locationItem.location;
		var users = locationItem.users;
		var popupText = "<h4>"+users.length+" Insalien"+((users.length>1)?"s":"")
			+" à "+location.city+" "+location.country.toUpperCase()+"</h4><div class='popupUsers'>";
		for (var j = 0; j < users.length; j++) {
			popupText += UtilsModule.toTitleCase(users[j].firstname)+" "+UtilsModule.toTitleCase(users[j].lastname)+" <small> - IF "+users[j].promo+"</small><br>";
		};
		popupText += "</div>";

		var marker = L.marker([location.lat, location.lon],{icon: this.newLocationIcon()});
		marker.nbIfs = users.length;
		var _module = this;
		marker.bindPopup(popupText).on("click", function(e){
			_module.map.panTo(this.getLatLng());
		});
		return marker;
	},

	// factice overlay selector
	addPromoOverlayToControl: function(promotion){
		if(typeof promotion !== "string" && typeof promotion !== "undefined" && promotion.toString){
			promotion = promotion.toString();
		}
		var $selector = $('<label><input class="leaflet-control-layers-selector" type="checkbox" checked><span> '+promotion+'</span></label>');
		var $selectorContainers = $(MapModule.control.getContainer()).find(".leaflet-control-layers-overlays");
		var _module = this;
		$selectorContainers.append($selector);
		$selector.unbind();
		$selector.find(".leaflet-control-layers-selector").on("change", function(e){
			e.stopPropagation();
			var index = _module.selectedPromos.indexOf(promotion);
			if($(this).is(':checked')){
				// add promotion
				if(index === -1){
					_module.selectedPromos.push(promotion);
					_module.selectedPromos.sort();
				}
			}
			else{
				// remove promotion
				if(index !== -1){
					_module.selectedPromos.splice(index,1);
				}
			}
			UtilsModule.logger(_module.selectedPromos);
			_module.reloadLocations(_module.getSelectedLocations());
		});
		$selector.click(function(e){e.stopPropagation();});
		_module.selectedPromos.push(promotion);
	},

	clearControl: function(){
		var controlHTML = this.control.getContainer();
		if(typeof controlHTML !== "undefined"){
			$(controlHTML).find(".leaflet-control-layers-overlays").empty();
		}
		return this.control;
	}
};
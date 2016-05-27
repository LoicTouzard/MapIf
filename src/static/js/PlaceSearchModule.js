/* PlaceSearchModule.js
*
* function related to search and map manipulation
*
* Dependancies : 
* 	SETTINGS
* 	UtilsModule.js
*/

PlaceSearchModule = {
	mymap : undefined,
	feature : undefined,
	selected_osm  : 0,

	chooseAddr : function (element, lat1, lng1, lat2, lng2, osm_type, osm_id) {
		$el = $(element);
		$el.closest(".list-group").find(".list-group-item").removeClass("selected");
		$el.addClass("selected");

		this.selected_osm = osm_id;


		var loc1 = new L.LatLng(lat1, lng1);
		var loc2 = new L.LatLng(lat2, lng2);
		var bounds = new L.LatLngBounds(loc1, loc2);

		if (this.feature) {
			this.mymap.removeLayer(this.feature);
			this.feature = undefined;
		}

		var loc3 = new L.LatLng(lat1, lng2);
		var loc4 = new L.LatLng(lat2, lng1);

		this.feature = L.polyline( [loc1, loc4, loc2, loc3, loc1], {color: 'red'}).addTo(this.mymap);
		this.mymap.fitBounds(bounds);
		this.mymap.zoomOut();

		return false;
	},

	addrSearch : function () {
	    var city = document.getElementById("addr-search-input-city");
	    var country = document.getElementById("addr-search-input-country");
	    UtilsModule.logger("request for "+city.value +" "+country.value)
	    var num_search = 0;
	    var that = this;
	    var display_result = function(data) {
	        var items = [];
	        num_search += 1;
	        UtilsModule.logger("request num"+num_search);
	    	UtilsModule.logger(data)
	        $.each(data, function(key, val) {
	        	if(((val.class == "place" && (val.type == "city" || val.type == "town" || val.type == "village" || val.type == "county"))
	        		|| (val.class == "boundary" && val.type == "administrative"))
	        		&& val.address.city && val.address.country
	        		&& val.osm_type!= "way"){
	    			UtilsModule.logger(val)
		            var bb = val.boundingbox;
					var $item;
					if(connected){
						// with button
						var $item = $('<div></div>')
			            	.addClass("list-group-item place-result-item media")
			            	.click(function(e){
			            		e.preventDefault();
			            		that.chooseAddr(this, bb[0], bb[2], bb[1], bb[3], val.osm_type, val.osm_id);
			            		return false;
			            	}).append($("<div></div>")
			            		.addClass("media-body")
			            		.append($("<h4></h4>")
				            		.text(val.address.city+' '+val.address.country.toUpperCase())
				            		.addClass("list-group-item-heading")
				            	)
			            		.append($("<p></p>")
				            		.text(val.display_name)
				            		.addClass("list-group-item-text")
				            	)
			            	).append($("<div></div>")
			            		.addClass("media-right media-middle btn-group-sm")
			            		.append($("<span></span>")
			            			.addClass("btn btn-success btn-raised btn-fab fab")
			            			.attr("title", "En faire ma position actuelle")
					            	.attr("data-toggle","modal")
					            	.attr("data-target", "#positionModal")
					            	.click(function(e){
				            			e.preventDefault();
				            			e.stopPropagation();
				            			// CONFIRM MODAL
					            		$("#change-current-position-validate").on("click",function(){
					            			e.preventDefault();
					            			e.stopPropagation();
					            			AjaxModule.addLocation(val.osm_type, val.osm_id);
					            			return false;
					            		})
					            		$("#position-add-city").text(val.address.city);
					            		$("#position-add-country").text(val.address.country.toUpperCase());
					            		$("#positionModal").modal("show");
				            			return false
				            		})
				            		.append($('<i></i>')
				            			.addClass("material-icons")
				            			.text("add")
				            		)
			            		)
			            	);
					}
					else{
			            var $item = $('<div></div>')
			            	.addClass("list-group-item place-result-item")
			            	.click(function(e){
			            		e.preventDefault();
			            		that.chooseAddr(this, bb[0], bb[2], bb[1], bb[3], val.osm_type, val.osm_id);
			            		return false;
			            	}).append($("<h4></h4>")
			            		.text(val.address.city+' '+val.address.country.toUpperCase())
			            		.addClass("list-group-item-heading")
			            	).append($("<p></p>")
			            		.text(val.display_name)
			            		.addClass("list-group-item-text")
			            	);
					}
		            items.push($item);
		            items.push($("<hr>"));
	        	}
	        });

			$('#search-results').empty();
	        if (items.length != 0) {
	        	$('<h4>').text("Recherche de villes pour \""+city.value+" "+country.value+"\" : ").appendTo('#search-results');
	            $('<div></div>').addClass("list-group")
	            	.append(items)
	            	.appendTo('#search-results');
	    		$.material.ripples('.place-result-item');
	    		$.material.ripples('.media-right .fab');
	        } else {
	        	if (num_search > 1) {
	            	$('<h4 class="no-result">').text("Pas de ville pour \""+city.value+" "+country.value+"\"...").appendTo('#search-results');
	            	$('<p class="no-result">').html("Pour trouver un résultat vous pouvez : <ol><li>Vérifier l'orthographe de votre recherche</li><li>Chercher une ville plus grande proche de la votre</li><li>Nous contacter en nous donnant votre recherche exacte, le big data n'est pas une science exacte ...</li></ol>").appendTo('#search-results');
	        	}
	        	else{
	        		// let's try a more permissive search
	        		 $.getJSON(SETTINGS.PROTOCOL + '://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=20&q=' + city.value + " "+country.value, display_result);
	        	}
	        }

	    }

	    $.getJSON(SETTINGS.PROTOCOL + '://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=20&city=' + city.value + "&country="+country.value, display_result);

	    $('<h4 class="no-result">').text("Recherche de ville pour \""+city.value+" "+country.value+"\" en cours...").appendTo('#search-results');

	    if (this.feature) {
			this.mymap.removeLayer(this.feature);
			this.feature = undefined;
		}
	}
};

SETTINGS = {
	'MAPBOXTOKEN':'pk.eyJ1IjoibHRvdXphcmQiLCJhIjoiY2lvMGV5OTJhMDB2Y3dka2xrZHpycGlrZiJ9.70MUkG_bCx7MPyIOhwfcKA',
	'GEOPOSITIONS':{
		'INSALYON':[45.7832543, 4.8780048]
	},
	'SERVER_ADDR':"http://localhost:5000",
	'DEBUG':true
}

// create an alert element with given content
var createAlert = function(msg){
	return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Bah alors ?!</strong> '+msg+'</div>');
}

var logger = function(msg){
	if(SETTINGS.DEBUG){
		console.log(msg);
	}
}

var handleServerError = function(code){
	createSnackbar(code);
}


/********* MAP *********/

var mymap
var feature;
var selected_osm = 0;

var chooseAddr = function (element, lat1, lng1, lat2, lng2, osm_type, osm_id) {
	$el = $(element);
	$el.closest(".list-group").find(".list-group-item").removeClass("selected");
	$el.addClass("selected");

	selected_osm = osm_id;


	var loc1 = new L.LatLng(lat1, lng1);
	var loc2 = new L.LatLng(lat2, lng2);
	var bounds = new L.LatLngBounds(loc1, loc2);

	if (feature) {
		mymap.removeLayer(feature);
		feature = undefined;
	}

	var loc3 = new L.LatLng(lat1, lng2);
	var loc4 = new L.LatLng(lat2, lng1);

	feature = L.polyline( [loc1, loc4, loc2, loc3, loc1], {color: 'red'}).addTo(mymap);
	mymap.fitBounds(bounds);
	mymap.zoomOut();

	return false;
}

var addrSearch = function () {
    var city = document.getElementById("addr-search-input-city");
    var country = document.getElementById("addr-search-input-country");
    logger("request for "+city.value +" "+country.value)
    var num_search = 0;
    var display_result = function(data) {
        var items = [];
        num_search += 1;
        logger("request num"+num_search);
    	logger(data)
        $.each(data, function(key, val) {
        	if(((val.class == "place" && (val.type == "city" || val.type == "town" || val.type == "village" || val.type == "county"))
        		|| (val.class == "boundary" && val.type == "administrative"))
        		&& val.address.city && val.address.country
        		&& val.osm_type!= "way"){
    			logger(val)
	            var bb = val.boundingbox;
				var $item;
				if(connected){
					// with button
					var $item = $('<div></div>')
		            	.addClass("list-group-item place-result-item media")
		            	.click(function(e){
		            		e.preventDefault();
		            		chooseAddr(this, bb[0], bb[2], bb[1], bb[3], val.osm_type, val.osm_id);
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
				            			ajaxAddLocation(val.osm_type, val.osm_id);
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
		            		chooseAddr(this, bb[0], bb[2], bb[1], bb[3], val.osm_type, val.osm_id);
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
        		 $.getJSON('http://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=20&q=' + city.value + " "+country.value, display_result);
        	}
        }

    }

    $.getJSON('http://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=20&city=' + city.value + "&country="+country.value, display_result);

    $('<h4 class="no-result">').text("Recherche de ville pour \""+city.value+" "+country.value+"\" en cours...").appendTo('#search-results');

    if (feature) {
		mymap.removeLayer(feature);
		feature = undefined;
	}
}


/********* PROFIL *********/

var checkAcountDelete = function(){
	$input = $(this);
	$confirm = $("#delete-button-confirm");
	if($input.val() === "je sui 1 gro boloss"){
		$confirm.removeAttr("disabled");
		$confirm.bind("click", ajaxDeleteAccount);
	}
	else{
		$confirm.attr("disabled", "disabled");
		$confirm.unbind("click", ajaxDeleteAccount);
	}
}

/********* FORM VALIDATION *********/

var p3_trolled = false;
var p3_open = false;
var $p3_block;
var $p3_msg;

var addFieldError = function($el){
	return $el.addClass("has-warning");
}

var removeFieldError = function($el){
	return $el.removeClass("has-warning");
}

var checkPasswords = function(){
	$p1 = $("#form-inscription-input-password1");
	p1 = $p1.val();
	$p2 = $("#form-inscription-input-password2");
	p2 = $p2.val();
	$p3 = $("#form-inscription-input-password3");
	p3 = $p3.val();
	if($p2.val() != ""){
		// check similarity with p1
		if(p1 != p2){
			addFieldError($p2.closest(".form-group"));
		}
		else{
			removeFieldError($p2.closest(".form-group"));
			if(!p3_open && !p3_trolled){
				//activate the troll not finished
				$p3_block.show(500);
				p3_open = true;
			}
		}
	}
	else{
		//addFieldError($p2.closest(".form-group"));
	}
	if(p3_open){
		if(p3 != ""){
			// check similarity with p1
			if(p1 != p3){
				addFieldError($p3.closest(".form-group"));
			}
			else{
				removeFieldError($p3.closest(".form-group"));
			}
		}
		else{
			// addFieldError($p3.closest(".form-group"));
		}
	}
	if(p1 != "" && p1 == p2 && p1 == p3){
		//validé !
		if(!p3_trolled){
			//activate the troll not finished
			$p3_block.hide(500);
			$p3_msg.show(500);
			p3_open = false;
			p3_trolled = true;
		}
	}
}

var displayFormErrors = function(form, errors){
    $form = $(form);
	// remove the old errors
	$form.find(".alert.alert-danger").remove();
	removeFieldError($form.find(".has-warning"));
	if(typeof errors.content == "string"){
		// single message
		$form.find(".modal-body").prepend(createAlert(errors.content));
	}
	else{
		// error is array
		for (var field in errors.content){
		    if (errors.content.hasOwnProperty(field)) {
		    	$fgroup = $(form+"-input-"+field).closest(".form-group");
		    	addFieldError($fgroup);
		    	$fgroup.prepend(createAlert(errors.content[field]));
		    }
		}
	}
}


/********* LEFT PANEL *********/

var leftPanelOpen = function(){
	$("#left-panel").removeClass("closePanel");
	$("#left-panel .widget-pane-toggle-button-container .btn").focusout().blur()
		.attr('data-original-title', "Réduire le panneau latéral")
		.find(".glyphicon").removeClass("glyphicon-triangle-right")
		.addClass("glyphicon-triangle-left");

	$("#menu-map").removeClass("active");
	$("#menu-search").addClass("active");
}

var leftPanelClose = function(){
	$("#left-panel").addClass("closePanel");
	$("#left-panel .widget-pane-toggle-button-container .btn").focusout().blur()
		.attr('data-original-title', "Étendre le panneau latéral")
		.find(".glyphicon").removeClass("glyphicon-triangle-left")
		.addClass("glyphicon-triangle-right");

	$("#menu-search").removeClass("active");
	$("#menu-map").addClass("active");
}

var leftPanelIsOpen = function(){
	return !$("#left-panel").hasClass("closePanel");
}

var leftPanelToggle = function(){
	if(leftPanelIsOpen()){
		leftPanelClose();
	}
	else{
		leftPanelOpen();
	}
}


/********* AJAX *********/

var ajaxLogin = function(e) {
    e.preventDefault();
    e.stopPropagation();
    $this = $(this);

    // TODO (or not) add form verification

		$.ajax({
        method: "POST",
        url: SETTINGS.SERVER_ADDR + "/login",
        data: $this.serialize(),
        cache: false,
        success: function(json){
            logger("AJAX OK");
            logger(json);
            if(!json.has_error){
            	//refresh en etant connecté au server
            	logger("CONNEXION");
        		location.reload(true);
            }
            else{
            	displayFormErrors("#form-connexion", json);
            }
        },
        error: function(resp, statut, erreur){
        	jsonResp = JSON.parse(resp.responseText);
        	handleServerError(jsonResp.code)
            logger("AJAX NOK");
        },
        complete: function(){
            logger("AJAX DONE");
        }
    });
	return false;
}

var ajaxSignup = function(e) {
    e.preventDefault();
    e.stopPropagation();
    $this = $(this);

    //ajouter form verification
	$.ajax({
	    method: "POST",
	    url: SETTINGS.SERVER_ADDR + "/signup",
	    data: $this.serialize(),
	    cache: false,
	    success: function(json){
            logger("AJAX OK");
            logger(json);
            if(!json.has_error){
            	//refresh en etant connecté au server
            	logger("REGISTERED");
        		location.reload(true);
            }
            else{
            	displayFormErrors("#form-inscription", json);
            }
        },
        error: function(resp, statut, erreur){
        	jsonResp = JSON.parse(resp.responseText);
        	handleServerError(jsonResp.code)
            logger("AJAX NOK");
        },
        complete: function(){
            logger("AJAX DONE");
        }
    });
	return false;
}


var ajaxAddLocation = function(osm_type, osm_id){
	var $params = $.param({
		'osm_id' : osm_id,
		'osm_type' : osm_type
	});
	$.ajax({
        method: "POST",
        url: SETTINGS.SERVER_ADDR + "/addlocation",
        data: $params,
        cache: false,
        success: function(json){
            logger("AJAX OK");
            logger(json);
            if(!json.has_error){
            	//refresh en etant connecté au server
            	logger("ADDED");
        		location.reload(true);
            }
            else{
            	alert("une erreur est survenue has_error")
            }
        },
        error: function(resp, statut, erreur){
        	jsonResp = JSON.parse(resp.responseText);
        	handleServerError(jsonResp.code)
            logger("AJAX NOK");
        },
        complete: function(){
            logger("AJAX DONE");
        }
    });
	return false;
}

var ajaxDeleteAccount = function(){
	$.ajax({
        method: "DELETE",
        url: SETTINGS.SERVER_ADDR + "/delete/account",
        cache: false,
        success: function(json){
            logger("AJAX OK");
            logger(json);
            if(!json.has_error){
            	//refresh en etant connecté au server
        		location.reload(true);
            }
        },
        error: function(resp, statut, erreur){
        	jsonResp = JSON.parse(resp.responseText);
        	handleServerError(jsonResp.code)
            logger("AJAX NOK");
        },
        complete: function(){
            logger("AJAX DONE");
        }
    });
	return false;
}




/******* JQUERY ON LOAD - BINDS *******/
$(function(){
	// Material Init
	$.material.init();

	$("body").tooltip({ selector: '[data-toggle=tooltip]' });

	logger(Cookies.get("visited"))
	// show about if it is the first visit
	if(!Cookies.get("visited")){
		Cookies.set('visited', 'visited', { expires: 365 });
		$("#aboutModal").modal("show");
	}	
	// generate the promotions year
	(function(){
		var startYear = 1969;
		var currentYear = new Date().getFullYear();
		var lastYear = currentYear+4;
		var $select = $("#form-inscription-input-promo");
		for (var i = startYear; i < lastYear; i++) {
			var $option = $('<option value="'+i+'">'+i+'</option>');
			if(i == currentYear){
				$option.attr("selected", "selected");
			}
			$select.append($option);
		};
	})()

	


	/********* MAP *********/

	mymap = L.map('mymap').setView(SETTINGS.GEOPOSITIONS.INSALYON).fitWorld().zoomIn();

	// different maps providers
	
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		minZoom: 2,
		id: 'ltouzard.0390bjno',
		accessToken: SETTINGS.MAPBOXTOKEN
	}).addTo(mymap);
	/*
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		attribution: 'Map data &copy; 2012 <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
		maxZoom: 18
	}).addTo(mymap);
	*/
	// add marker to insa
	L.marker(SETTINGS.GEOPOSITIONS.INSALYON).addTo(mymap)
	    .bindPopup('Bienvenue à l\'INSA !');

	// add markers for locations of users
	for (var i = 0; i < locations.length; i++) {
		var location = locations[i].location;
		var users = locations[i].users;

		var popupText = "<h4>"+users.length+" Insalien"+((users.length>1)?"s":"")
			+" à "+location.city+" "+location.country.toUpperCase()+"</h4><div class='popupUsers'>";
		for (var j = 0; j < users.length; j++) {
			popupText += users[j].firstname + " "+users[j].lastname+"<br>";
		};
		popupText += "</div>";

		L.marker([location.lat, location.lon]).addTo(mymap)
		    .bindPopup(popupText);

		// ajouter des binds ?
	};

	mymap.on('click', function(e) {
	    logger("CLICK : Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
	});



	/********* FORM VALIDATION *********/

	$p3_block = $("#p3-block").hide();
	$p3_msg = $("#p3-msg").hide();

	$("#form-inscription-input-password1, #form-inscription-input-password2, #form-inscription-input-password3").keyup(function(){
		checkPasswords();
	});


	/********* LEFT PANEL *********/

	$("#menu-search").click(leftPanelOpen);
	$("#menu-map").click(leftPanelClose);

	$("#left-panel .widget-pane-toggle-button-container .btn").on("click",function(){
		leftPanelToggle();
	});

	$("#addr-search-submit").click(function(e){
		e.preventDefault();
		addrSearch();
		logger($(this));
		// TODO focusout not working, need to find why. --> Okay nvm may depend on the browser
		$(this).focusout().blur();
		return false;
	});

	$("#addr-search-input-city, #addr-search-input-country").keypress(function(e) {
	    if(e.which == 13) {
	        $("#addr-search-submit").click();
	    }
	});


	/********* MENU *********/

	$("#menu-search, #menu-map").click(function(e){
		e.preventDefault();
		$(".navbar-left-item").removeClass("active");
		$(this).addClass("active");
	});

	$('#aboutModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-about").addClass("active");
	});

	$('#profilModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-profil").addClass("active");
	})

	$('#aboutModal, #profilModal').on('hide.bs.modal', function(e){
	    $(".navbar-left-item").removeClass("active");
	    if(leftPanelIsOpen()){
	    	$("#menu-search").addClass("active");
	    }
	    else{
	    	$("#menu-map").addClass("active");
	    }
	});


	/********* PROFIL *********/
	
	$("#delete-input").keyup(checkAcountDelete).val("");

	$("#delete-button-confirm").attr("disabled", "disabled");

	/********* AJAX *********/
	
	$('#form-connexion').on('submit', ajaxLogin);

    $('#form-inscription').on('submit', ajaxSignup);
});
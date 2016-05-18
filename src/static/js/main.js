SETTINGS = {
	'MAPBOXTOKEN':'pk.eyJ1IjoibHRvdXphcmQiLCJhIjoiY2lvMGV5OTJhMDB2Y3dka2xrZHpycGlrZiJ9.70MUkG_bCx7MPyIOhwfcKA',
	'GEOPOSITIONS':{
		'INSALYON':[45.7832543, 4.8780048]
	},
	'SERVER_ADDR':"http://localhost:5000"
}

// create an alert element with given content
var createAlert = function(msg){
	return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Bah alors ?!</strong> '+msg+'</div>');
}



/********* MAP *********/
var mymap
var feature;

var chooseAddr = function (lat1, lng1, lat2, lng2, osm_type) {
	var loc1 = new L.LatLng(lat1, lng1);
	var loc2 = new L.LatLng(lat2, lng2);
	var bounds = new L.LatLngBounds(loc1, loc2);

	if (feature) {
		mymap.removeLayer(feature);
	}
	if (osm_type == "node") {
		feature = L.circle( loc1, 25, {color: 'green', fill: false}).addTo(mymap);
		mymap.fitBounds(bounds);
		mymap.setZoom(18);
	} else {
		var loc3 = new L.LatLng(lat1, lng2);
		var loc4 = new L.LatLng(lat2, lng1);

		feature = L.polyline( [loc1, loc4, loc2, loc3, loc1], {color: 'red'}).addTo(mymap);
		mymap.fitBounds(bounds);
	}
}

var addrSearch = function () {
    var city = document.getElementById("addr-search-input-city");
    var country = document.getElementById("addr-search-input-country");
    console.log("request for "+city.value +" "+country.value)
    $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=5&city=' + city.value + "&country="+country.value, function(data) {
        var items = [];

    	console.log(data)
        $.each(data, function(key, val) {
            bb = val.boundingbox;
            item = '<div class="list-group-item"><div class="row-action-primary checkbox">  <label><input type="radio" name="result-choice"></label></div><div class="row-content">  <h4 class="list-group-item-heading">Tile with a checkbox in it</h4>  <p class="list-group-item-text"><a href="#"onclick="chooseAddr(' + bb[0] + ', ' + bb[2] + ', ' + bb[1] + ', ' + bb[3]  + ', "' + val.osm_type + '");return false;"">' + val.display_name + '</a></p></div></div><div class="list-group-separator"></div>';
            items.push(item);
        });

		$('#search-results').empty();
        if (items.length != 0) {
            $('<p>', { html: "Search results:" }).appendTo('#search-results');
            $('<div></div>').addClass("list-group")
            	.html(items.join(''))
            	.appendTo('#search-results');
        } else {
            $('<p>', { html: "No results found" }).appendTo('#search-results');
        }
    });
}



/********* FORM VALIDATION *********/
var p3_trolled = false;
var p3_open = false;
var $p3_block = $("#p3-block").hide();
var $p3_msg = $("#p3-msg").hide();

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
		$("#left-panel .widget-pane-toggle-button-container .btn").focusout()
			.attr('data-original-title', "Réduire le panneau latéral")
			.find(".glyphicon").removeClass("glyphicon-triangle-right")
			.addClass("glyphicon-triangle-left");
}

var leftPanelClose = function(){
	$("#left-panel").addClass("closePanel");
		$("#left-panel .widget-pane-toggle-button-container .btn").focusout()
			.attr('data-original-title', "Étendre le panneau latéral")
			.find(".glyphicon").removeClass("glyphicon-triangle-left")
			.addClass("glyphicon-triangle-right");
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




/******* JQUERY ON LOAD - BINDS *******/
$(function(){
	// Material Init
	$.material.init();

	$("body").tooltip({ selector: '[data-toggle=tooltip]' });
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

	mymap = L.map('mapid').setView(SETTINGS.GEOPOSITIONS.INSALYON, 13);

	// different maps providers
	
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
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
	    .bindPopup('Bienvenu(e) à l\'INSA.')
	    .openPopup();

	for (var i = users.length - 1; i >= 0; i--) {
		L.marker([users[i].lat, users[i].lon]).addTo(mymap)
		    .bindPopup(users[i].firstname + " " + users[i].lastname);

		// ajouter des binds ?
	};



	$("#addr-search-submit").click(function(e){
		e.preventDefault();
		addrSearch();
		console.log($(this));
		// TODO focusout not working, need to find why
		$(this).focusout();
		return false;
	});


	/********* FORM VALIDATION *********/

	$("#form-inscription-input-password1, #form-inscription-input-password2, #form-inscription-input-password3").keyup(function(){
		checkPasswords();
	});


	/********* LEFT PANEL *********/

	$("#left-panel .widget-pane-toggle-button-container .btn").on("click",function(){
		leftPanelToggle();
	});


	/********* AJAX *********/
	
	$('#form-connexion').on('submit', function(e) {
        e.preventDefault();
        e.stopPropagation();
        $this = $(this);

        // ajouter form verification

 		$.ajax({
	        method: "POST",
	        url: SETTINGS.SERVER_ADDR + "/login",
	        data: $this.serialize(),
	        cache: false,
	        success: function(json){
	            console.log("AJAX OK");
	            console.log(json);
	            if(!json.has_error){
	            	//refresh en etant connecté au server
	            	console.log("CONNEXION");
            		location.reload(true);
	            }
	            else{
	            	displayFormErrors("#form-connexion", json);
	            }
	        },
	        error: function(resp, statut, erreur){
    			$this.find(".modal-body").prepend(createAlert("Erreur "+resp.status+" à la connexion : "+resp.statusText));
	            console.log("AJAX NOK");
	        },
	        complete: function(){
	            console.log("AJAX DONE");
	        }
	    });
		return false;
    });

    $('#form-inscription').on('submit', function(e) {
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
	            console.log("AJAX OK");
	            console.log(json);
	            if(!json.has_error){
	            	//refresh en etant connecté au server
	            	console.log("REGISTERED");
            		location.reload(true);
	            }
	            else{
	            	displayFormErrors("#form-inscription", json);
	            }
	        },
	        error: function(resp, statut, erreur){
	            console.log("AJAX NOK");
    			$this.find(".modal-body").prepend(createAlert("Erreur "+resp.code+" à l'inscription : "+resp.statusText));
	        },
	        complete: function(){
	            console.log("AJAX DONE");
	        }
	    });
		return false;
    });
});
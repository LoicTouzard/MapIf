/******* JQUERY ON LOAD - BINDS *******/

$("body").on("settings-loaded",function(){
	// Material Init
	$.material.init();

	$(".version").text(SETTINGS.VERSION);

	$("body").tooltip({ selector: '[data-toggle=tooltip]' });

	UtilsModule.logger(Cookies.get("visited"))
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

	PlaceSearchModule.mymap = L.map('mymap').setView(SETTINGS.GEOPOSITIONS.INSALYON)
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
	}).addTo(PlaceSearchModule.mymap);

	// add marker to insa
	//L.marker(SETTINGS.GEOPOSITIONS.INSALYON).addTo(PlaceSearchModule.mymap)
	  //  .bindPopup('Bienvenue à l\'INSA !');
    var markers = L.markerClusterGroup({
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
    });

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

        var marker = L.marker([location.lat, location.lon]);
        marker.nbIfs = users.length;
		marker.addTo(markers).bindPopup(popupText);

		// ajouter des binds ?
	};

    PlaceSearchModule.mymap.addLayer(markers);

	PlaceSearchModule.mymap.on('click', function(e) {
	    UtilsModule.logger("CLICK : Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng);
	});



	/********* FORM VALIDATION *********/

	FormModule.$p3_block = $("#p3-block").hide();
	FormModule.$p3_msg = $("#p3-msg").hide();

	$("#form-inscription-input-password1, #form-inscription-input-password2, #form-inscription-input-password3").keyup(function(){
		FormModule.checkPasswords();
	});


	/********* LEFT PANEL *********/

	$("#menu-search").click(LeftPanelModule.open);
	$("#menu-map").click(LeftPanelModule.close);

	$("#left-panel .widget-pane-toggle-button-container .btn").on("click",function(){
		LeftPanelModule.toggle();
	});

	$("#addr-search-submit").click(function(e){
		e.preventDefault();
		PlaceSearchModule.addrSearch();
		UtilsModule.logger($(this));
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

	$(".navbar-left-item").click(function(e){
		e.preventDefault();
		if(UtilsModule.onMobile() && UtilsModule.menuIsExpanded()){
			$("#main-navbar").collapse("hide");
		}
	})

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
	    if(LeftPanelModule.isOpen()){
	    	$("#menu-search").addClass("active");
	    }
	    else{
	    	$("#menu-map").addClass("active");
	    }
	});


	/********* PROFILE *********/
	
	$("#delete-input").keyup(ProfileModule.checkAcountDelete).val("");

	$("#delete-button-confirm").attr("disabled", "disabled");

	/********* AJAX *********/
	
	$('#form-connexion').on('submit', AjaxModule.login);

    $('#form-inscription').on('submit', AjaxModule.signup);
});
SETTINGS = {
	'MAPBOXTOKEN':'pk.eyJ1IjoibHRvdXphcmQiLCJhIjoiY2lvMGV5OTJhMDB2Y3dka2xrZHpycGlrZiJ9.70MUkG_bCx7MPyIOhwfcKA',
	'GEOPOSITIONS':{
		'INSALYON':[45.7832543, 4.8780048]
	},
	'SERVER_ADDR':"http://localhost:5000"
}

$(function(){
	// Material Init
	$.material.init();

	// Map init
	var mymap = L.map('mapid').setView(SETTINGS.GEOPOSITIONS.INSALYON, 13);

	// different maps providers
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
		maxZoom: 18,
		id: 'ltouzard.0390bjno',
		accessToken: SETTINGS.MAPBOXTOKEN
	}).addTo(mymap);

	// add marker to insa
	L.marker(SETTINGS.GEOPOSITIONS.INSALYON).addTo(mymap)
	    .bindPopup('Bienvenu(e) à l\'INSA.')
	    .openPopup();

	// generate the promotions year
	(function(){
		var startYear = 1970;
		var currentYear = new Date().getFullYear();
		var lastYear = currentYear+4;
		var $select = $("#form-inscription-input-promotion");
		for (var i = startYear; i < lastYear; i++) {
			var $option = $('<option value="'+i+'">'+i+'</option>');
			if(i == currentYear){
				$option.attr("selected", "selected");
			}
			$select.append($option);
		};
	})()

	// form validation
	/*
	function checkSame() {
	   var passwordVal = $("#form-inscription-input-password1").val();
	   var checkVal = $("#form-inscription-input-password2").val();
	   if (passwordVal == checkVal) {
	     return true;
	   }
	   return false;
	};
	$("#form-inscription-input-password1, #form-inscription-input-password2").keyup(function(){
		var $this = $(this); 
		updateError(checkSame());
	});
*/
	
	$('#form-connexion').on('submit', function(e) {
        e.preventDefault();
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
	            if(json.response.status == "ok"){
	            	//refresh en etant connecté au server
            		location.reload(true);
	            }
	            else if{
	            	
	            }
	            else{
					alert("authentification failed");
	            }
	        },
	        error: function(json, statut, erreur){
	            console.log("AJAX NOK");
	            alert("Désolé ! Une erreur serveur est survenue, réessayez, sinon actualisez la page.");
	        },
	        complete: function(){
	            console.log("AJAX DONE");
	        }
	    });
    });

    $('#form-inscription').on('submit', function(e) {
        e.preventDefault();
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
	            if(json.response.status == "ok"){
	            	//refresh en etant connecté au server
            		location.reload(true);
	            }
	            else if{
	            	
	            }
	            else{
					alert("authentification failed");
	            }
	        },
	        error: function(json, statut, erreur){
	            console.log("AJAX NOK");
	            alert("Désolé ! Une erreur serveur est survenue, réessayez, sinon actualisez la page.");
	        },
	        complete: function(){
	            console.log("AJAX DONE");
	        }
	    });
    });
});
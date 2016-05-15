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

	var createAlert = function(msg){
		return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Bah alors ?!</strong> '+msg+'</div>');
	}
	/********* MAP *********/

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

	for (var i = users.length - 1; i >= 0; i--) {
		L.marker([users[i].lat, users[i].lon]).addTo(mymap)
		    .bindPopup(users[i].firstname + " " + users[i].lastname);

		// ajouter des binds ?
	};



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

	$("#form-inscription-input-password1, #form-inscription-input-password2, #form-inscription-input-password3").keyup(function(){
		checkPasswords();
	});


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
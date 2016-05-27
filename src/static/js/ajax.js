/* ajax.js
*
* all ajax calls
*
* Dependancies : 
* 	SETTINGS
* 	utils.js
*/
var ajaxLogin = function(e) {
    e.preventDefault();
    e.stopPropagation();
    $this = $(this);

    // TODO (or not) add form verification

		$.ajax({
        method: "POST",
        url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/login",
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
	    url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/signup",
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
        url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/addlocation",
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
        url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/delete/account",
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


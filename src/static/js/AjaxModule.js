/* AjaxModule.js
*
* all ajax calls
*
* Dependancies : 
* 	SETTINGS
* 	UtilsModule.js
*   FormModule.js
*/
var AjaxModule = {
    login : function(e) {
        e.preventDefault();
        e.stopPropagation();
        // this is the form
        $this = $(this);

        // TODO (or not) add form verification
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/login",
            data: $this.serialize(),
            cache: false,
            success: function(json){
                UtilsModule.logger("AJAX OK");
                UtilsModule.logger(json);
                if(!json.has_error){
                    //refresh en etant connecté au server
                    UtilsModule.logger("CONNEXION");
                    location.reload(true);
                }
                else{
                    FormModule.displayFormErrors("#form-connexion", json);
                }
            },
            error: function(resp, statut, erreur){
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code)
                UtilsModule.logger("AJAX NOK");
            },
            complete: function(){
                UtilsModule.logger("AJAX DONE");
            }
        });
        return false;
    },

    signup : function(e) {
        e.preventDefault();
        e.stopPropagation();
        // this is the form
        $this = $(this);

        //ajouter form verification
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/account/create",
            data: $this.serialize(),
            cache: false,
            success: function(json){
                UtilsModule.logger("AJAX OK");
                UtilsModule.logger(json);
                if(!json.has_error){
                    //refresh en etant connecté au server
                    UtilsModule.logger("REGISTERED");
                    location.reload(true);
                }
                else{
                    FormModule.displayFormErrors("#form-inscription", json);
                }
            },
            error: function(resp, statut, erreur){
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code)
                UtilsModule.logger("AJAX NOK");
            },
            complete: function(){
                UtilsModule.logger("AJAX DONE");
            }
        });
        return false;
    },

    addLocation : function(osm_type, osm_id){
        var $params = $.param({
            'osm_id' : osm_id,
            'osm_type' : osm_type
        });
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/location/add",
            data: $params,
            cache: false,
            success: function(json){
                UtilsModule.logger("AJAX OK");
                UtilsModule.logger(json);
                if(!json.has_error){
                    //refresh en etant connecté au server
                    UtilsModule.logger("ADDED");
                    location.reload(true);
                }
                else{
                    alert("une erreur est survenue has_error")
                }
            },
            error: function(resp, statut, erreur){
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code)
                UtilsModule.logger("AJAX NOK");
            },
            complete: function(){
                UtilsModule.logger("AJAX DONE");
            }
        });
        return false;
    },

    deleteAccount : function(){
        $.ajax({
            method: "DELETE",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/account/delete",
            cache: false,
            success: function(json){
                UtilsModule.logger("AJAX OK");
                UtilsModule.logger(json);
                if(!json.has_error){
                    //refresh en etant connecté au server
                    location.reload(true);
                }
            },
            error: function(resp, statut, erreur){
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code)
                UtilsModule.logger("AJAX NOK");
            },
            complete: function(){
                UtilsModule.logger("AJAX DONE");
            }
        });
        return false;
    }
};
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
        $form = $(this);

        // TODO (or not) add form verification
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/login",
            data: $form.serialize(),
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
                    FormModule.displayModalFormErrors("#form-connexion", json);
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
        $form = $(this);

        //ajouter form verification
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/account/create",
            data: $form.serialize(),
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
                    FormModule.displayModalFormErrors("#form-inscription", json);
                    grecaptcha.reset();
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

    passwordForgotten: function(e) {
        e.preventDefault();
        e.stopPropagation();

        $form = $(this);
        $.ajax({
            method: 'POST',
            url: SETTINGS.PROTOCOL + '://' + SETTINGS.SERVER_ADDR + '/password',
            data: $form.serialize(),
            cache: false,
            success: function(data) {
                UtilsModule.logger("AJAX OK");
                if (!data.has_error) {
                    FormModule.displayModalFormSuccess('#form-password-forgotten', data);
                    var $submitButton = $form.find('button[type="submit"]')
                    $submitButton.attr("disabled","disabled");
                    setTimeout(function() {$submitButton.removeAttr("disabled");}, 30*1000);// prevent from click flooding within 30 seconds
                } else {
                    FormModule.displayModalFormErrors('#form-password-forgotten', data);
                }
            },
            error: function(resp, status, error) {
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code);
                UtilsModule.logger("AJAX NOK");
            }
        });
        return false;
    },

    addLocation : function(osm_type, osm_id, reason){
        var $params = $.param({
            'osm_id' : osm_id,
            'osm_type' : osm_type,
            'reason' : reason
        });
        $.ajax({
            method: "POST",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + "/user/location/create",
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
                    UtilsModule.handleServerError("N0M1N4T1M."+osm_id);
                }
            },
            error: function(resp, statut, erreur){
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code);
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
    },

    editProfile : function(form){
        var $form = $(form);
        $.ajax({
            method: "PATCH",
            url: SETTINGS.PROTOCOL + "://" + SETTINGS.SERVER_ADDR + $form.attr("action"),
            data: $form.serialize(),
            cache: false,
            success: function(json){
                UtilsModule.logger("AJAX OK");
                UtilsModule.logger(json);
                if(!json.has_error){
                    FormModule.displayFormSucess(form, "Modification enregistrée !");
                    //refresh en etant connecté au server
                    UtilsModule.logger("MODIFIED");
                }
                else{
                    FormModule.displayFieldFormErrors(form, json);
                }
            },
            error: function(resp, statut, erreur){
                UtilsModule.logger("AJAX NOK");
                jsonResp = JSON.parse(resp.responseText);
                UtilsModule.handleServerError(jsonResp.code)
            },
            complete: function(){
                UtilsModule.logger("AJAX DONE");
            }
        });
    }
};

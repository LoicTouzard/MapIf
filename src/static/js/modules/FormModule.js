/* FormModule.js
*
* form functions
*
* Dependancies : 
* 	UtilsModule.js
*/
var FormModule = {
	addFieldError : function($el){
		return $el.addClass("has-warning");
	},

	removeFieldError : function($el){
		return $el.removeClass("has-warning");
	},

	displayFormErrors : function(form, errors){
	    $form = $(form);
		// remove the old errors
		$form.find(".alert.alert-danger").remove();
		this.removeFieldError($form.find(".has-warning"));
		if(typeof errors.content == "string"){
			// single message
			$form.find(".modal-body").prepend(UtilsModule.createAlert(errors.content));
		}
		else{
			// error is array
			for (var field in errors.content){
			    if (errors.content.hasOwnProperty(field)) {
			    	$fgroup = $(form+"-input-"+field).closest(".form-group");
			    	this.addFieldError($fgroup);
			    	$fgroup.prepend(UtilsModule.createAlert(errors.content[field]));
			    }
			}
		}
	}

};

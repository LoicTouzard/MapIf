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

	cleanFormMessages : function($form){
		// remove the old errors
		$form.find(".alert").remove();
		this.removeFieldError($form.find(".has-warning"));
	},

	displayFieldFormErrors : function(form, errors){
	    var $form = $(form);
	    this.cleanFormMessages($form);
		if(typeof errors.content == "string"){
			// single message
			this.displayFormError(form, errors.content)
		}
		else{
			// error is array
			for (var field in errors.content){
			    if (errors.content.hasOwnProperty(field)) {
			    	$fgroup = $("[name='"+field+"']").closest(".form-group");
			    	this.addFieldError($fgroup);
			    	UtilsModule.createDangerAlert(errors.content[field])
			    		.hide()
			    		.prependTo($fgroup)
			    		.slideDown("slow");
			    }
			}
		}
	},

	displayModalFormErrors : function(formId, errors){
	    var $form = $(formId);
	    this.cleanFormMessages($form);
		if(typeof errors.content == "string"){
			// single message
			$form.find(".modal-body").prepend(UtilsModule.createDangerAlert(errors.content));
		}
		else{
			// error is array
			for (var field in errors.content){
			    if (errors.content.hasOwnProperty(field)) {
			    	$fgroup = $(formId+"-input-"+field).closest(".form-group");
			    	this.addFieldError($fgroup);
			    	UtilsModule.createDangerAlert(errors.content[field])
			    		.hide()
			    		.prependTo($fgroup)
			    		.slideDown("slow");
			    }
			}
		}
	},

	displayModalFormSuccess : function(formId, data){
	    var $form = $(formId);
	    this.cleanFormMessages($form);
		if(typeof data.content == "string"){
			$form.find(".modal-body").prepend(UtilsModule.createSuccessAlert(data.content));
		}
	},


	displayFormSucess : function(form, message){
	    var $form = $(form);
	    this.cleanFormMessages($form);
	    var $alert = UtilsModule.createSuccessAlert(message).hide();
	    $alert.prependTo($form).slideDown("slow");
	},

	displayFormError : function(form, message){
	    var $form = $(form);
	    this.cleanFormMessages($form);
		var $alert = UtilsModule.createDangerAlert(message).hide();
	    $alert.prependTo($form).slideDown("slow");
	}
};

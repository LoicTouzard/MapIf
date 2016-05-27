/* FormModule.js
*
* form functions
*
* Dependancies : 
* 	UtilsModule.js
*/
var FormModule = {
	p3_trolled : false,
	p3_open : false,
	$p3_block : undefined,
	$p3_msg : undefined,

	addFieldError : function($el){
		return $el.addClass("has-warning");
	},

	removeFieldError : function($el){
		return $el.removeClass("has-warning");
	},

	checkPasswords : function(){
		$p1 = $("#form-inscription-input-password1");
		p1 = $p1.val();
		$p2 = $("#form-inscription-input-password2");
		p2 = $p2.val();
		$p3 = $("#form-inscription-input-password3");
		p3 = $p3.val();
		if($p2.val() != ""){
			// check similarity with p1
			if(p1 != p2){
				this.addFieldError($p2.closest(".form-group"));
			}
			else{
				this.removeFieldError($p2.closest(".form-group"));
				if(!this.p3_open && !this.p3_trolled){
					//activate the troll not finished
					this.$p3_block.show(500);
					this.p3_open = true;
				}
			}
		}
		else{
			//this.addFieldError($p2.closest(".form-group"));
		}
		if(this.p3_open){
			if(p3 != ""){
				// check similarity with p1
				if(p1 != p3){
					this.addFieldError($p3.closest(".form-group"));
				}
				else{
					this.removeFieldError($p3.closest(".form-group"));
				}
			}
			else{
				// this.addFieldError($p3.closest(".form-group"));
			}
		}
		if(p1 != "" && p1 == p2 && p1 == p3){
			//validé !
			if(!this.p3_trolled){
				//activate the troll not finished
				this.$p3_block.hide(500);
				this.$p3_msg.show(500);
				this.p3_open = false;
				this.p3_trolled = true;
			}
		}
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

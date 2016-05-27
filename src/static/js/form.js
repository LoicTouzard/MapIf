/* form.js
*
* form functions
*
* Dependancies : 
* 	utils.js
*/


var p3_trolled = false;
var p3_open = false;
var $p3_block;
var $p3_msg;

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


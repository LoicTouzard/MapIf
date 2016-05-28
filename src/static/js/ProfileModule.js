/* ProfileModule.js
*
* function related to profil modal view
*
* Dependancies : 
* 	AjaxModule.js
*/
var ProfileModule = {
	init : function(){
		$("#delete-input").keyup(this.checkAcountDelete).val("");

		$("#delete-button-confirm").attr("disabled", "disabled");
	},

	checkAcountDelete : function(){
		// this is the input
		$input = $(this);
		$confirm = $("#delete-button-confirm");
		if($input.val() === "je sui 1 gro boloss"){
			$confirm.removeAttr("disabled");
			$confirm.bind("click", AjaxModule.deleteAccount);
		}
		else{
			$confirm.attr("disabled", "disabled");
			$confirm.unbind("click", AjaxModule.deleteAccount);
		}
	}
};
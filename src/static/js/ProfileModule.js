/* ProfileModule.js
*
* function related to profil modal view
*
* Dependancies : 
* 	AjaxModule.js
*/
var ProfileModule = {
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
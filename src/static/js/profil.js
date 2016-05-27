/* profil.js
*
* function related to profil modal view
*
* Dependancies : 
* 	ajax.js
*/

var checkAcountDelete = function(){
	$input = $(this);
	$confirm = $("#delete-button-confirm");
	if($input.val() === "je sui 1 gro boloss"){
		$confirm.removeAttr("disabled");
		$confirm.bind("click", ajaxDeleteAccount);
	}
	else{
		$confirm.attr("disabled", "disabled");
		$confirm.unbind("click", ajaxDeleteAccount);
	}
}
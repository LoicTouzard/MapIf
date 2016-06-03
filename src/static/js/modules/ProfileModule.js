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

		$("#panel-profile-edit .list-group-item-header").click(this.toggleItem);
	},

	checkAcountDelete : function(){
		// this is the input
		$input = $(this);
		$confirm = $("#delete-button-confirm");
		if($input.val() === "Je reviens tout de suite !"){
			$confirm.removeAttr("disabled");
			$confirm.bind("click", AjaxModule.deleteAccount);
		}
		else{
			$confirm.attr("disabled", "disabled");
			$confirm.unbind("click", AjaxModule.deleteAccount);
		}
	},

	toggleItem : function(e){
		e.preventDefault();
		// this, is the clicked icon
		var $this = $(this);
		var $item = $this.closest(".list-group-item");
		$item.find(".list-group-item-text").collapse("toggle");
		UtilsModule.toggleArrow($item.find(".least-content i"));
	}
};
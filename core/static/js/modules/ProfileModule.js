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

		var $select = $("#form-profile-input-promo");
		UtilsModule.generatePromotion($select).val($select.data("value"));

		$("#panel-profile-edit .list-group-item-header").click(this.toggleItem);

		$(".profile-form").on("submit", this.sendProfileField);
	},

	checkAcountDelete : function(){
		// this is the input
		var $input = $(this);
		var $confirm = $("#delete-button-confirm");
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
		// this, is the clicked icon
		var $this = $(this);
		var $item = $this.closest(".list-group-item");
		$item.find(".list-group-item-text").collapse("toggle");
		UtilsModule.toggleArrow($item.find(".least-content i"));
	},

	sendProfileField : function(e){
		e.preventDefault();
		AjaxModule.editProfile(this)
		return false
	}

};
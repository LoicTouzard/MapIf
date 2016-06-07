/* UtilsModule.js
*
* global utils function
*
* Dependancies : 
* 	SETTINGS
*/

var UtilsModule = {
	// create an alert element with given content
	createDangerAlert : function(msg){
		return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Oups !</strong> '+msg+'</div>');
	},

	createSuccessAlert : function(msg){
		return $('<div class="alert alert-dismissible alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Yaay !</strong> '+msg+'</div>');
	},

	logger : function(msg){
		if(SETTINGS.DEBUG){
			console.log(msg);
		}
	},

	handleServerError : function(code){
		createSnackbar(code);
	},

	onMobile : function(){
		return $(window).width() < 768;
	},

	menuIsExpanded : function(){
		// TODO, can we know it another way ? from plugin API ?
		return ($("#main-navbar").attr("aria-expanded") == "true")?true:false;
	},

	toTitleCase : function(str)
	{
	    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
	},

	toggleArrow : function(icon){
		$icon = $(icon);
		$icon.text($icon.text()=="keyboard_arrow_right"?"keyboard_arrow_down":"keyboard_arrow_right")
	},

	generatePromotion : function(select){
		var startYear = 1969;
		var lastYear = new Date().getFullYear()+4;
		var $select = $(select);
		for (var i = startYear; i < lastYear; i++) {
			var $option = $('<option value="'+i+'">'+i+'</option>');
			$select.append($option);
		};
		return $select;
	}
}
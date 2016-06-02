/* UtilsModule.js
*
* global utils function
*
* Dependancies : 
* 	SETTINGS
*/

var UtilsModule = {
	// create an alert element with given content
	createAlert : function(msg){
		return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Bah alors ?!</strong> '+msg+'</div>');
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
	}
}
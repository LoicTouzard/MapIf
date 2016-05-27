/* util.js
*
* global utils function
*
* Dependancies : 
* 	SETTINGS
*/

// create an alert element with given content
var createAlert = function(msg){
	return $('<div class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Bah alors ?!</strong> '+msg+'</div>');
}

var logger = function(msg){
	if(SETTINGS.DEBUG){
		console.log(msg);
	}
}

var handleServerError = function(code){
	createSnackbar(code);
}


var onMobile = function(){
	return $(window).width() < 768;
}


var menuIsExpanded = function(){
	return ($("#main-navbar").attr("aria-expanded") == "true")?true:false;
}
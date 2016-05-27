/* left-panel.js
*
* left-panel controls
*
* Dependancies : 
*
*/

var leftPanelOpen = function(){
	$("#left-panel").removeClass("closePanel");
	$("#left-panel .widget-pane-toggle-button-container .btn").focusout().blur()
		.attr('data-original-title', "Réduire le panneau latéral")
		.find(".glyphicon").removeClass("glyphicon-triangle-right")
		.addClass("glyphicon-triangle-left");

	$("#menu-map").removeClass("active");
	$("#menu-search").addClass("active");
}

var leftPanelClose = function(){
	$("#left-panel").addClass("closePanel");
	$("#left-panel .widget-pane-toggle-button-container .btn").focusout().blur()
		.attr('data-original-title', "Étendre le panneau latéral")
		.find(".glyphicon").removeClass("glyphicon-triangle-left")
		.addClass("glyphicon-triangle-right");

	$("#menu-search").removeClass("active");
	$("#menu-map").addClass("active");
}

var leftPanelIsOpen = function(){
	return !$("#left-panel").hasClass("closePanel");
}

var leftPanelToggle = function(){
	if(leftPanelIsOpen()){
		leftPanelClose();
	}
	else{
		leftPanelOpen();
	}
}

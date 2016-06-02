/******* JQUERY ON LOAD - BINDS *******/

$(document).on("settings-loaded",function(){
	console.log("Welcome to MapIF V"+SETTINGS.VERSION+" !")
	// Material Init
	$.material.init();

	$(".version").text(SETTINGS.VERSION);

	$("body").tooltip({ selector: '[data-toggle=tooltip]' });

	var versionArray = SETTINGS.VERSION.split(".");
	versionArray.pop();
	var cookieName = versionArray.join("-");
	// show about if it is the first visit
	if(!Cookies.get(cookieName)){
		Cookies.set(cookieName, cookieName, { expires: 365 });
		$("#aboutModal").modal("show");
	}

	// generate the promotions year
	(function(){
		var startYear = 1969;
		var currentYear = new Date().getFullYear();
		var lastYear = currentYear+4;
		var $select = $("#form-inscription-input-promo");
		for (var i = startYear; i < lastYear; i++) {
			var $option = $('<option value="'+i+'">'+i+'</option>');
			if(i == currentYear){
				$option.attr("selected", "selected");
			}
			$select.append($option);
		};
	})()




	/********* MAP *********/
	
	MapModule.init();

	MapModule.loadLocations(locations);


	/********* FORM VALIDATION *********/

	FormModule.init();


	/********* LEFT PANEL *********/

	LeftPanelModule.init();
	

	/********* SEARCH *********/

	PlaceSearchModule.init();


	/********* PROFILE *********/

	ProfileModule.init();


	/********* AJAX *********/
	
	AjaxModule.init();


	/********* MENU *********/

	// bindings
	$(".navbar-left-item").click(function(e){
		e.preventDefault();
		if(UtilsModule.onMobile() && UtilsModule.menuIsExpanded()){
			$("#main-navbar").collapse("hide");
		}
	})

	$("#menu-search, #menu-map").click(function(e){
		e.preventDefault();
		$(".navbar-left-item").removeClass("active");
		$(this).addClass("active");
	});

	$('#aboutModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-about").addClass("active");
	});

	$('#profilModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-profil").addClass("active");
	})

	$('#aboutModal, #profilModal').on('hide.bs.modal', function(e){
	    $(".navbar-left-item").removeClass("active");
	    if(LeftPanelModule.isOpen()){
	    	$("#menu-search").addClass("active");
	    }
	    else{
	    	$("#menu-map").addClass("active");
	    }
	});
});
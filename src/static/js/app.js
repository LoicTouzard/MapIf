/******* JQUERY ON LOAD - BINDS *******/

$(document).one("settings-loaded",function(){
	
	/********* INITIALIZATIONS *********/

	console.log("Welcome to MapIF V"+SETTINGS.VERSION+" !")

	$.material.init();

	$("body").tooltip({ selector: '[data-toggle=tooltip]' });
	

	/********* VERSION *********/

	$(".version").text(SETTINGS.VERSION);

	var versionArray = SETTINGS.VERSION.split(".");
	versionArray.pop();
	var cookieName = versionArray.join("-");
	// show about if it is the first visit
	if(!Cookies.get(cookieName)){
		Cookies.set(cookieName, cookieName, { expires: 365 });
		$("#aboutModal").modal("show");
	}



	/********* SIGNINUP *********/

	if(!connected){
		SignInUpModule.init();
	}


	/********* MENU *********/

	// bindings
	$(".navbar-left-item").click(function(e){
		if(UtilsModule.onMobile() && UtilsModule.menuIsExpanded()){
			$("#main-navbar").collapse("hide");
		}
	})

	$("#menu-search, #menu-map").click(function(e){
		$(".navbar-left-item").removeClass("active");
		$(this).addClass("active");
	});

	$('#aboutModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-about").addClass("active");
	});
/* there is no more profilModal
	$('#profilModal').on('show.bs.modal', function() {
	    $(".navbar-left-item").removeClass("active");
	    $("#menu-profil").addClass("active");
	})
*/
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

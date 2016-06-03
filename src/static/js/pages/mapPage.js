$(document).one("settings-loaded",function(){
	/********* MAP *********/
	
	MapModule.init();

	MapModule.loadLocations(locations);


	/********* LEFT PANEL *********/

	LeftPanelModule.init();
	

	/********* SEARCH *********/

	PlaceSearchModule.init();


	/********* PROFILE *********/

	ProfileModule.init();
})
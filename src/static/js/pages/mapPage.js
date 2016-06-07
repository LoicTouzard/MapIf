$(document).one("settings-loaded",function(){
	/********* MAP *********/

	MapModule.init();

	var promos = [];
	locations.forEach(function(val1, key1, arr1){
		val1.users.forEach(function(user, key2, arr2){
			if(promos.indexOf(user.promo) === -1){
				promos.push(user.promo);
			}
		});
	});

	promos.sort().forEach(function(year){
		MapModule.addPromoOverlayToControl(year);
	});

	MapModule.loadLocations(locations);


	/********* LEFT PANEL *********/

	LeftPanelModule.init();
	

	/********* SEARCH *********/

	PlaceSearchModule.init();


	/********* PROFILE *********/

	ProfileModule.init();
})
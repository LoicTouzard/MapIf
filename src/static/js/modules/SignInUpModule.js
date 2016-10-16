/* FormModule.js
*
* form functions
*
* Dependancies : 
* 	FormModule.js
* 	AjaxModule.js
*/
var SignInUpModule = {
	p3_trolled : false,
	p3_open : false,
	$p3_block : undefined,
	$p3_msg : undefined,

	init : function(){
		this.$p3_block = $("#p3-block").hide();
		this.$p3_msg = $("#p3-msg").hide();
		var _module = this;
		$("#form-inscription-input-password1, #form-inscription-input-password2, #form-inscription-input-password3").keyup(function(){
			_module.checkPasswords();
		});

		// generate the promotions year
		UtilsModule.generatePromotion("#form-inscription-input-promo").val(2016);

        $('#form-connexion').on('submit', AjaxModule.login);

        $('#form-inscription').on('submit', AjaxModule.signup);  

        $('#form-password-forgotten').on('submit', AjaxModule.password_forgotten);
	},

	checkPasswords : function(){
		$p1 = $("#form-inscription-input-password1");
		p1 = $p1.val();
		$p2 = $("#form-inscription-input-password2");
		p2 = $p2.val();
		$p3 = $("#form-inscription-input-password3");
		p3 = $p3.val();
		if($p2.val() != ""){
			// check similarity with p1
			if(p1 != p2){
				FormModule.addFieldError($p2.closest(".form-group"));
			}
			else{
				FormModule.removeFieldError($p2.closest(".form-group"));
				if(!this.p3_open && !this.p3_trolled){
					//activate the troll not finished
					this.$p3_block.show(500);
					this.p3_open = true;
				}
			}
		}
		else{
			//FormModule.addFieldError($p2.closest(".form-group"));
		}
		if(this.p3_open){
			if(p3 != ""){
				// check similarity with p1
				if(p1 != p3){
					FormModule.addFieldError($p3.closest(".form-group"));
				}
				else{
					FormModule.removeFieldError($p3.closest(".form-group"));
				}
			}
			else{
				// FormModule.addFieldError($p3.closest(".form-group"));
			}
		}
		if(p1 != "" && p1 == p2 && p1 == p3){
			//validé !
			if(!this.p3_trolled){
				//activate the troll not finished
				this.$p3_block.hide(500);
				this.$p3_msg.show(500);
				this.p3_open = false;
				this.p3_trolled = true;
			}
		}
	},
};

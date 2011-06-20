$(document).ready(function(){
	
	function handle_account_overview_link_click(){
		console.log("account_overview");
	};
	function handle_subscription_and_billing_link_click(){
		console.log("subscription_and_billing");
	};
	function handle_preferences_link_click(){
		console.log("preferences");
	};
	
	$("#subscription_and_billing_link").click(handle_subscription_and_billing_link_click);
	$("#preferences_link").click(handle_preferences_link_click);
	$("#account_overview_link").click(handle_account_overview_link_click);
});
/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {
	$('#email_icon_section').Fisheye(
	{
		maxWidth: 30,
		items: 'a',
		itemsText: 'span',
		container: '.dock_container',
		itemWidth: 40,
		proximity: 80,
		halign: 'center',
		valign: 'bottom'
	})
});

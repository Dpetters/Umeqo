/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	$("#tabs").tabs({
		"show": function(event, ui) {
			var oTable = $('div.dataTables_wrapper>table.display', ui.panel).dataTable();
			if ( oTable.length > 0 ) {
				oTable.fnAdjustColumnSizing();
			}
		}
	});

	$("table.display").dataTable({
		"sDom": '<"menu_bar"fp>t',
		"sPaginationType": "full_numbers"
	});
} );
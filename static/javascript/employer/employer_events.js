/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
 */

$(document).ready( function() {

	// Event Description Collapse and Toggle
	$("#old_event_list").hide();
	$("#view_old_events_link").click( function() {
		var visible = ($("#old_event_list").is(':visible'));
		$("#old_event_list").slideToggle();
		$("#view_old_events_link").text(
		visible ? "View Older Events" : "Hide Older Events"
		);
	});
	$(".event_description").hide();
	$(".view_description_link").click( function() {
		$('#description_'+ this.id).slideToggle('slow');
	});
	var create_new_event_dialog = function () {
		var $dialog = $('<div></div>')
		.dialog({
			autoOpen: false,
			title: "New Event",
			dialogClass: "new_event_form_dialog",
			modal: true,
			width: "700px",
			beforeClose: function(event, ui) {
				$("#id_audience").multiselect("destroy");
			}
		});
		$dialog.dialog('open');
		return $dialog;
	};
	var event_rules = {
		name:{
			required: true,
		},
		datetime:{
			required: true,
		},
		duration:{
			required:true,
			min: 0,
		},
		type:{
			required:true,
		},
		location:{
			required:true,
		}
	};

	var deadline_rules = {
		name:{
			required: true,
		},
		datetime:{
			required: true,
		},
		type:{
			required:true,
		},
	};

	function addRules(rulesObj) {
		for (item in rulesObj) {
			$('#id_'+item).rules('add',rulesObj[item]);
		}
	}

	function removeRules(rulesObj) {
		for (item in rulesObj) {
			$('#id_'+item).rules('remove');
		}
	}

	var format = function() {
		var widths = [];
		$('label').each( function(idx, label) {
			widths.push(label.offsetWidth);
		});
		$('label').each( function(idx, label) {

			var diff = Array.max(widths) - this.offsetWidth;
			label.style.paddingLeft = diff + "px";
		});
	};
	$("#new_event_link").click( function () {
		var $new_event_dialog = create_new_event_dialog();
		$new_event_dialog.html(ajax_loader);

		$new_event_dialog.load( '/new_event', function () {

			$new_event_dialog.dialog('option', 'position', 'center');

			required_label_format();
			format();
			$("label[for=id_description]").css('padding-left', '0px');

			$("#id_audience").multiselect({
				noneSelectedText: '---------',
				minWidth: "202px"
			});

			$('#id_datetime').AnyTime_picker();

			$("select[id='id_type']").change( function() {
				if ($("select[id='id_type']").val() === "Deadline") {
					$('.event_only_field').hide();
					removeRules(event_rules);
					addRules(deadline_rules);
				} else {
					$('.event_only_field').show();
					removeRules(deadline_rules);
					addRules(event_rules);

				}
			});
			$("#new_event_form").validate({
				submitHandler: function (form) {
					$(form).ajaxSubmit({
						dataType: 'json',
						beforeSubmit: function (arr, $form, options) {
							showDialogFormSubmitLoader();
						},
						success: function (data) {
							hideDialogFormSubmitLoader();
							$("#id_audience").multiselect("destroy");
							if (data.valid === true) {
								var success_message = "<div id='dialog_wrapper' class='centered'><p>Your event has been created.</p><br><a id='close_new_event_dialog_link' href='javascript:void(0)'>Refresh Event List</a></div>";
								$new_event_dialog.html(success_message);
								$new_event_dialog.dialog('option', 'position', 'center');
							}

							$("#close_new_event_dialog_link").click( function () {
								location.replace('/employer/events/');
							});
						}
					});
				},
				highlight: function (element, errorClass) {
					$(element).css('border', '1px solid red');
				},
				unhighlight: function (element, errorClass) {
					$(element).css('border', '1px solid #808080');
				},
				errorPlacement: function(error, element) {
					$(error).appendTo(element.parent().prev());
					var offset = element.position().left-element.parent().parent().position().left;
					$(error).css("padding-left", offset).css("float", "left").css('position', 'absolute').css('bottom','0');
				}
			});
			addRules(event_rules);

		})
	});
	$(".delete_event").click( function() {
		url = '/delete_event';

		data = {
			event_id: this.id
		};

		$.post(url, data, function(response) {
			if (response != false) {
				$("#event_"+ response).remove();
			} else {
			}
		}
		), "json"
	});
	var action = window.location.pathname.split("/")[3];
	if (action == "new") {
		$("#new_event_link").click();
	}

});
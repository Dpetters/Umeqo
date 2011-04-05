/*
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
*/

$(document).ready( function() {

	var openEmployerSubscriptionsDialog = function () {
		var $dialog = $('<div></div>')
		.dialog({
			autoOpen: false,
			title: "Setup Employer Subscriptions",
			dialogClass: "employer_subscriptions_dialog",
			modal: true,
			resizable: false,
			width: 476
		});
		$dialog.dialog('open');
		return $dialog;
	};
	var get_suggested_employers_list = function() {
		var array_of_checkboxes = $("select").multiselect("getChecked");
		var already_selected_employers = [array_of_checkboxes.length];
		for (i=0; i<array_of_checkboxes.length; i++) {
			already_selected_employers[i] = $(array_of_checkboxes[i]).parent().text();
		}
		$.ajax({
        	beforeSend: function(xhr) {
        		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))
    		},
        	type: 'POST',
        	url: '/student/get-suggested-employers-list/',
        	data:{'already_selected':already_selected_employers },
        	dataType: "html",
        	success: function(data){
        		$("#suggested_employers_list").html(data);
        		$("#suggested_employers_list li").click( function() {
					$("select").multiselect("widget").find(":checkbox[title=" + $(this).text() + "]").trigger("click");
				});
        	}
		});
	};
	$('#setup_employer_subscriptions_link').click( function () {
		var $employerSubscriptionsDialog = openEmployerSubscriptionsDialog();

		$employerSubscriptionsDialog.html(ajax_loader);
		$employerSubscriptionsDialog.load('/student/employer-subscriptions-dialog/', function () {
			
			$("#get_more_employer_suggestions_link").live('click', function() {
				get_suggested_employers_list();
			});
			get_suggested_employers_list();

			format_required_labels();

			$("#id_subscribed_employers").multiselect({
				noneSelectedText: 'select employers',
				checkAllText: "All",
				uncheckAllText: "None",
				height:140,
				click: function(e, ui) {
					$("#suggested_employers_list li").each( function(i, e) {
						if ($(e).text() == ui.text) {

							if ($(e).children().size() == 0) {
								$(e).css("background-color", "#A1E285");
								$(e).append("<img src='/static/images/icons/check.gif'>");
							} else {
								$(this).css("background-color", "#d9d9d9");
								$(this).children().remove();
							}
							/*
 							if (!$(ui).attr("checked")) {
 							$(e).css("background-color", "#A1E285");
 							$(e).append("<img class='fright icon' src='/static/images/icons/check.gif'>");
 							}
 							else {
 							$(this).css("background-color", "#d9d9d9");
 							$(this).children().remove();
 							}
 							*/
							/*
 							if (ui.checked && $(e).children().size() == 0 || !ui.checked && $(e).children().size() == 1) {
 							$(e).trigger("click");
 							}
 							*/
							return;
						}
					});
				}
			}).multiselectfilter();

			$employerSubscriptionsDialog.dialog('option', 'position', 'center');

			$("#employer_subscriptions_form").validate({
				submitHandler: function (form) {
					$(form).ajaxSubmit({
						dataType: 'json',
						beforeSubmit: function (arr, $form, options) {
							$("#ajax_form_submit_loader").css("display", "");
						},
						success: function (data) {
							$employerSubscriptionsDialog.dialog('destroy');
							location.reload(true);
						}
					});
				},
				highlight: highlight,
				unhighlight: unhighlight,
				errorPlacement: place_errors,
				rules: {
					subscribed_employers: {
						required: true
					},
				}
			});
		});
	});
	/* The rest is the drag and drop */

	var temp = new XMLHttpRequest();
	if(temp.sendAsBinary == null) {
		$('#drop-area').html("Switch to Firefox 3.6 or above to use the quick resume updater.")
	} else {
		var up = {

			$drop :			null,
			queue :			[],
			processing :	null,
			uploading :		false,
			binaryReader :	null,
			dataReader :	null,
			xhr:			null,

			init : function() {
				up.$drop = $('#drop-area');

				up.$drop.bind('dragenter',up.enter);
				up.$drop.bind('dragleave',up.leave);
				up.$drop.bind('dragover',up.over);
				up.$drop.bind('drop',up.drop);

				up.xhr = new XMLHttpRequest();
				up.xhr.upload.addEventListener('progress', up.uploadProgress , false);
				up.xhr.upload.addEventListener('load', up.uploadLoaded , false);

			},
			enter : function(e) {
				$(e.target).addClass('hover').removeClass('success').removeClass('error').html('Drop PDF File Here');
				return false;
			},
			leave : function(e) {
				$(e.target).removeClass('hover');
				return false;
			},
			over : function(e) {
				return false;
			},
			drop : function(e) {
				$(e.target).removeClass('hover').addClass('uploading');

				var files = e.originalEvent.dataTransfer.files;
				if (files.length > 1) {
					$(e.target).addClass('error').html('Only one file allowed.<br\>Please try again.');
				} else if(files[0].type != "application/pdf") {
					$(e.target).addClass('error').html('Only .pdf files are allowed.<br\>Please try again.');
				} else {
					for (var i = 0; i<files.length; i++) {
						var file = files[i];
						up.queue.push(file);
					}

					if(up.uploading == false) {
						up.uploading = true;
						up.process();
					}
				}
				return false;
			},
			process : function() {
				up.processing = up.queue.shift();
				if(window.FileReader) { //firefox 3.6, Chrome 6, Webkit
					up.binaryReader = new FileReader();
					if(up.binaryReader.addEventListener) { //firefox
						up.binaryReader.addEventListener('loadend', up.binaryLoad, false);
						up.binaryReader.addEventListener('error', up.loadError, false);
						up.binaryReader.addEventListener('progress', up.loadProgress, false);
					} else { //chrome / webkit
						up.binaryReader.onloadend = up.binaryLoad;
						up.binaryReader.onerror = up.loadError;
						up.binaryReader.onprogress = up.loadProgress;
					}
					try {
						up.binaryReader.readAsBinaryString(up.processing);
					} catch(error) {
						up.uploading=false;
						$("#drop-area").removeClass('uploading').addClass('error').html('The file could not be read.<br\>Please try again.');
					}

				} else { // safari 5 + others?

					up.xhr.abort(); //make sure xhr is a new request
					up.xhr.open('POST', '/html5_upload.php?up=true', true);

					up.xhr.setRequestHeader('UP-FILENAME', up.processing.name);
					up.xhr.setRequestHeader('UP-SIZE', up.processing.size);
					up.xhr.setRequestHeader('UP-TYPE', up.processing.type);

					up.xhr.send(up.processing);
					up.xhr.onload = up.onload;
				}

			},
			loadError : function(e) {
				switch(e.target.error.code) {
					case e.target.error.NOT_FOUND_ERR:
						$("#drop-area").removeClass('uploading').addClass('error').html('File Not Found.<br\>Please try again.');
						break;
					case e.target.error.NOT_READABLE_ERR:
						$("#drop-area").removeClass('uploading').addClass('error').html('File is not readable.<br\>Please try again.');
						break;
					case e.target.error.ABORT_ERR:
						break;
					default:
						$("#drop-area").removeClass('uploading').addClass('error').html('The file could not be read.<br\>Please try again.');
				};

			},
			loadProgress : function(e) {
				if (e.lengthComputable) {
					var percentage = Math.round((e.loaded * 100) / e.total);
					$('#drop-area').html('loaded: '+percentage+'%');
				}
			},
			binaryLoad : function(e) {

				up.xhr.abort(); //make sure xhr is a new request

				var binary = e.target.result;

				if(up.xhr.sendAsBinary != null) { //firefox
					up.xhr.open('POST', '/resume_update?up=true', true);

					var boundary = 'xxxxxxxxx';

					var body = '--' + boundary + "\r\n";
					body += "Content-Disposition: form-data; name=resume; filename=" + up.processing.name + "\r\n";
					body += "Content-Type: application/pdf\r\n\r\n";
					body += binary + "\r\n";
					body += '--' + boundary + '--';

					up.xhr.setRequestHeader('content-type', 'multipart/form-data; boundary=' + boundary);
					up.xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
					up.xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
					up.xhr.sendAsBinary(body);

				} else { //for browsers that don't support sendAsBinary yet

					up.xhr.open('POST', '/resume_update?up=true&base64=true', true);

					up.xhr.setRequestHeader('UP-FILENAME', up.processing.name);
					up.xhr.setRequestHeader('UP-SIZE', up.processing.size);
					up.xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
					up.xhr.setRequestHeader('UP-TYPE', up.processing.type);

					up.xhr.send(window.btoa(binary));
				}

				up.xhr.onload = up.onload;

			},
			uploadProgress : function(e) {
				if (e.lengthComputable) {
					var percentage = Math.round((e.loaded * 100) / e.total);
					$('#drop-area').html('uploaded: '+percentage+'%');
				}
			},
			uploadLoaded : function(e) {
				$('#drop-area').html('Uploaded: 100%');
			},
			onload : function (e) {
				up.uploading = false;
				currentRequest = $.getJSON("/resume_info/", function(data) {
					$('#drop-area').html('<p>Resume Updated</p><p>'+ data["num_of_extracted_keywords"]+ ' keywords extracted.').removeClass('uploading').addClass('success');
					$("#view_resume_link").attr("href", "/static/" + data["path_to_new_resume"]);
				});
			},
			cancel : function(e) {
				if(up.dataReader) {
					up.dataReader.abort();
				}
				if(up.dataReader) {
					up.binaryReader.abort();
				}
				if(up.xhr) {
					up.xhr.abort();
				}
				up.uploading = false;
				up.queue = [];
				up.processing = null;
				$('#drop-area').html('Drag and Drop files to begin...');
				return false;
			}
		}

		$(up.init);
	}
});
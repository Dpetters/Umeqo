if (typeof (XMLHttpRequest.prototype.sendAsBinary) === "undefined") {
    XMLHttpRequest.prototype.sendAsBinary = function (datastr) {
        function byteValue(x) {
            return x.charCodeAt(0) & 0xff;
        }
        var ords = Array.prototype.map.call(datastr, byteValue),
        ui8a = new Uint8Array(ords);
        this.send(ui8a.buffer);
    };
}

$(document).ready( function() {
    $("#update_resume_link").click( function() {
        $("#update_resume_div").slideToggle();
    });

    if (typeof (FileReader) === "undefined" || typeof (XMLHttpRequest) === "undefined" || !('draggable' in document.createElement('span'))) {
        $('#dropbox_status').html("Browser Not Supported");
    } else {
        var up = {
            $dropbox :        null,
            processing :    null,
            uploading :        false,
            binaryReader :    null,
            dataReader :    null,
            xhr:            null,
            
            noop : function (e){
                e.stopPropagation();
                e.preventDefault();
            },
            init : function () {
                up.$dropbox = $("#dropbox");
                up.$dropbox.bind("dragenter", up.dragenter);
                up.$dropbox.bind("dragleave", up.dragleave);
                up.$dropbox.bind("dragover", up.dragover);
                up.$dropbox.bind("drop", up.drop);
                
                up.$status = $("#dropbox_status");
                
                up.xhr = new XMLHttpRequest();
                up.xhr.upload.addEventListener('progress', up.uploadProgress , false);
                up.xhr.upload.addEventListener('load', up.uploadLoaded , false);
            },
            dragover : function (e) {
                console.log("dragover");
                up.noop(e);
            },
            dragenter : function (e) {
                console.log("dragenter");
                up.noop(e);
                up.$dropbox.removeClass('success').removeClass('error').addClass('hover');
                up.$status.html("Drag & Drop PDF File Here");
                return false;
            },
            dragleave : function (e) {
            	console.log("dragleave");
                up.noop(e);
                up.$dropbox.removeClass('hover');
                return false;
            },
            drop : function (e) {
            	console.log("dropped!")
                up.noop(e);
                up.$dropbox.removeClass('hover').addClass('uploading');

                var files = e.originalEvent.dataTransfer.files;
                if (files.length > 1) {
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.$status.html('Only one file allowed.');
                } else if(files[0].type != "application/pdf") {
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.$status.html('Only PDFs are allowed.');
                } else {
                    if(up.uploading == false) {
                        up.processing = files[0];
                        up.uploading = true;
                        up.process();
                    }
                }
                return false;
            },
            process : function() {
                up.binaryReader = new FileReader();
                up.binaryReader.onloadend = up.binaryLoad;
                up.binaryReader.onerror = up.loadError;
                up.binaryReader.onprogress = up.loadProgress;
                
                try {
                    up.binaryReader.readAsBinaryString(up.processing);
                } catch(error) {
                    up.uploading = false;
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.$status.html('The file could not be read.');
                }
            },
            loadError : function(e) {
                switch(e.target.error.code) {
                    case e.target.error.NOT_FOUND_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('File Not Found.');
                        break;
                    case e.target.error.NOT_READABLE_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('File is not readable.');
                        break;
                    case e.target.error.ABORT_ERR:
                        break;
                    default:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('The file could not be read.');
                        break;
                };
            },
            loadProgress : function(e) {
                if (e.lengthComputable) {
                    var percentage = Math.round((e.loaded * 100) / e.total);
                    up.$status.html('Loaded: ' + percentage + '%');
                }
            },
            binaryLoad : function(e) {
                up.xhr.abort();
                
                var binary = e.target.result;

                up.xhr.open('POST', '/student/update-resume/', true);
                
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
                
                up.xhr.onreadystatechange = function (aEvt){
                    if (up.xhr.readyState==4){
                        if(up.xhr.status != 200){
                            up.$dropbox.removeClass('uploading').addClass('error');
                            up.$status.html('Error. Please try again.');
                        }
                    }
                };
                up.xhr.onload = up.onload;
            },
            uploadProgress : function(e) {
                if (e.lengthComputable) {
                    var percentage = Math.round((e.loaded * 100) / e.total);
                    up.$status.html('Uploading: ' + percentage + '%');
                }
            },
            uploadLoaded : function(e) {
                $('#drop-area').html('Uploaded: 100%');
            },
            onload : function (e) {
                data = $.parseJSON(e.currentTarget.responseText);
                up.uploading = false;
                if(data.valid) {
                    currentRequest = $.getJSON("/student/update-resume/info/", function(data) {
                        up.$dropbox.removeClass('uploading').addClass('success');
                        up.$status.html(data["num_of_extracted_keywords"]+ ' keywords extracted.');
                    });
                } else {
                      if(data.unparsable_resume){
                        up.$status.html('0 keywords extracted.');
                        var $unparsable_resume_dialog = open_unparsable_resume_dialog();
                        $unparsable_resume_dialog.html(DIALOG_AJAX_LOADER);
                        var unparsable_resume_dialog_timeout = setTimeout(show_long_load_message_in_dialog, LOAD_WAIT_TIME);
                        $.ajax({
                            dataType: "html",
                            url: UNPARSABLE_RESUME_URL + "?home=true",
                            complete: function(jqXHR, textStatus) {
                                clearTimeout(unparsable_resume_dialog_timeout);
                                $unparsable_resume_dialog.dialog('option', 'position', 'center');
                            },
                            success: function (data) {
                                $unparsable_resume_dialog.html(data);
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                if(jqXHR.status==0){
                                    $unparsable_resume_dialog.html(CHECK_CONNECTION_MESSAGE_DIALOG);
                                }else{
                                    $unparsable_resume_dialog.html(ERROR_MESSAGE_DIALOG);
                                }
                            }
                        });
                    } else{
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('Error. Please try again.');
                    }
                }
            }
        };
        $(up.init);
    };
});
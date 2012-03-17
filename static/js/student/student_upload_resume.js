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
        $("#line_one").html("Your browser")
        $('#line_two').html("does not support");
        $("#line_three").html("Drap & Drop");
    } else {
        var up = {
            $dropbox :      null,
            processing :    null,
            uploading :     false,
            binaryReader :  null,
            dataReader :    null,
            xhr:            null,
            maxSize:        MAX_RESUME_SIZE,
            errors: {'too_many_files': ['', 'Only one file allowed', ''],
                     'default': ['', "Drag & Drop PDF File Here", ''],
                     'invalid_type': ['', "Only PDFs are allowed", ""],
                     'not_readable': ['', "File is not readable", ''],
                     'not_found': ['', "File was not found", ''],
                     'unparsable': ['', '0 keywords extracted', ''],
                     'uploading': ['', "Loading file...", ''],
            },
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
                
                up.$message_lines = [$("#line_one"), $("#line_two"), $("#line_three")]
                                
                up.xhr = new XMLHttpRequest();
                up.xhr.upload.addEventListener('progress', up.uploadProgress , false);
            },
            setMessage : function(message_type){
                if(message_type=="custom"){
                    // The last three arguments are lines #1, #2 & #3
                    var args = Array.prototype.slice.call(arguments);
                    for(i=0; i < 3; i++){
                        up.$message_lines[i].html(args[i+1]);
                    }                    
                } else{  
                    // Iterate over the three lines of the error message
                    // and put them in each of the three error lines
                    for(i=0; i < 3; i++){
                        up.$message_lines[i].html(up.errors[message_type][i]);
                    }
                }
            },
            dragover : function (e) {
                up.noop(e);
            },
            dragenter : function (e) {
                up.noop(e);
                up.$dropbox.removeClass('success').removeClass('error').addClass('hover');
                up.setMessage("default");
                return false;
            },
            dragleave : function (e) {
                up.noop(e);
                up.$dropbox.removeClass('hover');
                return false;
            },
            drop : function (e) {
                up.noop(e);
                up.$dropbox.removeClass('hover').addClass('uploading');
                var files = e.originalEvent.dataTransfer.files;
                // Check that nothing else is being uploaded
                if(up.uploading == false) {
                    // Check that there is only one file
                    // This check is only done here since we almost immediately
                    // just pick off the first one below using files[0]
                    if (files.length > 1) {
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.setMessage('too_many_files', 123, 23);
                    } else{
                        // Check that the file is a pdf
                        if(files[0].type != "application/pdf") {
                            up.$dropbox.removeClass('uploading').addClass('error');
                            up.setMessage("invalid_type");
                        }else{
                            // Check file size
                            if(files[0].size > MAX_RESUME_SIZE){
                                up.$dropbox.removeClass('uploading').addClass('error');
                                up.setMessage("custom", "", "File exceeds the " + MAX_RESUME_SIZE/1024/1024 + "MB limit");
                            } else {
                                up.processing = files[0];
                                up.uploading = true;
                                up.process();
                            }
                        }
                    }
                }
                return false;
            },
            process : function() {
                up.binaryReader = new FileReader();
                up.binaryReader.onloadend = up.binaryLoad;
                up.binaryReader.onerror = up.loadError;
                up.binaryReader.readAsBinaryString(up.processing);
                up.setMessage("uploading");
            },
            loadError : function(e) {
                switch(e.target.error.code) {
                    case e.target.error.NOT_FOUND_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.setMessage("not_found");
                        break;
                    case e.target.error.NOT_READABLE_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.setMessage("not_readable");
                        break;
                    case e.target.error.ABORT_ERR:
                        break;
                    default:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.setMessage("not_readable");
                        break;
                };
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
                up.xhr.onload = up.onload;
            },
            uploadProgress : function(e) {
                if (e.lengthComputable) {
                    var percentage = Math.round((e.loaded * 100) / e.total);
                    up.setMessage("custom", "", 'Uploading: ' + percentage + '%', "");
                }
            },
            onload : function (e) {
                data = $.parseJSON(e.currentTarget.responseText);
                up.uploading = false;
                if(data.errors){
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.setMessage(data.errors.resume);
                } else {
                    if(data.unparsable_resume){
                        up.setMessage("unparsable");
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
                    }
                    up.$dropbox.removeClass('uploading').addClass('success');
                    up.setMessage("custom", "", data["num_of_extracted_keywords"]+ ' keywords extracted.', "");
                }
            }
        };
        $(up.init);
    };
});
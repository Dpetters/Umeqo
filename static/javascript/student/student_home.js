if (typeof(XMLHttpRequest.prototype.sendAsBinary) == "undefined")
{
    XMLHttpRequest.prototype.sendAsBinary = function(datastr) {
        function byteValue(x) {
            return x.charCodeAt(0) & 0xff;
        }
        var ords = Array.prototype.map.call(datastr, byteValue);
        var ui8a = new Uint8Array(ords);
        this.send(ui8a.buffer);
    };
    }

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
    $('#setup_employer_subscriptions_link').click( function () {
        var $employerSubscriptionsDialog = openEmployerSubscriptionsDialog();

        $employerSubscriptionsDialog.html(dialog_ajax_loader);
        $employerSubscriptionsDialog.load('/student/employer-subscriptions-dialog/', function () {
            $employerSubscriptionsDialog.dialog('option', 'position', 'center');

        });
    });

    if(typeof(FileReader) == "undefined" || typeof(XMLHttpRequest) == "undefined" || !('draggable' in document.createElement('span'))) {
        $('#dropbox_status').html("Switch to latest version of Firefox or Chrome to use the quick resume updater.")
    } else {
        var up = {
            $dropbox :        null,
            processing :    null,
            uploading :        false,
            binaryReader :    null,
            dataReader :    null,
            xhr:            null,
            
            noop : function(e){
                e.stopPropagation();
                e.preventDefault();
            },
            init : function() {
                up.$dropbox = $("#dropbox");
                up.$dropbox.bind("dragenter", up.dragenter);
                up.$dropbox.bind("dragleave", up.dragleave);
                up.$dropbox.bind("dragover", up.dragover);
                up.$dropbox.bind("drop", up.drop, false);
                
                up.$status = $("#dropbox_status");
                
                up.xhr = new XMLHttpRequest();
                up.xhr.upload.addEventListener('progress', up.uploadProgress , false);
                up.xhr.upload.addEventListener('load', up.uploadLoaded , false);
            },
            dragover : function(e) {
                up.noop(e);
            },
            dragenter : function(e) {
                up.noop(e);
                up.$dropbox.removeClass('success').removeClass('error').addClass('hover');
                up.$status.html("Drop PDF File Here");
                return false;
            },
            dragleave : function(e) {
                up.noop(e);
                up.$dropbox.removeClass('hover');
                return false;
            },
            drop : function(e) {
                up.noop(e);
                up.$dropbox.removeClass('hover').addClass('uploading');

                var files = e.originalEvent.dataTransfer.files;
                if (files.length > 1) {
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.$status.html('Only one file allowed.<br\>Please try again.');
                } else if(files[0].type != "application/pdf") {
                    up.$dropbox.removeClass('uploading').addClass('error');
                    up.$status.html('Only PDF files are allowed.<br\>Please try again.');
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
                    up.$dropbox.removeClass('uploading').addClass('error')
                    up.$status.html('The file could not be read.<br\>Please try again.');
                }
            },
            loadError : function(e) {
                switch(e.target.error.code) {
                    case e.target.error.NOT_FOUND_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('File Not Found.<br\>Please try again.');
                        break;
                    case e.target.error.NOT_READABLE_ERR:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('File is not readable.<br\>Please try again.');
                        break;
                    case e.target.error.ABORT_ERR:
                        break;
                    default:
                        up.$dropbox.removeClass('uploading').addClass('error');
                        up.$status.html('The file could not be read.<br\>Please try again.');
                        break;
                };
            },
            loadProgress : function(e) {
                if (e.lengthComputable) {
                    var percentage = Math.round((e.loaded * 100) / e.total);
                    up.$status.html('Loaded: '+percentage+'%');
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
                            up.$status.html('Oops, something went wrong!<br\> We\'ve been notified.<br\>Please try again.');
                        }
                    }
                };
                    
                up.xhr.onload = up.onload;
            },
            uploadProgress : function(e) {
                if (e.lengthComputable) {
                    var percentage = Math.round((e.loaded * 100) / e.total);
                    up.$status.html('Uploaded: '+percentage+'%');
                }
            },
            uploadLoaded : function(e) {
                $('#drop-area').html('Uploaded: 100%');
            },
            onload : function (e) {
                up.uploading = false;
                currentRequest = $.getJSON("/student/update-resume/info/", function(data) {
                    up.$dropbox.removeClass('uploading').addClass('success');
                    up.$status.html('<p>Resume Updated.</p><p>'+ data["num_of_extracted_keywords"]+ ' keywords extracted.');
                    $("#view_resume_link").attr("href", "/media/" + data["path_to_new_resume"]);
                });
            }
        };
        $(up.init);
    };
});
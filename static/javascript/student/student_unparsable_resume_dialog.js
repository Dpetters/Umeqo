function open_unparsable_resume_dialog(){
    var dialog = $('<div class="dialog"></div>')
    .dialog({
        autoOpen: false,
        title:"Unparsable Resume",
        dialogClass: "unparsable_resume_dialog",
        modal:true,
        width:426,
        resizable: false,
        close: function() {
            $(".unparsable_resume_dialog").remove();
        }
    });
    dialog.dialog('open');
    return dialog;
};
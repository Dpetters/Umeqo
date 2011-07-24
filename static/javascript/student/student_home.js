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
});
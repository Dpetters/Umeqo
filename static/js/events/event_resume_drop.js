function dropResume() {
    $('#event_resume_drop').attr('id', 'event_resume_undrop');
    $('#event_resume_undrop').html('Undo Drop Resume');
}
function undropResume() {
    $('#event_resume_undrop').attr('id', 'event_resume_drop');
    $('#event_resume_drop').html('Drop Resume');
}
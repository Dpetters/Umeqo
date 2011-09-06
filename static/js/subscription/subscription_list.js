$(document).ready(function(){
    $("#firm_type").change(function(){
        switch($(this).val()){
            case 'P':
                window.location = window.location + "?employer_type=P"
                break;
            case 'S':
                window.location = window.location + "?employer_type=S"
                break;
            case 'M':
                window.location = window.location + "?employer_type=M"
                break;
            case 'L':
                window.location = window.location + "?employer_type=L"
                break;
            default:
                break;
        }
    })
    $("#firm_type").val("");
});

var student_body_statistics_chart;
var student_body_statistics_series;
var second_major_statistics_chart;
var second_major_statistics_series;

function update_student_body_statistics() {
    var y_axis = $('#id_y_axis').val();
    var x_axis = $('#id_x_axis').val();
    $.ajax({
        url : STUDENT_BODY_STATISTICS_URL,
        data : {
            'y_axis' : y_axis,
            'x_axis' : x_axis
        },
        beforeSend: function (arr, $form, options) {
            show_form_submit_loader("#custom_statistics_controls");
        },
        complete : function(jqXHR, textStatus) {
            hide_form_submit_loader("#custom_statistics_controls");
        },
        success : function(data) {
            if (typeof(student_body_statistics_series) != "undefined"){
                student_body_statistics_series.remove();
            }
            data.series.color = "#4572A7";
            student_body_statistics_series = student_body_statistics_chart.addSeries(data.series);
            student_body_statistics_chart.xAxis[0].setCategories(data.categories);
            student_body_statistics_chart.yAxis[0].setExtremes(data.y_axis_min, data.y_axis_max);
            student_body_statistics_chart.yAxis[0].axisTitle.attr({
                text: data.y_axis_text
            });
        },
        error : errors_in_message_area_handler
    });
}

function update_second_major_statistics() {
    $.ajax({
        url : SECOND_MAJOR_STATISTICS_URL,
        data : {
            'first_major' : $('#id_first_major').val(),
        },
        beforeSend: function (arr, $form, options) {
            show_form_submit_loader("#second_major_statistics_controls");
        },
        complete : function(jqXHR, textStatus) {
            hide_form_submit_loader("#second_major_statistics_controls");
        },
        success : function(data) {
            if (typeof(second_major_statistics_series) != "undefined"){
                second_major_statistics_series.remove();
            }
            data.series.color = "#4572A7";
            second_major_statistics_series = second_major_statistics_chart.addSeries(data.series);
            second_major_statistics_chart.xAxis[0].setCategories(data.categories);
        },
        error : errors_in_message_area_handler
    });
}

$(document).ready(function() {
    $('#id_y_axis, #id_x_axis').change(function() {
        update_student_body_statistics();
    });

    $('#id_first_major').change(function() {
        update_second_major_statistics();
    });
    
    second_major_statistics_chart = new Highcharts.Chart({
        chart : {
            renderTo : 'second_major_chart_container',
            defaultSeriesType : 'column',
        },
        title : {
            text : "",
        },
        tooltip : {
            formatter : function() {
                return '' + this.x + ': ' + Highcharts.numberFormat(this.y, 2) + '';
            }
        },
        legend:{
            enabled: false,
        },
        credits : {
            enabled: false,
        },
        xAxis: {
            labels: {
            rotation: -45,
            align: 'right',
            style: {
                font: 'normal 10px Verdana, sans-serif'
            }
         }
        },
        yAxis: {
            title: {
                text: '# of students'
            },
            tickInterval: 1
        },
        plotOptions : {
            column : {
                pointPadding : 0.2,
                borderWidth : 0
            }
        },
    });
    
    student_body_statistics_chart = new Highcharts.Chart({
        chart : {
            renderTo : 'student_body_chart_container',
            defaultSeriesType : 'column',
        },
        title : {
            text : "",
        },
        tooltip : {
            formatter : function() {
                return '' + this.x + ': ' + Highcharts.numberFormat(this.y, 2) + '';
            }
        },
        legend:{
            enabled: false,
        },
        credits : {
            enabled: false,
        },
        xAxis: {
        },
        yAxis: {
        },
        plotOptions : {
            column : {
                pointPadding : 0.2,
                borderWidth : 0
            }
        },
    });
    update_second_major_statistics();
    update_student_body_statistics();
});
var student_body_statistics_chart;
var student_body_statistics_series;

function update_student_body_statistics() {
    var y_axis = $('#id_y_axis').val();
    var x_axis = $('#id_x_axis').val();
    $.ajax({
        url : STUDENT_BODY_STATISTICS_URL,
        data : {
            'y_axis' : y_axis,
            'x_axis' : x_axis
        },
        success : function(data) {
            if (typeof(student_body_statistics_series) != "undefined"){
                student_body_statistics_series.remove();
            }
            data.series.color = "#4572A7";
            student_body_statistics_series = data.series;
            student_body_statistics_series = student_body_statistics_chart.addSeries(student_body_statistics_series);
            student_body_statistics_chart.xAxis[0].setCategories(data.categories);
            student_body_statistics_chart.yAxis[0].axisTitle.attr({
                text: data.y_axis_text
            });
        },
        error : errors_in_message_area_handler
    });
}
$(document).ready(function() {
    $('#id_y_axis, #id_x_axis').change(function() {
        update_student_body_statistics();
    });

    student_body_statistics_chart = new Highcharts.Chart({
        chart : {
            renderTo : 'student_body_graph_container',
            defaultSeriesType : 'column',
        },
        title : {
            text : "",
        },
        tooltip : {
            formatter : function() {
                return '' + this.x + ': ' + this.y + '';
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
    update_student_body_statistics();
});
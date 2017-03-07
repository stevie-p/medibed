$(document).ready(function() {
    var chart = c3.generate({
        bindto: '#move_chart',
        data: {
            columns: [
                ['data1', 30, 200, 100, 400, 150, 250]
            ],
            type: 'spline',
            names: {
                data1: 'Time moved'
            }
        }
    });
});
$(document).ready(function() {
	var chartData = [
		{
			time: new Date('2017-03-10T10:00:00.123456'),
			forceLeg1: 0.2,
			forceLeg2: -0.2
		},
		{
			time: new Date('2017-03-10T10:00:10.123456'),
			forceLeg1: 0.3,
			forceLeg2: -0.25
		},
		{
			time: new Date('2017-03-10T10:00:20.123456'),
			forceLeg1: 0.2,
			forceLeg2: -0.2
		},
		{
			time: new Date('2017-03-10T10:00:30.123456'),
			forceLeg1: 0.2,
			forceLeg2: -0.2
		},
		{
			time: new Date('2017-03-10T10:00:25.123456'),
			forceLeg1: 1.2,
			forceLeg2: -2.2
		}
	];
	console.log('Generating chart');
	var chart = c3.generate({
		bindto: '#data-stream',
		data: {
			x: 'time',
			// xFormat: '%Y-%m-%dT%H:%M:%S',
			json: chartData,
			keys: {
				x: 'time',
				value: ['forceLeg1', 'forceLeg2']
			},
			types: {
				forceLeg1: 'area',
				forceLeg2: 'area'
			},
			colors: {
				forceLeg1: '#337ab7',
				forceLeg2: '#337ab7'
			}
		},
		axis: {
			x: {
				type: 'timeseries',
				tick: {
					format: '%H:%M:%S',
					count: 5
				}
			},
			y: {
				show: false
			}
		},
		legend: {
			show: false
		},
		padding: {
			left: 20,
			right: 20
		}
	});

	window.addReading = function (point) {
		console.log(point, new Date(point.time));
		chartData.push({
			time: new Date(point.time),
			forceLeg1: point.forceLeg1,
			forceLeg2: -point.forceLeg2
		});
		chart.load({
			json: chartData,
			keys: {
				x: 'time',
				value: ['forceLeg1', 'forceLeg2']
			}
		});
	};

});
$(document).ready(function() {
	var chartData = [
		{
			time: '2017-03-10T10:00:00Z',
			forceLeg1: 0.2,
			forceLeg2: -0.2,
			forceTotal: 0.4,
			status: "Empty",
			sound: 0
		},
		{
			time: '2017-03-10T10:00:10Z',
			forceLeg1: 0.3,
			forceLeg2: -0.25,
			forceTotal: 0.55,
			status: "Empty",
			sound: 0
		},
		{
			time: '2017-03-10T10:00:20Z',
			forceLeg1: 0.2,
			forceLeg2: -0.2,
			forceTotal: 0.4,
			status: "Empty",
			sound: 0
		},
		{
			time: '2017-03-10T10:00:30Z',
			forceLeg1: 0.2,
			forceLeg2: -0.2,
			forceTotal: 0.4,
			status: "Empty",
			sound: 0
		},
		{
			time: '2017-03-10T10:00:25Z',
			forceLeg1: 1.2,
			forceLeg2: -2.2,
			forceTotal: 2.6,
			status: "Empty",
			sound: 0
		}
	];
	console.log('Generating chart');
	var chart = c3.generate({
		bindto: '#data-stream',
		data: {
			x: 'time',
			xFormat: '%Y-%m-%dT%H:%M:%SZ',
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
		if(point.forceLeg2) point.forceLeg2 = -point.forceLeg2;
		chartData.push(point);
		chart.load({
			json: chartData,
			keys: {
				x: 'time',
				value: ['forceLeg1', 'forceLeg2']
			}
		});
	};

});
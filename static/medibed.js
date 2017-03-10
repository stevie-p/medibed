$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/medibed');
	
	var connection = $('#toggle-connection');
	socket.on('connect', function() {
		console.log('Connected');
		connection.removeClass('text-danger');
		connection.addClass('text-success');
		connection.attr('title', 'Connected. Click to disconnect.');
		connection.find('span.sr-only').text('Connected');
	});  
	socket.on('disconnect', function() {
		connection.removeClass('text-success');
		connection.addClass('text-danger');
		connection.attr('title', 'Disconnected. Click to connect.');
		connection.find('span.sr-only').text('Disconnected');
	});  

	socket.on('logEvent', function(data) {
		console.log('Event recieved', data);
		var tablerow = $("<tr></tr>");
		var strTime = new Date(data.time).toLocaleTimeString();
    		$("<td></td>").text(strTime).appendTo(tablerow);
    		$("<td></td>").text(data.message).appendTo(tablerow);
		if(data.class) {
			tablerow.addClass(data.class);
		}
    		$("#log").append(tablerow);	
	});
    
	socket.on('reading', function(data) {
		// console.log(data.status);
		addReading(data);
		$("#bed1 .status").text(data.status);
		var bedInner = $("#bed1 .bed-inner");
		switch(data.status) {
			case "Empty":
				bedInner.removeClass("success");
				bedInner.addClass("info");
				break;
			case "Occupied":
				bedInner.removeClass("info");
				bedInner.addClass("success");
				break;
		}
		$("#bed1 .leg1").text(data.forceLeg1 + " N");
		$("#bed1 .leg2").text(data.forceLeg2 + " N");
		var soundSpan = $("#bed1 .sound>span");
		switch(data.sound) {
			case 1:
				soundSpan.removeClass("fa-volume-off");
				soundSpan.addClass("fa-volume-up");
				break;
			default:
				soundSpan.removeClass("fa-volume-up");
				soundSpan.addClass("fa-volume-off");
		}
	});
	
	function clock() {
		var d = new Date;
		var dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
		var locale = 'en-GB';
		var date = d.toLocaleDateString(locale, dateOptions);
		var timeOptions = { hour: 'numeric', minute: 'numeric' };
		var time = d.toLocaleTimeString(locale, timeOptions);
		$("#clock").html(date + " &middot; " + time);
	}
	setInterval(clock, 1000);
	
	setTimeout(function() {
		addReading({
			time: new Date('2017-03-10T10:00:55.123456'),
			forceLeg1: 2.5,
			forceLeg2: 2.2,
			forceTotal: 4.7,
			status: "Occupied",
			sound: 0
		});
	}, 2000);
	
});
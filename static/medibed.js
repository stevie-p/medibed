$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/medibed');
  /*  
  socket.on('change', function(data) {
    tablerow = $("<tr></tr>");
    $("<td></td>").text(data.time).appendTo(tablerow);
    $("<td></td>").text(data.forceLeg1).appendTo(tablerow);
    $("<td></td>").text(data.forceLeg2).appendTo(tablerow);
    $("<td></td>").text(data.forceTotal).appendTo(tablerow);
    $("<td></td>").text(data.status).appendTo(tablerow);
    $("#log").append(tablerow);
  });
	*/
	socket.on('reading', function(data) {
		console.log(data.status);
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
	
});
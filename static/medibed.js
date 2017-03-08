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
		$("#bed1 .status").text(data.status);
		switch(data.status) {
			case "Empty":
				$("#bed1 .bed-inner").addClass("info");
			case "Occupied":
				$("#bed1 .bed-inner").addClass("success");
		}
		$("#bed1 .leg1").text(data.forceLeg1 + " N");
		$("#bed1 .leg2").text(data.forceLeg2 + " N");
	});
	
});
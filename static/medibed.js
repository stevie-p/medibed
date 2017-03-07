$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/medibed');
    
  socket.on('change', function(data) {
    tablerow = $("<tr></tr>");
    $("<td></td>").text(data.time).appendTo(tablerow);
    $("<td></td>").text(data.forceLeg1).appendTo(tablerow);
    $("<td></td>").text(data.forceLeg2).appendTo(tablerow);
    $("<td></td>").text(data.forceTotal).appendTo(tablerow);
    $("<td></td>").text(data.status).appendTo(tablerow);
    $("#log").append(tablerow);
  });
});
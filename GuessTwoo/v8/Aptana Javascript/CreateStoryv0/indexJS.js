/**
 * @author seant_000
 */

//alert("Working");

$(document).ready(function() {
	//$("#hello").fadeOut(3000);

	$("#getButton").click(function() {
		$.getJSON("/print", function(data) {
			$("#print").append(data.printMe + "<br>" + data.printMe2 + "<br>");
			/*
			 $.each(data, function() {
			 $.each(this, function(key, value) {
			 $("#print").append(
			 value.printMe + "<br>" + value.printMe2 + "<br>"
			 );
			 });
			 }); */
		});
	});
	
	$("#sendMe").submit(function(event) {
		event.preventDefault();
		var data = '{"data":' + JSON.stringify($("#sendMe").serializeArray()) + '}';
		$("#print").append(data.toString() + "<br>");
		$.ajax({
			cache : false,
			url : "/display",
			type : "POST",
			dataType : "json",
			headers : {
				"Content-Type":"application/json"
			},
			data : data,
			success : function() {
			},
			error : function() {
			}
		});
	});
	
	
	/*
	$("#postButton").click(function() {
		var data = JSON.stringify($("#sendMe").serializeArray());
		$("#print").append(data.toString() + "<br>");
		$.ajax({
			cache : false,
			url : "/display",
			type : "POST",
			dataType : "json",
			data : data,
			success : function() {
			},
			error : function() {
			}
		});
	});
	*/

});


/**
 * @author seant_000
 */


//
// Like and Spam stories
//

$(document).on('click', '.likeButton', function() {
	var data = '{"storyID":' + JSON.stringify($(this).attr("value")) + '}';
		
	$.ajax({
		cache : false,
		url : "/likeStory",
		type : "POST",
		dataType : "json",
		headers : {
			"Content-Type" : "application/json"
		},
		data : data,
		// Probably have to do some stuff with the success and failure functions
		success : function() {
		},
		error : function() {
		}
	});
});

$(document).on('click', '.spamButton', function() {
	var data = '{"storyID":' + JSON.stringify($(this).attr("value")) + '}';
		
	$.ajax({
		cache : false,
		url : "/spamStory",
		type : "POST",
		dataType : "json",
		headers : {
			"Content-Type" : "application/json"
		},
		data : data,
		// Probably have to do some stuff with the success and failure functions
		success : function() {
		},
		error : function() {
		}
	});
});








/*

 Hard coded variables in the views

 var hardTitleLength = 50;
 var hardStoryLength = 1000;
 var hardTotalTagLength = 1000;
 var hardUsernameLength = 50;
 // Not in the database
 var hardPasswordLength = 50;
 var hardEmailLength = 50;
 */
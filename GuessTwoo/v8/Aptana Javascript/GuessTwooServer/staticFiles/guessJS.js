/**
 * @author seant_000
 */

$(document).ready(function() {
	var currentStoryDisplayedGuessID = -1;

	if ($("#currentStoryGuessDiv")) {
		currentStoryDisplayedID = $("#currentStoryGuessDiv").attr("value");
	};

	$(document).on('click', '#yesButton', function() {
		var data = '{"storyID":' + JSON.stringify($("#currentStoryGuessDiv").attr("value")) + '}';

		$.ajax({
			cache : false,
			url : "/guessSuccessPost",
			type : "POST",
			dataType : "json",
			headers : {
				"Content-Type" : "application/json"
			},
			data : data,
			success : function() {
			},
			error : function() {
			}
		});

		// Proabbly will change in the future
		var storyID = $("#currentStoryGuessDiv").attr("value");
		var httpRequest = "/guessNextStory?storyID=" + storyID;
		$.getJSON(httpRequest, function(data) {
			if (data.moreStories == "false") {
				// Once again, change this message later on
				$("#currentStoryGuessDiv").replaceWith('<div id="noMoreStoriesToGuess">No more stories!</div>');
			} else {
				$("#currentStoryGuessDiv").replaceWith(data.nextStory);
				if ($("#currentStoryGuessDiv")) {
					currentStoryDisplayedID = $("#currentStoryGuessDiv").attr("value");
				};
			}
		});
	});

	$(document).on('click', '#noButton', function() {
		var data = '{"storyID":' + JSON.stringify($("#currentStoryGuessDiv").attr("value")) + '}';

		$.ajax({
			cache : false,
			url : "/guessFailurePost",
			type : "POST",
			dataType : "json",
			headers : {
				"Content-Type" : "application/json"
			},
			data : data,
			success : function() {
			},
			error : function() {
			}
		});

		// Proabbly will change in the future
		var storyID = $("#currentStoryGuessDiv").attr("value");
		var httpRequest = "/guessNextStory?storyID=" + storyID;
		$.getJSON(httpRequest, function(data) {
			if (data.moreStories == "false") {
				// Once again, change this message later on
				$("#currentStoryGuessDiv").replaceWith('<div id="noMoreStoriesToGuess">No more stories!</div>');
			} else {
				$("#currentStoryGuessDiv").replaceWith(data.nextStory);
				if ($("#currentStoryGuessDiv")) {
					currentStoryDisplayedID = $("#currentStoryGuessDiv").attr("value");
				};
			}
		});
	});

	$(document).on('click', '#skipButton', function() {
		var data = '{"storyID":' + JSON.stringify($("#currentStoryGuessDiv").attr("value")) + '}';
		
		$.ajax({
			cache : false,
			url : "/guessSkipPost",
			type : "POST",
			dataType : "json",
			headers : {
				"Content-Type" : "application/json"
			},
			data : data,
			success : function() {
			},
			error : function() {
			}
		});

		// Proabbly will change in the future
		var storyID = $("#currentStoryGuessDiv").attr("value");
		var httpRequest = "/guessNextStory?storyID=" + storyID;
		$.getJSON(httpRequest, function(data) {
			if (data.moreStories == "false") {
				// Once again, change this message later on
				$("#currentStoryGuessDiv").replaceWith('<div id="noMoreStoriesToGuess">No more stories!</div>');
			} else {
				$("#currentStoryGuessDiv").replaceWith(data.nextStory);
				if ($("#currentStoryGuessDiv")) {
					currentStoryDisplayedID = $("#currentStoryGuessDiv").attr("value");
				};
			}
		});
	});

});

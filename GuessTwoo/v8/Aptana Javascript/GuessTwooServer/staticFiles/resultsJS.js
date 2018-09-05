/**
 * @author seant_000
 */

//
// Helper functions
//

//
// On load stuff
//

$(document).ready(function() {
	var currentStoryDisplayedID = -1;
	if ($(".storyResultsDiv")) {
		currentStoryDisplayedID = $(".storyResultsDiv").attr("value");
	}

	// DON'T FORGET TO UPDATE CURRENTSTORYDISPLAYID EVERY TIME!!!

	$("#resultsGetMoreStories").click(function() {
		var httpRequest = "/resultsGetMoreStories?currentStoryID=" + currentStoryDisplayedID;

		// Proabbly will change in the future
		$.getJSON(httpRequest, function(data) {
			if(data.moreStories == "false") {
				$("#resultsLastDivMessage").replaceWith('<div id="resultsLastDivMessage">No more stories!</div>');
			}
			else {
				// I have two divs, one from the long function from route and this one--may be inefficient
				var insertDiv = document.createElement('div');
				$(data.nextStory).insertBefore("#resultsLastDiv");
				currentStoryDisplayedID = $("#resultsLastDiv").prev().attr("value");
			}
		});
	});
});

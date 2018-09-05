/**
 * @author seant_000
 */
//
// On load stuff
//

$(document).ready(function() {
	var currentStoryDisplayedID = -1;
	if ($("#storyOriginal")) {
		currentStoryDisplayedID = $("#storyOriginal").attr("value");
	}

	// DON'T FORGET TO UPDATE CURRENTSTORYDISPLAYID EVERY TIME!!!

	$("#myStoriesReviewStoriesGetMoreStories").click(function() {
		var httpRequest = "/myStories/reviewStories/getMoreStories?currentStoryID=" + currentStoryDisplayedID;

		// Proabbly will change in the future
		$.getJSON(httpRequest, function(data) {
			if(data.moreStories == "false") {
				$("#myStoriesReviewStoriesLastMessage").replaceWith('<div id="myStoriesReviewStoriesLastMessage">No more stories!</div>');
			}
			else {
				// I have two divs, one from the long function from route and this one--may be inefficient
				var insertDiv = document.createElement('div');
				$(data.nextStory).insertBefore("#myStoriesReviewStoriesLast");
				currentStoryDisplayedID = $("#myStoriesReviewStoriesLast").prev().attr("value");
			}
		});
	});
});

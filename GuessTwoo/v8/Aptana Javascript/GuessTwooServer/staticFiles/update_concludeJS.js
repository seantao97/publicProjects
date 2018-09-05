/**
 * @author seant_000
 */

//
// Start jQuery
//

$(document).ready(function() {
	var storyID = $("#updateConcludeStoryDiv").attr("value");
	var httpRequest = "/myStories/reviewStories/updateConcludeStory/InitialValues?storyID=" + storyID;

	// Proabbly will change in the future
	$.getJSON(httpRequest, function(data) {
		var title = data.title;
		var text = data.text;
		var userComment = data.userComment;
		$("#title").attr("value", title);
		$("#story").text(text);
		$("#userComment").text(userComment);
	});

});

/**
 * @author seant_000
 */

//
// This route deals with stories (like, spam) and for everything under review stories
//

//
// Hard coded variables
//

var hardTableNameStoryLikers = 'story_likersv1';
var hardTableNameStorySpam = 'story_spamv1';
var hardTableNameStory = 'storyv1';

var hardMaxTagLength = 50;
var hardMaxNumTags = 50;
var hardMaxTitleLength = 50;
var hardMaxStoryLength = 1000;
var hardMaxUsernameLength = 50;
// This isn't the same one in the database since that one is bcrypt
var hardMaxPasswordLength = 50;
var hardMaxEmailLength = 50;
// One day
var hardExpireTimeMS = 86400000;

//
// Import standard libraries
//

var passport = require('passport');
var bcrypt = require('bcrypt-nodejs');
var uuid = require('node-uuid');
var nodemailer = require('nodemailer');
var xoauth2 = require('xoauth2');

//
// Import custom libraries
//

// model
// Assuming that everything is in the same folder
var Model = require('./model');
var Database = require('./db');

//
// Helper functions
//

// check to make sure concluded is an expected input from update/conclude
// THIS MAY CHANGE IN THE FUTURE DEPENDING ON IF THE TEXT IN THE SELECT CHANGES
function checkConcluded(checkMe) {
	if (checkMe == "Yes!!! :)") {
		// success
		return 's';
	}
	if (checkMe == "No... :(") {
		// failure
		return 'f';
	}
	if (checkMe == "Not done yet") {
		// not done
		return 'n';
	}
	return 'error';
};

// check for null and undefined
// CHECK THIS FUNCTION FOR CORRECTNESS LATER ON!!!
function checkDefined(checkMe) {
	if (checkMe == 'undefined' || checkMe == null) {
		return false;
	}
	return true;
};

/*
<div id="storyOriginal" value=... >
<p>
<div name="storyTitle"></div>
</p>
<p>
<div name="storyText"></div>
</p>
<p>
<div name="storyLikes"></div>
</p>
<p>
<div name="storySpam"></div>
</p>
<button class="likeButton" name="storyLikeButton" value=... type="button">
Like
</button>
<button class="spamButton" name="storySpamButton" value=... type="button">
Spam
</button>
<p><a href="/myStories/reviewStories/updateConcludeStory?currentStoryID=...">Update/Conclude</a>
</p>
</div>
*/

// Create the div for a new story
// THIS IS BROKEN AND DOESN'T EXACTLY CREATE THE ABOVE HTML
var newDiv = function(title, text, likes, spam, storyID) {
	return '<div id="storyOriginal" value="' + storyID + '" ><p><div name="storyTitle">Title: ' + title + '</div></p><p><div name="storyText">Text: ' + text + '</div></p><p><div name="storyLikes">Likes: ' + likes + '</div></p><p><div name="storySpam">Spam: ' + spam + '</div></p><button class="likeButton" name="storyLikeButton" value="' + storyID + '" type="button">Like</button><button class="spamButton" name="storySpamButton" value="' + storyID + '" type="button">Spam</button>' + '<p><a href="/myStories/reviewStories/updateConcludeStory?currentStoryID=' + storyID + '">Update/Conclude</a></p>' + '</div>';
};

// Create the new div for updating and concluding a story
// THIS WILL CHANGE LAER ON FOR SURE
// Doesn't exactly match the bottom HTML
var newDivUpdateConclude = function(storyID) {
	return ' <div name="updateConcludeStoryDiv" id="updateConcludeStoryDiv" value="' + storyID + '" > <form method="post" action="/myStories/reviewStories/updateConcludeStoryPost?storyID=' + storyID + '" id="updateStoryForm" name="updateStoryForm" enctype="multipart/form-data" > <p> Title: <input type="text" id="title" name="title" size="12" maxlength=50 required="required" /> </p> <p> Story: <textarea name="story" id="story" size="12" maxlength=1000 required="required" rows="4" cols="50" form="updateStoryForm"></textarea> </p><p> How did it end up? What did your love say? <br><select name="concluded" id="concluded" form="updateStoryForm"> <option value="Yes!!! :)">Yes!!! :)</option><option value="No... :(">No... :(</option><option value="Not done yet" selected>Not done yet</option> </select></p> <p> User comment: <textarea type="text" name="userComment" id="userComment" form="updateStoryForm" size="12" maxlength=1000 rows="4" cols="50"></textarea> </p> <p> <input type="submit" name="updateStory" id="updateStory" value="update"/> </p> </form> </div>';
};
/*
<div name="updateConcludeStoryDiv">
<form method="post" action="/myStories/reviewStories/updateConcludeStories" id="createStoryForm" enctype="multipart/form-data" >
<p>
Title:
<input type="text" name="title" id="title" size="12" maxlength=50 required="required" />
</p>
<p>
Story:
<textarea name="story" id="story" form="createStoryForm" size="12" maxlength=1000 required="required" rows="4" cols="50"></textarea>
</p>
<p>
Tags:
<textarea type="text" name="tags" id="tags" form="createStoryForm" size="12" maxlength=1000 rows="4" cols="50" placeholder="Just type tags separated by spaces." ></textarea>
</p>
<p>
How did it end up? What did your love say?
<br>
<select>
<option value="Yes!!! :)"></option>
<option value="No... :("></option>
<option value="Not done yet" selected></option>
</select>
</p>
<p>
User comment:
<textarea type="text" name="userComment" id="userComment" form="createStoryForm" size="12" maxlength=1000 rows="4" cols="50"></textarea>
</p>
<p>
<input type="submit" name="createStory" id="createStory" value="Create"/>
</p>
</form>
</div>
*/

//
// Routing functions
//

// reviewStories
// NOT the name of the GET HTTP request
var reviewStories = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}

		var storyDB = Database.knex(hardTableNameStory);

		storyDB.where('user', user.username).min('storyID as storyID').then(function(firstID) {
			Database.knex.select('*').from(hardTableNameStory).where('storyID', firstID[0].storyID).then(function(rows) {
				if (rows.length == 0) {
					res.render('reviewStories', {
						lastStoryMessage : "No stories to show!"
					});
				} else {
					var originalStory = newDiv(rows[0].title, rows[0].text, rows[0].likes, rows[0].spam, rows[0].storyID);
					res.render('reviewStories', {
						originalStory : originalStory
					});
				}
			});
		});
	}
};

// like a story
var likeStory = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}
		var storyID = req.body.storyID;

		var storyLikersDB = Database.knex(hardTableNameStoryLikers);
		storyLikersDB.where('user', user.username).andWhere('storyID', storyID).then(function(rows) {
			if (rows.length != 0) {
				// Do nothing, maybe unlike in the future???
			} else {
				var currentDate = new Date().toMysqlFormat();
				var newStoryLike = new Model.StoryLikers({
					storyID : storyID,
					user : user.username,
					date : currentDate
				}).save(null, {
					method : 'insert'
				});
				var likedStory = new Model.Story({
					storyID : storyID
				}).fetch().then(function(model) {
					var newLikeCount = model.toJSON().likes + 1;
					var likedStoryUpdate = new Model.Story({
						storyID : storyID,
						likes : newLikeCount
					}).save(null, {
						method : 'update'
					});
				});
			}
		});
	}
};

// spam a story
var spamStory = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}
		var storyID = req.body.storyID;

		var storySpamDB = Database.knex(hardTableNameStorySpam);
		storySpamDB.where('user', user.username).andWhere('storyID', storyID).then(function(rows) {
			if (rows.length != 0) {
				// Do nothing, maybe unlike in the future???
			} else {
				var currentDate = new Date().toMysqlFormat();
				var newStorySpam = new Model.StorySpam({
					storyID : storyID,
					user : user.username,
					date : currentDate
				}).save(null, {
					method : 'insert'
				});
				var spamStory = new Model.Story({
					storyID : storyID
				}).fetch().then(function(model) {
					var newSpamCount = model.toJSON().spam + 1;
					var likedStoryUpdate = new Model.Story({
						storyID : storyID,
						spam : newSpamCount
					}).save(null, {
						method : 'update'
					});
				});
			}
		});
	}
};

// my stories, review stories, get more stories
var myStoriesReviewStoriesGetMoreStories = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}
		var currentStoryID = req.query.currentStoryID;

		var storyDB = Database.knex(hardTableNameStory);

		storyDB.where('user', user.username).andWhere('storyID', '>', currentStoryID).min('storyID as storyID').then(function(firstID) {
			Database.knex.select('*').from(hardTableNameStory).where('storyID', firstID[0].storyID).then(function(rows) {
				if (rows.length == 0) {
					res.json({
						"nextStory" : "",
						"moreStories" : "false"
					});
				} else {
					var nextStory = newDiv(rows[0].title, rows[0].text, rows[0].likes, rows[0].spam, rows[0].storyID);
					res.json({
						"nextStory" : nextStory,
						"moreStories" : "true"
					});
				}
			});
		});
	}
};

var updateConcludeStory = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}
		var currentStoryID = req.query.currentStoryID;

		var storyDB = Database.knex(hardTableNameStory);

		storyDB.where('storyID', currentStoryID).min('storyID as storyID').then(function(rows) {
			if (rows.length == 0) {
				res.status(404);
				res.render('404', {
					title : '404 Not Found'
				});
			} else {
				res.render('update_conclude', {
					forms : newDivUpdateConclude(currentStoryID)
				});
			}
		});
	}
};

var updateConcludeStoriesInitialValues = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var storyID = req.query.storyID;
		var storyPromise = null;
		userPromise = new Model.Story({
			storyID : storyID
		}).fetch().then(function(model) {
			if (!checkDefined(model)) {
				res.status(404);
				res.render('404', {
					title : '404 Not Found'
				});
			} else {
				res.json({
					"title" : model.toJSON().title,
					"text" : model.toJSON().text,
					"userComment" : model.toJSON().userComment
				});
			}
		});
	}
};

// updateConcludeStoryPost
// Create Story post
var updateConcludeStoryPost = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var storyID = req.query.storyID;
		var title = req.body.title;
		var story = req.body.story;
		var userComment = req.body.userComment;
		var concludedChecked = checkConcluded(req.body.concluded);

		// Maybe later on add a function to get rid of hashtags
		if (!checkDefined(title) || !checkDefined(story) || title.length > hardMaxTitleLength || story.length > hardMaxStoryLength || concludedChecked == 'error') {
			// This redirect should show an error message later on
			res.redirect('/myStories/reviewStories/updateConcludeStory');
		} else {
			var currentDate = new Date().toMysqlFormat();
			var user = req.user;

			if (user !== undefined) {
				user = user.toJSON();
			}
			var updateConcludedDate = null;
			if (concludedChecked != 'n') {
				updateConcludedDate = currentDate;
			}

			var createStoryObj = new Model.Story({
				storyID : storyID,
				title : title,
				text : story,
				dateWritten : currentDate,
				dateConcluded : updateConcludedDate,
				concluded : concludedChecked,
				userComment : userComment
			}).save(null, {
				method : 'update'
			});
			
			//
			//
			//
			//
			// IF CONCLUDED, UPDATE POINTS
			// DEFINITELY HAVE TO UPDATE USER RIGHT/WRONG SCORES; DO THESE TWO LATER!!!
			//
			//
			//
			//
			
			// Probably should display something telling the user the story was updated
			res.redirect('/myStories/reviewStories');
		}
	}
};

// export functions
/**************************************/

// review stories
module.exports.reviewStories = reviewStories;

// like story
module.exports.likeStory = likeStory;

// spam story
module.exports.spamStory = spamStory;

// my stories review stories get more stories
module.exports.myStoriesReviewStoriesGetMoreStories = myStoriesReviewStoriesGetMoreStories;

// my stories review stories update conclude story
module.exports.updateConcludeStory = updateConcludeStory;

// my stories review stories update conclude story
module.exports.updateConcludeStoriesInitialValues = updateConcludeStoriesInitialValues;

// my stories review stories update conclude story post
module.exports.updateConcludeStoryPost = updateConcludeStoryPost;


/**
 * @author seant_000
 */

//
// Hard coded variables
//

var hardTableNameUser = 'usersv1';
var hardTableNameTags = 'story_tagv1';
var hardTableNameStory = 'storyv1';
var hardTableNameUUID = 'uuid';
var hardTableNameUUIDResetPassword = 'uuidresetpwd';
var hardTableNameStoryLikers = 'story_likersv1';
var hardTableNameStorySpam = 'story_spamv1';
var hardTableNameSeenBefore = 'seen_beforev1';
var hardTableNameUserVotes = 'user_votesv1';

//
// Importing modules
//

// Assuming that the db.js file is in the same folder
// as model.js
var DB = require('./db').DB;

//
// Setting up bookshelf
//

var User = DB.Model.extend({
	tableName : hardTableNameUser,
	idAttribute : 'username'
});

var Email = DB.Model.extend({
	tableName : hardTableNameUser,
	idAttribute : 'email'
});

var TagsByTags = DB.Model.extend({
	tableName : hardTableNameTags,
	idAttribute : 'tag'
});

var TagsByStory = DB.Model.extend({
	tableName : hardTableNameTags,
	idAttribute : 'storyID'
});

var Story = DB.Model.extend({
	tableName : hardTableNameStory,
	idAttribute : 'storyID'
});

var UUID = DB.Model.extend({
	tableName : hardTableNameUUID,
	idAttribute : 'uuid'
});

var UUIDResetPwd = DB.Model.extend({
	tableName : hardTableNameUUIDResetPassword,
	idAttribute : 'uuid'
});

var StoryLikers = DB.Model.extend({
	tableName : hardTableNameStoryLikers,
	idAttribute : 'storyID'
});

var StorySpam = DB.Model.extend({
	tableName : hardTableNameStorySpam,
	idAttribute : 'storyID'
});

var SeenBefore = DB.Model.extend({
	tableName : hardTableNameSeenBefore,
	idAttribute : 'username'
});

var UserVotes = DB.Model.extend({
	tableName : hardTableNameUserVotes,
	idAttribute : 'user'
});



//
// Exporting
//

module.exports = {
	User : User,
	Email : Email,
	TagsByTags : TagsByTags,
	TagsByStory : TagsByStory,
	Story : Story,
	UUID : UUID,
	UUIDResetPwd : UUIDResetPwd,
	StoryLikers : StoryLikers,
	StorySpam : StorySpam,
	SeenBefore : SeenBefore,
	UserVotes : UserVotes
};


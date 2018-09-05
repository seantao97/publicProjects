/**
 * @author seant_000
 */

//
// This route deals with signup, signin, and creating a story
//

//
// Hard coded variables
//

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
var hardEmailServiceProvider = "gmail";
var hardGmailAccount = "guesstwoo@gmail.com";
var hardClientID = "566871957904-dp1f90ig8qlopu8e3smfnn751ame27e4.apps.googleusercontent.com";
var hardClientSecret = "O1M27RsvT7JaT5fv5-8Lc6l4";
var hardRefreshToken = "1/MMgjCjKSsZKFkyI8iuJfrSlRFLcKKrNAw7S1YC2agt0";
var hardCachedAccessToken = 'ya29.Ci8gAw9U_C8NuGsQMeqEOB9Ia9nzzjvfo78hrFL2R9T05PVZ9jaHMjYcfy3aU07O6w';
var hardEmailSender = "guesstwoo@gmail.com";

// Do these really need to be hard coded variables
var hardEmailSubject = "Registration Confirmation for GuessTwoo";
var hardEmailText = "Please click on the following link to confirm the registration: ";
var hardEmailHTMLBefore = "<p>Please click on the following link to confirm the registration: ";
var hardEmailHTMLAfter = "</p>";

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
// Assuming that model.js is in the same folder
var Model = require('./model');

//
// Helper functions
//

// Date to MySQL format
function twoDigits(d) {
	if (0 <= d && d < 10)
		return "0" + d.toString();
	if (-10 < d && d < 0)
		return "-0" + (-1 * d).toString();
	return d.toString();
};

Date.prototype.toMysqlFormat = function() {
	return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

// Once mysql dates are retrieved and converted to JSON, they can't be compared with
// JS Date(); this fixes that
function parseMysqlJSONDate(someJSON) {
	/*
	EXAMPLE of a Mysql.toJSON().toString() date:
	Fri Jul 15 2016 05:33:13 GMT-0400 (Eastern Daylight Time)
	012345678901234567890123456...
	10       20
	*/
	//	var month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
	var str = someJSON.toString();
	var month_names_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
	var shortMonth = str.slice(4, 7);
	var month = 0;
	for (var i = 0; i < month_names_short.length; i++) {
		if (shortMonth == month_names_short[i]) {
			month = i + 1;
		}
	};
	var day = str.slice(8, 10);
	var year = str.slice(11, 15);
	var time = str.slice(16, 24);
	var MysqlString = year + "-" + twoDigits(month) + "-" + twoDigits(day) + " " + time;
	return MysqlString;
};

// check tags are valid
function checkTags(tagsArray) {
	for (var i = 0; i < tagsArray.length; i++) {
		if (tagsArray[i].length > hardMaxTagLength || tagsArray[i].length < 0) {
			return false;
		}
	}
	return true;
};

// check for null and undefined
// CHECK THIS FUNCTION FOR CORRECTNESS LATER ON!!!
function checkDefined(checkMe) {
	if (checkMe == 'undefined' || checkMe == null) {
		return false;
	}
	return true;
};

//
// Routing functions
//

// my stories
var myStories = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		return res.render('myStories');
	}
};

// Create Story post
var createStoryPost = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var title = req.body.title;
		var story = req.body.story;
		var tagString = req.body.tags;
		// Maybe later on add a function to get rid of hashtags
		var tags = tagString.replace(/\n+/g, " ").trim().split(/\s*\b\s*/, hardMaxNumTags);
		if (!checkDefined(title) || !checkDefined(story) || !checkDefined(tags) || !checkTags(tags) || title.length > hardMaxTitleLength || story.length > hardMaxStoryLength) {
			// This redirect should show an error message later on
			res.redirect('/myStories/createStory');
		} else {

			var currentDate = new Date().toMysqlFormat();
			var user = req.user;

			if (user !== undefined) {
				user = user.toJSON();
			}

			var createStoryObj = new Model.Story({
				title : title,
				text : story,
				user : user.username,
				dateWritten : currentDate,
				dateConcluded : null,
				concluded : 'n',
				likes : 0,
				spam : 0,
				userComment : "",
				yes : 0,
				no : 0,
				location : null
			});

			createStoryObj.save(null, {
				method : 'insert'
			}).then(function(model) {

				createStoryObj.fetch().then(function(modelStory) {
					var storyID = model.toJSON().storyID;
					for (var i = 0; i < tags.length; i++) {
						var UpdateTags = new Model.TagsByStory({
							storyID : storyID,
							tag : tags[i]
						});
						UpdateTags.save(null, {
							method : 'insert'
						});
					};
				});
			});
			res.redirect('/myStories');
		}
	}
};

// Create Story
var createStory = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		return res.render('create_story');
	}
};

// index
var index = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}
		// This will probably change if the index gets changed later on
		res.render('index', {
			title : 'Home',
			user : user
		});
	}
};

// sign in
// GET
var signIn = function(req, res, next) {
	if (req.isAuthenticated()) {
		res.redirect('/');
	}
	// This title will need to be changed later on
	res.render('signin', {
		title : 'Sign In'
	});
};

// sign in
// POST
var signInPost = function(req, res, next) {
	// Once again, the success, failure, error, and not user redirects will probably change
	// later on, as well as the JSON
	passport.authenticate('local', { successRedirect: '/',
	failureRedirect: '/signin'}, function(err, user, info) {
	if(err) {
	return res.render('signin', {title: 'Sign In', errorMessage: err.message});
	}

	if(!user) {
	return res.render('signin', {title: 'Sign In', errorMessage: info.message});
	}
	return req.logIn(user, function(err) {
	if(err) {
	return res.render('signin', {title: 'Sign In', errorMessage: err.message});
	} else {
	return res.redirect('/');
	}
	});
	})(req, res, next);
};

// sign up
// GET
var signUp = function(req, res, next) {
	if (req.isAuthenticated()) {
		res.redirect('/');
	} else {
		// This JSON will certainly change later on
		res.render('signup', {
			title : 'Sign Up'
		});
	}
};

// sign up
// POST
var signUpPost = function(req, res, next) {
	var user = req.body;
	if (!user) {
		// This JSON will probably change later on
		res.render('signup', {
			title : 'signup',
			errorMessage : 'Error: null object received'
		});
	}

	var userPromise = null;
	userPromise = new Model.User({
		username : user.username
	}).fetch();

	var emailPromise = null;
	emailPromise = new Model.Email({
		email : user.email
	}).fetch();
	var username = user.username;
	var email = user.email;
	var password = user.password;

	return userPromise.then(function(model) {
		emailPromise.then(function(modelEmail) {
			if (model || modelEmail || !checkDefined(password)) {
				if (model) {
					// This JSON will probably change later on
					res.render('signup', {
						title : 'signup',
						errorMessage : 'Error: username already exists'
					});
				} else if (modelEmail) {
					// This JSON will probably change later on
					res.render('signup', {
						title : 'signup',
						errorMessage : 'Error: email already exists'
					});
					res.end();
				} else {
					// This JSON will probably change later on
					res.render('signup', {
						title : 'signup',
						errorMessage : 'Error: null password'
					});
					res.end();
				}
			} else {

				var hashPwd = bcrypt.hashSync(password);

				if (username.length > hardMaxUsernameLength || password.length > hardMaxPasswordLength || username.length <= 0 || password.length <= 0 || email.length > hardMaxEmailLength || email.length <= 0) {
					// This JSON will probably change later on
					res.render('signup', {
						title : 'signup',
						// Later on add the actual character limit
						errorMessage : 'Error: all fields have a character limit and must be filled'
					});
					res.end();
				}

				// Later on we have to modify this if the signup page
				// gets more complicated

				else {
					var newUUID = uuid.v4();
					var dateCreatedUUID = new Date();
					var dateExpiresUUID = new Date(dateCreatedUUID.getTime() + hardExpireTimeMS).toMysqlFormat();
					dateCreatedUUID = dateCreatedUUID.toMysqlFormat();

					var newUUIDObj = new Model.UUID({
						uuid : newUUID,
						dateCreated : dateCreatedUUID,
						dateExpires : dateExpiresUUID,
						expired : 'n',
						used : 'n',
						username : username,
						password : hashPwd,
						email : email
					});

					newUUIDObj.save(null, {
						method : 'insert'
					}).then(function(model) {
						var smtpTransport = nodemailer.createTransport({
							service : hardEmailServiceProvider,
							auth : {
								xoauth2 : xoauth2.createXOAuth2Generator({
									user : hardGmailAccount,
									clientId : hardClientID,
									clientSecret : hardClientSecret,
									refreshToken : hardRefreshToken,
									accessToken : hardCachedAccessToken
								})
							}
						});
						// the string should be replaced by like req.host or something like that
						var confirmationLink = "https://localhost:3001" + "/verifySignUp?uuid=" + newUUID;

						var mailOptions = {
							from : hardEmailSender,
							to : user.email,
							subject : hardEmailSubject,
							text : hardEmailText + confirmationLink,
							html : hardEmailHTMLBefore + confirmationLink + hardEmailHTMLAfter
						};

						smtpTransport.sendMail(mailOptions, function(error, response) {
							if (error) {
								// Probably have to do something more that just this lol
								console.log(error);
							} else {
								res.render('email_sent');
								res.end();
							}
						});
					});
				}
			}
		});
	});
};

// GET
// verifySignUp
var verifySignUp = function(req, res, next) {
	var uuid = req.query.uuid;
	var currentDate = new Date().toMysqlFormat();
	var newUUIDObj = new Model.UUID({
		uuid : uuid
	}).fetch().then(function(model) {
		var JSONUUIDObj = model.toJSON();
		var expireDate = JSONUUIDObj.dateExpires;
		// Make sure this comparison function works!!!!!!!!!
		if ((currentDate <= parseMysqlJSONDate(expireDate)) && (JSONUUIDObj.used == 'n')) {
			//register user and redirect to signin page
			var signUpUser = new Model.User({
				username : JSONUUIDObj.username,
				password : JSONUUIDObj.password,
				email : JSONUUIDObj.email,
				firstname : null,
				lastname : null,
				age : null,
				gender : null,
				score : 1000,
				right : 0,
				wrong : 0,
				location : null,
				registerDate : currentDate,
				currentStory : -1
			});

			var UUIDExpired = new Model.UUID({
				uuid : uuid,
				expired : 'y',
				used : 'y',
			}).save(null, {
				method : 'update'
			}).then(function(model) {
				signUpUser.save(null, {
					method : 'insert'
				}).then(function(model) {
					// This JSON needs to change sometime
					res.render('signin', {
						title : 'Sign In'
					});
				});
			});

		} else {
			// This JSON also needs to be changed in the future
			res.render('signup', {
				title : 'signup',
				errorMessage : 'Could not verify account or account already verified...there is a one day limit before the email expires'
			});
			res.end();
		}
	});
};

// sign out
var signOut = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		req.logout();
		res.redirect('/signin');
	}
};

// settings
var settings = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var user = req.user;
		if (user !== undefined) {
			user = user.toJSON();
		}

		var userPromise = null;
		userPromise = new Model.User({
			username : user
		}).fetch().then(function(model) {
			if (checkDefined(userPromise) == false) {
				res.render('signup', {
					title : 'signup',
					errorMessage : 'Error: user not in database'
				});
			} else {
				res.render('settings', {
					score : model.toJSON().score
				});
			}
		});

	}
};

// change password
var changePassword = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		return res.render('change_password');
	}
};

// change password post
var changePasswordPost = function(req, res, next) {
	if (!req.isAuthenticated()) {
		res.redirect('/signin');
	} else {
		var info = req.body;
		if (!checkDefined(info)) {
			// This JSON will probably change later on
			res.render('change_password', {
				errorMessage : 'Error: null object received'
			});
		} else {
			var userPromise = null;
			userPromise = new Model.User({
				username : info.username
			}).fetch().then(function(model) {
				if (!checkDefined(userPromise) || !bcrypt.compareSync(info.oldPassword, model.toJSON().password)) {
					res.render('change_password', {
						errorMessage : 'Error: invalid username or password'
					});
				} else {
					if (info.newPassword.length > hardMaxPasswordLength) {
						res.render('change_password', {
							errorMessage : 'Error: new password too long'
						});
					} else {
						var updatedUser = new Model.User({
							username : info.username,
							password : bcrypt.hashSync(info.newPassword),
						}).save(null, {
							method : 'update'
						}).then(function(model) {
							req.logout();
							res.redirect('/signin');
						});
					}
				}
			});
		}
	}
};

// 404 not found
var notFound404 = function(req, res, next) {
	res.status(404);
	res.render('404', {
		title : '404 Not Found'
	});
};

// export functions
/**************************************/
// index
module.exports.index = index;

// sigin in
// GET
module.exports.signIn = signIn;
// POST
module.exports.signInPost = signInPost;

// sign up
// GET
module.exports.signUp = signUp;
// POST
module.exports.signUpPost = signUpPost;

// sign out
module.exports.signOut = signOut;

// 404 not found
module.exports.notFound404 = notFound404;

// create story
module.exports.createStory = createStory;

// create story post
module.exports.createStoryPost = createStoryPost;

// verifySignUp
module.exports.verifySignUp = verifySignUp;

// settings
module.exports.settings = settings;

// changePassword
module.exports.changePassword = changePassword;

// changePasswordPost
module.exports.changePasswordPost = changePasswordPost;

// myStories
module.exports.myStories = myStories;


/**
 * @author seant_000
 */

// Import standard libraries
var passport = require('passport');
var bcrypt = require('bcrypt-nodejs');

var uuid = require('node-uuid');
var nodemailer = require('nodemailer');
var xoauth2 = require('xoauth2');

// Helper functions

function twoDigits(d) {
	if (0 <= d && d < 10)
		return "0" + d.toString();
	if (-10 < d && d < 0)
		return "-0" + (-1 * d).toString();
	return d.toString();
};

function parseMysqlJSONDate(someJSON) {
/*
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
	var MysqlString = year + "-" + twoDigits(month) + "-" + day + " " + time;
	return MysqlString;
};

Date.prototype.toMysqlFormat = function() {
	return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

// Import custom libraries

// model
// Assuming that model.js is in the same folder
var Model = require('./model');

// Routing functions

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
	// The redirect and the render JSON will probably change later on
	if (req.isAuthenticated()) {
		res.redirect('/');
	}
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
	// This redirect may change later on
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
	var userPromise = null;
	userPromise = new Model.User({
		username : user.username
	}).fetch();

	var emailPromise = null;
	emailPromise = new Model.Email({
		email : user.email
	}).fetch();

	return userPromise.then(function(model) {
		emailPromise.then(function(modelEmail) {
			if (model || modelEmail) {
				if (model) {
					// This render will probably change later on
					res.render('signup', {
						title : 'signup',
						errorMessage : 'username already exists'
					});
				} else {
					// This render will probably change later on
					res.render('signup', {
						title : 'signup',
						errorMessage : 'email already exists'
					});
					res.end();
				}
			} else {

				var password = user.password;
				var hashPwd = bcrypt.hashSync(password);

				var newUUID = uuid.v4();
				var dateCreatedUUID = new Date();
				var dateExpiresUUID = new Date(dateCreatedUUID.getTime() + 86400000).toMysqlFormat();
				dateCreatedUUID = dateCreatedUUID.toMysqlFormat();
				
				var newUUIDObj = new Model.UUID({
					uuid : newUUID,
					dateCreated : dateCreatedUUID,
					dateExpires : dateExpiresUUID,
					expired : 'n',
					used : 'n',
					username : user.username,
					password : hashPwd,
					email : user.email
				});

				newUUIDObj.save(null, {
					method : 'insert'
				}).then(function(model) {

					var smtpTransport = nodemailer.createTransport({
						service : "gmail",
						auth : {
							xoauth2 : xoauth2.createXOAuth2Generator({
								user : "guesstwoo@gmail.com",
								clientId : "566871957904-dp1f90ig8qlopu8e3smfnn751ame27e4.apps.googleusercontent.com",
								clientSecret : "O1M27RsvT7JaT5fv5-8Lc6l4",
								refreshToken : "1/MMgjCjKSsZKFkyI8iuJfrSlRFLcKKrNAw7S1YC2agt0",
								accessToken : 'ya29.Ci8gAw9U_C8NuGsQMeqEOB9Ia9nzzjvfo78hrFL2R9T05PVZ9jaHMjYcfy3aU07O6w'
							})
						}
					});
					// the string should be replaced by like req.host or something like that
					var confirmationLink = "https://localhost:3001" + "/verifySignUp?uuid=" + newUUID;

					var mailOptions = {
						from : "guesstwoo@gmail.com",
						to : user.email,
						subject : "Registration Confirmation",
						text : "Please click on the following link to confirm the registration: " + confirmationLink,
						html : "<p>Please click on the following link to confirm the registration: " + confirmationLink + "</p>"
					};

					smtpTransport.sendMail(mailOptions, function(error, response) {
						if (error) {
							console.log(error);
						} else {
							// This will probably change later on
							res.render('email_sent');
							res.end();
						}
					});

				});
				// Old code start
				/*
				var password = user.password;
				var hashPwd = bcrypt.hashSync(password);

				// **************************************************** //
				// MORE VALIDATION GOES HERE(E.G. PASSWORD VALIDATION)
				// right length for username and password
				// no email previously exists
				// add other stuff based on what else is included in the signup page
				// **************************************************** //

				// Later on we have to modify this if the signup page
				// gets more complicated

				var signUpUser = new Model.User({
				username : user.username,
				password : hashPwd,
				email : user.email
				});

				signUpUser.save(null, {
				method : 'insert'
				}).then(function(model) {
				// sign in the newly registered user
				signInPost(req, res, next);
				});
				*/
				// Old code end

			}
		});
	});
};

var verifySignUp = function(req, res, next) {
	var uuid = req.query.uuid;
	var currentDate = new Date().toMysqlFormat();
	var newUUIDObj = new Model.UUID({
		uuid : uuid
	}).fetch().then(function(model) {
		var JSONUUIDObj = model.toJSON();
		var expireDate = JSONUUIDObj.dateExpires;
		// Make sure this comparison function works!!!!!!!!!
		console.log("current: " + currentDate);
		console.log("expire: " + expireDate);
		console.log("no JSON: " + parseMysqlJSONDate(expireDate));
		console.log("date: " + (currentDate < expireDate));
		console.log("used: " + (JSONUUIDObj.used == 'n'));
		if ((currentDate <= parseMysqlJSONDate(expireDate)) && (JSONUUIDObj.used == 'n')) {
			//register user and redirect to signin page
			var signUpUser = new Model.User({
				username : JSONUUIDObj.username,
				password : JSONUUIDObj.password,
				email : JSONUUIDObj.email
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
					// sign in the newly registered user
					// This link needs to be changed in the future
					signIn(req, res, next);
				});
			});

		} else {
			res.render('signup', {
				title : 'signup',
				errorMessage : 'Could not verify via email...there is a one day limit before the email expires'
			});
			res.end();
		}
	});
};

// sign out
var signOut = function(req, res, next) {
	if (!req.isAuthenticated()) {
		notFound404(req, res, next);
	} else {
		req.logout();
		// This redicrect may also change
		res.redirect('/signin');
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

// verifySignUp
module.exports.verifySignUp = verifySignUp;


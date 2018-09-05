/**
 * @author seant_000
 */

//
// This route deals with resetting a password
//

//
// Hard Coded Variables
//

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
var hardEmailSubject = "Reset Password Confirmation for GuessTwoo";
var hardEmailText = "";
var hardEmailHTMLBefore = "";
var hardEmailHTMLAfter = "";

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
// Helper Functions
//

// check for null and undefined
// CHECK THIS FUNCTION FOR CORRECTNESS LATER ON!!!
function checkDefined(checkMe) {
	if (checkMe == 'undefined' || checkMe == null) {
		return false;
	}
	return true;
};

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

//Generate random password

String.prototype.pick = function(min, max) {
	var n,
	    chars = '';
	if ( typeof max === 'undefined') {
		n = min;
	} else {
		n = min + Math.floor(Math.random() * (max - min + 1));
	}
	for (var i = 0; i < n; i++) {
		chars += this.charAt(Math.floor(Math.random() * this.length));
	}
	return chars;
};

String.prototype.shuffle = function() {
	var array = this.split('');
	var tmp,
	    current,
	    top = array.length;
	if (top)
		while (--top) {
			current = Math.floor(Math.random() * (top + 1));
			tmp = array[current];
			array[current] = array[top];
			array[top] = tmp;
		}
	return array.join('');
};

function generatePassword() {
	var lowercase = 'abcdefghijklmnopqrstuvwxyz';
	var uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
	var numbers = '0123456789';
	var all = lowercase + uppercase + numbers;

	var password = '';
	password += lowercase.pick(2);
	password += uppercase.pick(2);
	password += numbers.pick(2);
	password += all.pick(4);
	return password.shuffle();
};

//
// Routing functions
//

// reset password
var resetPwd = function(req, res, next) {
	if (req.isAuthenticated()) {
		res.redirect('/');
	} else {
		res.render('reset_password');
	}
};

//reset password post
var resetPwdPost = function(req, res, next) {
	var info = req.body;
	if (!info) {
		res.render('reset_password', {
			errorMessage : 'Error: null object received'
		});
	}

	var emailPromise = null;
	emailPromise = new Model.Email({
		email : info.email
	}).fetch().then(function(modelEmail) {
		if (!checkDefined(modelEmail)) {
			res.render('reset_password', {
				errorMessage : 'Error: email not in database'
			});
		} else {
			var newPwd = generatePassword();
			var hashPwd = bcrypt.hashSync(newPwd);

			var newUUID = uuid.v4();

			var dateCreatedUUID = new Date();
			var dateExpiresUUID = new Date(dateCreatedUUID.getTime() + hardExpireTimeMS).toMysqlFormat();
			dateCreatedUUID = dateCreatedUUID.toMysqlFormat();

			var newUUIDObj = new Model.UUIDResetPwd({
				uuid : newUUID,
				dateCreated : dateCreatedUUID,
				dateExpires : dateExpiresUUID,
				expired : 'n',
				used : 'n',
				newPwd : hashPwd,
				email : info.email
			});

			newUUIDObj.save(null, {
				method : 'insert'
			}).then(function(modelUUID) {
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
				var confirmationLink = "https://localhost:3001" + "/verifyResetPwd?uuid=" + newUUID;

				var mailOptions = {
					from : hardEmailSender,
					to : info.email,
					subject : "GuessTwoo password reset confirmation",
					text : "Username: " + modelEmail.toJSON().username + "\nNew password: " + newPwd + "\nClick this link to reset your password: " + confirmationLink,
					html : "<p>Username: " + modelEmail.toJSON().username + "</p><p>New password: " + newPwd + "</p><p>Click this link to reset your password: " + confirmationLink
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
	});
};

// verify reset
var verifyResetPwd = function(req, res, next) {
	var uuid = req.query.uuid;
	var currentDate = new Date().toMysqlFormat();
	var newUUIDObj = new Model.UUIDResetPwd({
		uuid : uuid
	}).fetch().then(function(model) {
		var JSONUUIDObj = model.toJSON();
		var expireDate = JSONUUIDObj.dateExpires;
		// Make sure this comparison function works!!!!!!!!!
		if ((currentDate <= parseMysqlJSONDate(expireDate)) && (JSONUUIDObj.used == 'n')) {
			//register user and redirect to signin page
			var signUpUser = new Model.Email({
				email : JSONUUIDObj.email,
				password : JSONUUIDObj.newPwd
			});

			var UUIDExpired = new Model.UUIDResetPwd({
				uuid : uuid,
				expired : 'y',
				used : 'y'
			}).save(null, {
				method : 'update'
			}).then(function(model) {
				signUpUser.save(null, {
					method : 'update'
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
				errorMessage : 'Could not verify the password change...there is a one day limit before the email expires'
			});
			res.end();
		}
	});
};

// export functions
/**************************************/

// reset password
module.exports.resetPwd = resetPwd;

// reset password post
module.exports.resetPwdPost = resetPwdPost;

// verify reset password
module.exports.verifyResetPwd = verifyResetPwd;


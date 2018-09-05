// hard coded variables

var hardPrivateKey = 'C:/Program Files (x86)/nodejs/ssl/private.key';
var hardCertificate = 'C:/Program Files (x86)/nodejs/ssl/certificate.pem';
var hardViewEngine = 'ejs';
//This is the default one from the website; we'll definiately need to change this
var hardSessionSecret = 'secret strategic xxzzz code';
var hardInsecurePort = 3000;
var hardSecurePort = 3001;

// Import standard libraries
var http = require('http');
var https = require('https');
var fs = require('fs');
var express = require('express');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var bcrypt = require('bcrypt-nodejs');
var ejs = require('ejs');
var path = require('path');
var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;

// Import custom libraries

// Assuming everything is in the same folder

// routes
var route = require('./route');
// model
var Model = require('./model');

// Define key for RSA

var options = {
	key : fs.readFileSync(hardPrivateKey),
	cert : fs.readFileSync(hardCertificate)
};

// Begin express code

var app = express();

// Redirects all traffic to https
app.all('*', function(req, res, next) {
	if (req.secure) {
		return next();
	};
	// The redirect line will have to change later on
	// We will also delete console.log later on
	console.log('https://' + req.hostname + ':' + hardSecurePort + req.url);
	res.redirect('https://' + req.hostname + ':' + hardSecurePort + req.url);
});


passport.use(new LocalStrategy(function(username, password, done) {
	new Model.User({
		username : username
	}).fetch().then(function(data) {
		var user = data;
		if (user === null) {
			return done(null, false, {
				message : 'Invalid username or password'
			});
		} else {
			user = data.toJSON();
			if (!bcrypt.compareSync(password, user.password)) {
				return done(null, false, {
					message : 'Invalid username or password'
				});
			} else {
				return done(null, user);
			}
		}
	});
}));

passport.serializeUser(function(user, done) {
	done(null, user.username);
});

passport.deserializeUser(function(username, done) {
	new Model.User({
		username : username
	}).fetch().then(function(user) {
		done(null, user);
	});
});

// This line probably is antiquated
//app.set('port', process.env.PORT || 3000);

// This will be replaced with the location of the views folder
app.set('views', path.join(__dirname, 'views'));
// This may change if we don't use ejs anymore, but I doubt that
app.set('view engine', hardViewEngine);

app.use(cookieParser());
app.use(bodyParser.urlencoded({
	// Do we actually want extended?
	extended : true
}));

// Later learn how express session works and also what resave and saveUninitialized are
// maybe change them later on

app.use(session({
	secret : hardSessionSecret,
	resave : true,
	saveUninitialized : true
}));
app.use(passport.initialize());
app.use(passport.session());

// GET
app.get('/', route.index);

// signin
// GET
app.get('/signin', route.signIn);
// POST
app.post('/signin', route.signInPost);

// signup
// GET
app.get('/signup', route.signUp);
// POST
app.post('/signup', route.signUpPost);

// logout
// GET
app.get('/signout', route.signOut);

// verify signup
app.get('/verifySignUp', route.verifySignUp);

/********************************/

/********************************/
// 404 not found
app.use(route.notFound404);

// This is antiquated before we did https
/*
 var server = app.listen(app.get('port'), function(err) {
 if(err) throw err;

 var message = 'Server is running @ http://localhost:' + server.address().port;
 console.log(message);
 });
 */

var insecureRedirectServer = http.createServer(app).listen(hardInsecurePort, function(err) {
	if (err)
		throw err;

	var message = 'Insecure server is running @ http://localhost:' + insecureRedirectServer.address().port;
	console.log(message);
});

var secureServer = https.createServer(options, app).listen(hardSecurePort, function(err) {
	if (err)
		throw err;

	var message = 'Secure server is running @ https://localhost:' + secureServer.address().port;
	console.log(message);
});


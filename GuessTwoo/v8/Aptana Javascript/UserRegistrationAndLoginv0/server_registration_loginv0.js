// Before passport and https

/**
 * @author seant_000
 */

//
// Hard-coded variables
//

	var hardFilePath = 'C:/Users/seant_000/Desktop/GuessTwoo/Static/index.html';
	var hardPort = 8125;
	var hardSessionSecret = 'findabetteronelaterlol';

//
// Importing modules
//

var http = require('http');
var express = require('express');

var path = require('path');
var fs = require('fs');
var multer = require('multer');
var bodyParser = require('body-parser');
//var work = require('./lib/timetrack');
var mysql = require('mysql');
var passport = require('passport');
var flash = require('connect-flash');
var morgan = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var session = require('express-session');

//
// Setting up express
//

var app = express();
//app.use(morgan('dev'));
//app.use(cookieParser());
//app.use(bodyParser());
//app.set('view engine', 'ejs');
//app.use(session({ secret: hardSessionSecret }));
//app.use(passport.initialize());
//app.use(passport.session());
//app.use(flash());

//
// Setting up the database connection
//

/*
 * Now in seperate module
var connection = mysql.createConnection({
	host : hardHost,
	user : hardDataUser,
	password : hardDataPwd,
	database : hardDataSchema
});

connection.connect(function(err) {
	if (!err) {
		console.log("Database is connected!");
	} else {
		console.log("Error connecting database...");
	}
});
*/

//
// Handling user registration
//

var urlencodedParser = bodyParser.urlencoded({
	extended : false
});

// /new_user may change depending on the html page
app.post('/new_user', urlencodedParser, function(req, res) {
	console.log("hi");
	console.log("Username: " + req.body.username);
	console.log("Password: " + req.body.password);
	console.log("Email: " + req.body.email);

	var newUser = {
		username : req.body.username,
		password : req.body.password,
		email : req.body.email
	};
	connection.query('INSERT INTO users_v0 SET ?', newUser, function(err, res) {
		if (err) {
			throw err;
		}
	});
	res.end("User updated!");
});


//
// Displaying home page
//

app.get('/', function(request, response) {
	var filePath = hardFilePath;
	fs.readFile(filePath, function(error, content) {
		if (error) {
			if (error.code == 'ENOENT') {
				fs.readFile('./404.html', function(error, content) {
					response.writeHead(200, {
						'Content-Type' : 'text/html'
					});
					response.end(content, 'utf-8');
				});
			} else {
				response.writeHead(500);
				response.end('Sorry, check with the site admin for error: ' + error.code + ' ..\n');
				response.end();
			}
		} else {
			response.writeHead(200, {
				'Content-Type' : 'text/html'
			});
			response.end(content, 'utf-8');
		}
	});
});

//
// Setting up the server
//

var server = app.listen(hardPort, function() {
	console.log('Server started');
});
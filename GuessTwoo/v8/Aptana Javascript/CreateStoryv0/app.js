// Completed

/**
 * @author seant_000
 */

var http = require('http');
var fs = require('fs');
var express = require('express');
var bodyParser = require('body-parser');

var jsonParser = bodyParser.json();

var route = require('./route');

var app = express();

app.use(express.static('staticFiles'));

app.get('/', route.index);
app.get('/print', route.print);
app.post('/display', jsonParser, route.display);

var server = app.listen(4000, function(err) {
	if (err) {
		throw err;
	}
	var message = 'Server is running @ http://localhost:' + server.address().port;
	console.log(message);
});

/**
 * @author seant_000
 */

var fs = require('fs');


var hardFilePathHTML = '/staticFiles/index.html';

var index = function(req, res) {
	res.sendFile(__dirname + hardFilePathHTML);
};

var print = function(req, res) {
	res.json({ "printMe" : "yay it",
				"printMe2" : "worked"});
};

var display = function(req, res) {
	console.log("length: " + req.body.data.length);
	console.log("Title: " + req.body.data[0].value);
	console.log("Story: " + req.body.data[1].value);
	res.end();
};

module.exports.index = index;

module.exports.print = print;

module.exports.display = display;
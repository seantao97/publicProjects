var express = require('express');
var app = express();
app.get("/", function(req, res) {
	res.send("Hello world!");
});


var server = app.listen(8000, function(err) {
	if (err)
		throw err;
   var host = server.address().address;
   var port = server.address().port;
   
   console.log("Hello world server listening at http://%s:%s", host, port);
});
/**
 * @author seant_000
 */

//
// Hard coded variables
//

var hardHost = '127.0.0.1';
var hardDataUser = 'root';
var hardDataPwd = 'Sean0411';
var hardDataSchema = 'guesstwoo';
var hardUTF = 'UTF8_GENERAL_CI';
var hardDBType = 'mysql';

//
// Import modules
//

// knex is imported later on
var bookshelf = require('bookshelf');

//
// Connecting to database
//

var config = {
	host : hardHost,
	user : hardDataUser,
	password : hardDataPwd,
	database : hardDataSchema,
	charset : hardUTF
};

// Also importing knex here

var knex = require('knex')({
	client : hardDBType,
	connection : config
});

var DB = bookshelf(knex);


//
// Export
//

module.exports.DB = DB;

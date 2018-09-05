/**
 * @author seant_000
 */

//
// Hard coded variables
//

var hardTableName = 'users_v0';
var hardIDAttributeUser = 'username';
var hardIDAttributeEmail = 'email';




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
	tableName : hardTableName,
	idAttribute : hardIDAttributeUser
});

var Email = DB.Model.extend({
	tableName : hardTableName,
	idAttribute : hardIDAttributeEmail
});

var UUID = DB.Model.extend({
	tableName : hardTableNameUUID,
	idAttribute : hardIDAttributeUUID
});

//
// Exporting
//

module.exports = {
	User : User,
	Email : Email,
	UUID : UUID
};


// Require the MongoDB driver
const MongoClient = require('mongodb').MongoClient;

// Connection URL and database name
const url = 'mongodb://localhost:27017/myproject';
const dbName = 'myproject';

// Use connect method to connect to the server
MongoClient.connect(url, function(err, client) {
  console.log("Connected successfully to server");

  const db = client.db(dbName);

  // Create a new collection
  const collection = db.collection('mycollection');

  // Insert a document
  collection.insertOne({ name: "John", age: 30 }, function(err, result) {
    console.log("Inserted document into the collection");
    client.close();
  });
});

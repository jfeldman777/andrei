const MongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017/mydb';

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  console.log('MongoDB connected...');

  // Add your database operations here

  db.close();
});

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Define your routes here

app.listen(port, () => {
  console.log(`Server started on port ${port}`);
});


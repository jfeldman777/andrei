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

'use strict';
var firebase = require("firebase");
// Initialize Firebase
var fs = require('fs');
var config = {
  apiKey: "",
  authDomain: "atom-doggo.firebaseapp.com",
  databaseURL: "https://atom-doggo.firebaseio.com",
  storageBucket: "atom-doggo.appspot.com",
  messagingSenderId: "214143893393"
};
//firebase.initializeApp(config);
const express = require('express');
const logger = require('morgan');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
//current date:
var dateObj = new Date();
var month = dateObj.getUTCMonth() + 1; //months from 1-12
var day = dateObj.getUTCDate();
var year = dateObj.getUTCFullYear();
var testname = "TestDefault";
var newdate =  month + "-" + day + "-" + year ;
//Dweet Install
var dweetClient = require("node-dweetio");
var dweetio = new dweetClient();

app.use(logger('dev'));
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());
// Set view engine to EJS and locate views
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, '/views'));
app.get('/', (request, response) => {
  response.render('index');
});


//get requests that downloads the CSV with the appropriate labels
app.get('/generateCSV', function (req, res, next) {
});

app.post('/pi', function (req, res) {
  const samples = req.body;
  res.send('thanks');
});
app.post('/computer', function (req, res) {
  const sample = req.body;
  res.send('thanks');
});
app.post
const port = 3000; //the port currently being looked at
app.listen(port, function () {
  console.log('Atom Server running on port: ' + port);
});
const express = require('express');
const app = express();
const morgan = require('morgan');
const path = require('path');

const ___dirname = path.resolve();

// settings
app.set('port', process.env.PORT || 9000);
app.set('json spaces',2);

// middleware
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));

// routes
app.use("/api/startFlight", require("./routes/startFlight"));
app.use("/api/endFlight", require("./routes/endFlight"));
app.use(express.static(___dirname + '/public'));


// starting the server
app.listen(app.get('port'), () => {
    console.log(`Server on port ${app.get('port')}`);
});

app.get('/*', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/index.html'));
});

app.get('/planner', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/planner/flightPlanner.html'));
});

app.get('/results', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/results/flightResults.html'));
});

app.get('/jquery.js', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/js/jquery.js'));
});

app.get('/planner.js', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/js/planner.js'));
});

app.get('/results.js', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/js/results.js'));
});

app.get('/style.css', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/css/style.css'));
});

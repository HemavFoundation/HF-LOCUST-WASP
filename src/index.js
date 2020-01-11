const express = require('express');
const app = express();
const morgan = require('morgan');
const cors = require('cors');
const path = require('path');

const ___dirname = path.resolve();

// settings
app.set('port', process.env.PORT || 9000);
app.set('json spaces',2);

// middleware
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cors());

// routes
app.use("/api/connect", require("./routes/connect"));
app.use("/api/load", require("./routes/load"));
app.use("/api/start", require("./routes/start"));


//app.use("/api/ruta", require("./routes/ejemplo"));

// starting the server
app.listen(app.get('port'), () => {
    console.log(`Server on port ${app.get('port')}`);
});

app.get('/*', (req, res) => {
    res.sendFile(path.join(___dirname + '/public'));
});

app.get('/planner', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/planner/flightPlanner.html'));
});

app.get('/history', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/results/History.html'));
});

app.get('/waiting.jpeg', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/planner/waiting.jpeg'));
});
    
app.get('/tick.jpg', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/planner/tick.jpg'));
});
    
app.get('/cross.jpg', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/planner/cross.jpg'));
});

app.get('/flightResults', (req, res) => {
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

app.get('/GetResults.js', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/results/GetResults.js'));
});

app.get('/style.css', (req, res) => {
    res.sendFile(path.join(___dirname + '/public/css/style.css'));
});

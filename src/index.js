const express = require('express');
const app = express();
const morgan = require('morgan');

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

//app.use("/api/ruta", require("./routes/ejemplo"));

// starting the server
app.listen(app.get('port'), () => {
    console.log(`Server on port ${app.get('port')}`);
});

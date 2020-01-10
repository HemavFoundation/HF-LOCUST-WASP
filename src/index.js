const express = require('express');
const app = express();
const morgan = require('morgan');
const cors = require('cors');

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

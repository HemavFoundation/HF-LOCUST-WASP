const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

const Config  = require('./config');
const environment = Config.environment;

router.get("/arm", (req, res) => {

  let options;

  if (environment == "drone") {
    options = {
      mode: "text",
      pythonPath: "/usr/bin/python3",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  } else if (environment == "win") {
    options = {
      mode: "text",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  } else {
    options = {
      mode: "text",
      pythonPath: "/usr/local/bin/python",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  }


  PythonShell.run("arm.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res.status(400).send({ message: "ERROR: Fallo el script start.py" });
	console.log(err);
    }else{
    res.status(200).send({ message: "Drone armado" });
    }
  });

});


router.get("/", (req, res) => {

  let options;

  if (environment == "drone") {
    options = {
      mode: "text",
      pythonPath: "/usr/bin/python3",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  } else if (environment == "win") {
    options = {
      mode: "text",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  } else {
    options = {
      mode: "text",
      pythonPath: "/usr/local/bin/python",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  }


  PythonShell.run("start.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res.status(400).send({ message: "ERROR: Fallo el script start.py" });
	console.log(err);
    }else{
    res.status(200).send({ message: "Proceso de captura de imagenes iniciado" });
    }
  });

});


module.exports = router;

const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

var localhost = true;

class LocationDrone {
  constructor(heading, lon, lat, alt) {
    this.heading = heading;
    this.lon = lon;
    this.lat = lat;
    this.alt = alt;
  }
}

router.get("/", (req, res) => {
  let options;

  if (localhost != true) {
    options = {
      mode: "text",
      pythonPath: "/usr/bin/python3",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  } else {
    options = {
      mode: "text",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts"
    };
  }

  PythonShell.run("connect.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res.status(400).send({ message: "ERROR: Fallo el script connect.py" });
      console.log(err);
    } else {
      location = new LocationDrone(
        results[3],
        results[4],
        results[5],
        results[6]
      );

      res.status(200).send(location);
    }
  });
});

module.exports = router;

const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

var localhost = true;

var location;
var options;

var lonFlight;
var latFlight;
var headingFlight;

var localhost = true;

class LocationDrone {
  constructor(heading, lon, lat, alt) {
    this.heading = heading;
    this.lon = lon;
    this.lat = lat;
    this.alt = alt;
  }
}

router.get("/directionOfFlight", (req, res) => {
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

  PythonShell.run("directionOfFlight.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res
        .status(400)
        .send({ message: "ERROR: Fallo el script directionOfFlight.py" });
      console.log(err);
    } else {
      location = new LocationDrone(
        results[3],
        results[4],
        results[5],
        results[6]
      );

      lonFlight = results[5];
      latFlight = results[4];
      headingFlight = results[3];

      res.status(200).send(location);
    }
  });
});

router.post("/rectangleMission/:distance/:w/:x/:L/:h", (req, res) => {
  const distance = req.params.distance;
  const width = req.params.w;
  const spaceDistance = req.params.x;
  const spaceBtwLines = req.params.L;
  const height = req.params.h;

  let options;

  if (localhost != true) {
    options = {
      mode: "text",
      pythonPath: "/usr/bin/python3",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts",
      args: [
        distance,
        width,
        spaceDistance,
        spaceBtwLines,
        height,
        latFlight,
        lonFlight,
        headingFlight
      ]
    };
  } else {
    options = {
      mode: "text",
      pythonOptions: ["-u"], // get print results in real-time
      scriptPath: "./scripts",
      args: [
        distance,
        width,
        spaceDistance,
        spaceBtwLines,
        height,
        latFlight,
        lonFlight,
        headingFlight
      ]
    };
  }

  PythonShell.run("rectangleMission.py", options, function(err, results) {
    if (err) {
      res
        .status(400)
        .send({ message: "ERROR: Fallo el script rectangleMission.py" });
      console.log(err);
    } else {
      console.log(results);
      res.status(200).send({ message: "Misión cargada correctamente!" });
    }
  });
});

module.exports = router;

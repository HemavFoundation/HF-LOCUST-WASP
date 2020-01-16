const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

class LocationDrone {
  constructor(heading, lon, lat, alt) {
    this.heading = heading;
    this.lon = lon;
    this.lat = lat;
    this.alt = alt;
  }
}

var location;
var options;

router.post("/:distance", (req, res) => {
  const { distance } = req.params;

  var options = {
    mode: "text",
    pythonPath: '/usr/bin/python3',
    pythonOptions: ["-u"], // get print results in real-time
    scriptPath: "./scripts",
    args: [distance]
  };

  PythonShell.run("rectangleMission.py", options, function(err, results) {
    if (err) {
      res
        .status(400)
        .send({ message: "ERROR: Fallo el script rectangleMission.py" });
	console.log(err);
    }else{
    console.log(results);
    res
      .status(200)
      .send({ message: "Misión cargada correctamente!" });
    }
  });
});

module.exports = router;

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
    //pythonOptions: ["-u"], // get print results in real-time
    scriptPath: "./",
    args: [distance]
  };

  PythonShell.run("load.py", options, function(err, results) {
    if (err) throw err;
    console.log(results);
  });
});

module.exports = router;

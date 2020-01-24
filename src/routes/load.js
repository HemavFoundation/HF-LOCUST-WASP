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

router.post("/:distance/:w/:x/:L/:h", (req, res) => {
  const distance = req.params.distance;
  const width = req.params.w;
  const spaceDistance  = req.params.x;
  const  spaceBtwLines  = req.params.L;
  const  height = req.params.h;


  var options = {
    mode: "text",
    pythonPath: '/usr/bin/python3',
    pythonOptions: ["-u"], // get print results in real-time
    scriptPath: "./scripts",
    args: [distance, width, spaceDistance, spaceBtwLines, height]
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

const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

router.get("/part1", (req, res) => {
let options = {
  mode: 'text',
  pythonPath: '/usr/bin/python3.7',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: './scripts'
 };

  PythonShell.run("start_part1.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res.status(400).send({ message: "ERROR: Fallo el script start_part1.py" });
	console.log(err);
    }else{
    res.status(200).send({ message: "Drone armado y en modo Auto" });
    }
  });

});

router.get("/part2", (req, res) => {
  let options = {
    mode: 'text',
    pythonPath: '/usr/bin/python3.7',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: './scripts'
   };
  
    PythonShell.run("start_part2.py", options, function(err, results) {
      //if (err) throw err;
      if (err) {
        res.status(400).send({ message: "ERROR: Fallo el script start_part2.py" });
    console.log(err);
      }else{
      res.status(200).send({ message: "Drone haciendo fotos" });
      }
    });
  
  });

module.exports = router;

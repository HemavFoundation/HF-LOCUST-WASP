const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

router.get("/", (req, res) => {
let options = {
  mode: 'text',
  pythonPath: '/usr/bin/python3',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: './scripts'
 };

  PythonShell.run("start.py", options, function(err, results) {
    //if (err) throw err;
    if (err) {
      res.status(400).send({ message: "ERROR: Fallo el script start.py" });
    }else{
    res.status(200).send({ message: "Iniciado el vuelo, nos vemos a la vuelta" });
    }
  });

});

module.exports = router;

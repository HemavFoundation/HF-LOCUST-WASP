const { Router } = require("express");
const { PythonShell } = require("python-shell");
const router = Router();

router.get("/", (req, res) => {
  // PythonShell.runString("x=1+1;print(x)", null, function(err, results) {
  //   if (err) throw err;
  //   res.send(results);
  // });

  PythonShell.run('./missionTest.py',null,function(err, results){
    if (err) throw err;
    console.log(results);
  });



});

module.exports = router;

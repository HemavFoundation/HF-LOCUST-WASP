const { Router } = require("express");
var { PythonShell } = require("python-shell");
const router = Router();

const Config  = require('./config');
const environment = Config.environment;

router.post("/hook", (req, res) => {
    console.log(req.body) // Call your action on the request here
    res.status(200).end() // Responding is important
  });


module.exports = router;
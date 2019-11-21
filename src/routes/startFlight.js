const { Router } = require('express');
const router = Router();

// const data = require('../data.json');
const fs = require("fs");

router.get('/info', (req,res) => {
    const data = fs.readFileSync("./data2.json");
    res.json(JSON.parse(data));
});

// creamos el plan de vuelo 
router.post('/flightPlan', (req,res) => {
    console.log({req: req.body})
    const flightPlan = {...req.body};

    const obj = {
        areaType: flightPlan.areaType,
        humidity: flightPlan.humidity,
        typeOfFlight: flightPlan.typeOfFlight,
        coordinates: flightPlan.coordinates,
    }
    
    //stringify
    const jsonContent = JSON.stringify(obj);
    console.log(jsonContent);

    fs.writeFile("./data2.json", jsonContent, 'utf8', function(err, data) {
        if (err){
            console.log(err);
            res.send("Ha fallado");
        }
        
        res.send(data);
    });

    // res.json(data);
});

module.exports = router;
const { Router } = require('express');
const router = Router();

//const data = require('../data.json');

router.get('/', (req,res) => {
    res.status(200).send({message: "hola soy un 200"})
});

router.get('/error', (req,res) => {
    res.status(400).send({message: "Esto es un error"})
})

module.exports = router;
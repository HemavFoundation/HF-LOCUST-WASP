const { Router } = require("express");
const checkDiskSpace = require('check-disk-space');
const router = Router();

const Config = require("./config");
const environment = Config.environment

function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
}

router.get('/SDdiskSpace', (req, res) => {

    if (environment == 'drone' || environment == 'mac') {
        checkDiskSpace('/mnt').then((disk) => {
            res.status(200).send({
                freeSpace: round(disk.free / 1073741824, 2),
                sizeSpace: round(disk.size / 1073741824, 2)
            })
        })
    } else {
        checkDiskSpace('C:/').then((disk) => {
            res.status(200).send({
                freeSpace: round(disk.free / 1073741824, 2),
                sizeSpace: round(disk.size / 1073741824, 2)
            })

        })
    }

})

module.exports = router;

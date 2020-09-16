const fs = require('fs')
const {zip} = require('zip-a-folder')

class ZipAFolder {
    static async main(){
        await zip('../../Desktop/HF-LOCUST-WASP/public/results/photos/2020_6_2-8_49','../../Desktop/HF-LOCUST-WASP/public/results/photos.zip');
    }
}

ZipAFolder.main()


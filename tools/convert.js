const sharp = require('sharp');
const fs = require('fs');

const sizes = [16, 32, 48, 128];

async function convertToPng() {
    const svgBuffer = fs.readFileSync('./icons/icon.svg');
    
    for (const size of sizes) {
        await sharp(svgBuffer)
            .resize(size, size)
            .png()
            .toFile(`./icons/icon${size}.png`);
        console.log(`Generated icon${size}.png`);
    }
}

convertToPng().catch(console.error); 
// Same-size PNG part layers -> layered PSD (ag-psd from the Rigby2D checkout). Usage: node layers_to_psd.mjs <parts_dir> <out.psd>
import fs from 'node:fs'; import path from 'node:path'; import { createRequire } from 'node:module';
const require = createRequire('C:/AI/AUTO-ANIM-2D/_vendor/rigby2d/package.json');
const { writePsdBuffer } = require('ag-psd');
const dir = process.argv[2], out = process.argv[3];
const meta = JSON.parse(fs.readFileSync(path.join(dir, 'parts.json'), 'utf8'));
const [W, H] = meta.size;
// decode PNG via the PNG files written as raw RGBA next to them by the python step
const layers = meta.order.map(name => {
  const raw = fs.readFileSync(path.join(dir, name + '.rgba'));
  return { name, imageData: { width: W, height: H, data: new Uint8ClampedArray(raw) }, top: 0, left: 0, bottom: H, right: W };
});
const psd = { width: W, height: H, children: layers };
fs.writeFileSync(out, Buffer.from(writePsdBuffer(psd, { generateThumbnail: false, noBackground: true })));
console.log('wrote', out, layers.length, 'layers');

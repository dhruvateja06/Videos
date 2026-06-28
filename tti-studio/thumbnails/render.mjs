// Render a System Design thumbnail from template.html → PNG (1280×720 @2x = 2560×1440).
// Usage:
//   npm i -D puppeteer-core            # once (Chrome is found via PUPPETEER_EXECUTABLE_PATH or common paths)
//   node thumbnails/render.mjs --ep "01 · START HERE" --lead "The" \
//        --main "Fundamentals" --micro "the building blocks behind every app" \
//        --out assets/thumbnails/sd-ep01.png
import puppeteer from 'puppeteer-core';
import { readFileSync, writeFileSync, unlinkSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) =>
  v.startsWith('--') ? [...a, [v.slice(2), arr[i + 1]]] : a, []));

const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const out = resolve(process.cwd(), args.out || 'assets/thumbnails/thumb.png');

const CHROME = process.env.PUPPETEER_EXECUTABLE_PATH
  || ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
      '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']
     .find(p => existsSync(p));
if (!CHROME) { console.error('No Chrome found. Set PUPPETEER_EXECUTABLE_PATH.'); process.exit(1); }

let html = readFileSync(join(__dirname, 'template.html'), 'utf8')
  .replaceAll('{{EP_BADGE}}', esc('EPISODE ' + (args.ep || '01')))
  .replaceAll('{{TOPIC_LEAD}}', esc(args.lead || ''))
  .replaceAll('{{TOPIC_MAIN}}', esc(args.main || 'Fundamentals'))
  .replaceAll('{{MICRO}}', esc(args.micro || ''));
html = html.replaceAll('{{BIG_NUM}}', esc((String(args.ep||'01').match(/\d+/)||['01'])[0]));

const tmp = join(__dirname, '.render.tmp.html');
writeFileSync(tmp, html);
try {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new',
    args: ['--no-sandbox', '--force-color-profile=srgb', '--hide-scrollbars'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
  await p.goto('file://' + tmp, { waitUntil: 'networkidle0' });
  await Promise.race([p.evaluate(() => document.fonts.ready), new Promise(r => setTimeout(r, 2500))]);
  await (await p.$('#tb')).screenshot({ path: out });
  await b.close();
  console.log('wrote ' + out);
} finally { unlinkSync(tmp); }

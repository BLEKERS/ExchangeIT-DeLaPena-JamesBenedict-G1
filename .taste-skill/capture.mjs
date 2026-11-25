/* Minimal CDP capture: screenshots + computed metrics for authenticated Django pages.
   node .taste-skill/capture.mjs --out .taste-skill/before --session <sessionid> */
import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const arg = (key, fallback) => {
  const i = process.argv.indexOf('--' + key);
  return i >= 0 ? process.argv[i + 1] : fallback;
};
const out = arg('out', '.taste-skill/before');
const session = arg('session', '');
const base = arg('base', 'http://127.0.0.1:8080');
const widths = arg('widths', '1440,1024,768,390').split(',').map(Number);
const pages = arg('pages', 'dashboard,convert,history,favorites,profile,login').split(',');
const paths = {
  dashboard: '/dashboard/', convert: '/converter/convert/', history: '/converter/history/',
  favorites: '/converter/favorites/', profile: '/profile/', login: '/login/',
};
const exe = process.env.CHROME_PATH || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const profile = join(tmpdir(), 'taste-capture-' + process.pid);
mkdirSync(out, { recursive: true });
const child = spawn(exe, ['--headless=new', `--user-data-dir=${profile}`, '--remote-debugging-port=0',
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--mute-audio',
  '--disable-gpu', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', 'about:blank'], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const activePort = join(profile, 'DevToolsActivePort');
async function devtools() {
  for (let i = 0; i < 200; i++) {
    if (existsSync(activePort)) return readFileSync(activePort, 'utf8').split('\n');
    await sleep(50);
  }
  throw new Error('Chrome devtools port timeout');
}

const [port, wsPath] = await devtools();
const ws = new WebSocket(`ws://127.0.0.1:${port}${wsPath.trim()}`);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let seq = 0;
const pending = new Map();
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) {
    const job = pending.get(m.id);
    pending.delete(m.id);
    m.error ? job.rej(new Error(m.error.message)) : job.res(m.result);
  }
};
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const id = ++seq;
  pending.set(id, { res, rej });
  ws.send(JSON.stringify({ id, method, params, sessionId }));
});

const METRICS = `(() => {
  const vw = innerWidth, de = document.documentElement;
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const css = e => e ? getComputedStyle(e) : null;
  const h1 = document.querySelector('h1'), nav = document.querySelector('.nav-dark');
  const amount = document.querySelector('.area-amount input'), result = document.querySelector('.result-value');
  const grid = document.querySelector('.stat-grid');
  const keys = [...document.querySelectorAll('h1,h2,.stat-value,.nav-link,.result-value,.fav-pair,.btn-primary,.btn-secondary')].filter(vis).map(e => e.getBoundingClientRect());
  let overlaps = 0;
  for (let i = 0; i < keys.length; i++) for (let j = i + 1; j < keys.length; j++) {
    const a = keys[i], b = keys[j];
    if (Math.min(a.right,b.right) - Math.max(a.left,b.left) > 3 && Math.min(a.bottom,b.bottom) - Math.max(a.top,b.top) > 3) overlaps++;
  }
  const taps = [...document.querySelectorAll('button,input,select,a.btn-primary,a.btn-secondary,a.nav-link')].filter(vis).map(e => Math.round(e.getBoundingClientRect().height)).filter(h => h > 0);
  return {
    overflowPx: de.scrollWidth - vw,
    spillElements: [...document.querySelectorAll('body *')].filter(vis).filter(e => { const r = e.getBoundingClientRect(); return r.right > vw + 1 || r.left < -1; }).length,
    textOverlapPairs: overlaps,
    navHeight: nav ? Math.round(nav.getBoundingClientRect().height) : null,
    navLinksVisible: [...document.querySelectorAll('.nav-link')].filter(vis).length,
    minTapHeight: taps.length ? Math.min(...taps) : null,
    tapsUnder44: taps.filter(h => h < 44).length,
    amountHeight: amount ? Math.round(amount.getBoundingClientRect().height) : null,
    amountFontPx: amount ? css(amount).fontSize : null,
    resultFontPx: result ? css(result).fontSize : null,
    resultWidth: result ? Math.round(result.getBoundingClientRect().width) : null,
    gridColumns: grid ? css(grid).gridTemplateColumns : null,
    statFontPx: [...document.querySelectorAll('.stat-value')].map(e => css(e).fontSize),
    cardHeights: [...document.querySelectorAll('.stat-card')].map(e => Math.round(e.getBoundingClientRect().height)),
    headingFont: h1 ? css(h1).fontFamily : null,
    headingPx: h1 ? css(h1).fontSize : null,
    monoFont: result ? css(result).fontFamily : null,
    pageHeight: Math.round(de.scrollHeight)
  };
})()`;

const metrics = {}, links = {};
try {
  for (const page of pages) {
    const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
    for (const m of ['Page.enable', 'Runtime.enable', 'Network.enable']) await send(m, {}, sessionId);
    if (page === 'login') {
      await send('Network.clearBrowserCookies', {}, sessionId);
    } else if (session) {
      await send('Network.setCookie', { name: 'sessionid', value: session, domain: '127.0.0.1', path: '/', httpOnly: true }, sessionId);
    }
    for (const w of widths) {
      await send('Emulation.setDeviceMetricsOverride', { width: w, height: w < 500 ? 844 : 900, deviceScaleFactor: 1, mobile: false }, sessionId);
      await send('Page.navigate', { url: base + paths[page] }, sessionId);
      await sleep(450);
      await send('Runtime.evaluate', { expression: 'document.fonts.ready', awaitPromise: true, returnByValue: true }, sessionId);
      if (page === 'convert') {
        await send('Runtime.evaluate', { expression: `if(!document.querySelector('.result-value')){const d=document.createElement('div');d.className='card-dark result-card';d.innerHTML='<div class="result-label">Conversion result</div><div class="result-value">100 USD = 92.00 EUR</div>';document.querySelector('.convert-card').after(d);}`, returnByValue: true }, sessionId);
      }
      const value = await send('Runtime.evaluate', { expression: METRICS, returnByValue: true }, sessionId);
      metrics[`${page}-${w}`] = value.result.value;
      const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false }, sessionId);
      writeFileSync(join(out, `${page}-${w}.png`), Buffer.from(shot.data, 'base64'));
      if (w === widths[0]) {
        const html = await send('Runtime.evaluate', { expression: 'document.documentElement.outerHTML', returnByValue: true }, sessionId);
        writeFileSync(join(out, `${page}.html`), html.result.value);
        const nav = await send('Runtime.evaluate', { expression: `JSON.stringify({links:[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')))],forms:[...new Set([...document.querySelectorAll('form[action]')].map(f=>f.getAttribute('action')))]})`, returnByValue: true }, sessionId);
        links[page] = JSON.parse(nav.result.value);
      }
    }
    await send('Target.closeTarget', { targetId });
  }
  writeFileSync(join(out, 'metrics.json'), JSON.stringify(metrics, null, 2));
  writeFileSync(join(out, 'links.json'), JSON.stringify(links, null, 2));
  console.log('captured', pages.length, 'pages x', widths.length, 'widths into', out);
} finally {
  ws.close();
  child.kill();
  await sleep(300);
  try { rmSync(profile, { recursive: true, force: true }); } catch { /* Edge keeps a lock briefly on Windows. */ }
}

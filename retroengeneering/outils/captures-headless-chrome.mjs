import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';

const OUT = process.env.OUT;
const PROFILE = process.env.PROFILE;
const BASE = 'http://localhost:18080/convertigo/projects/ParcInformatique/DisplayObjects/mobile';
const PORT = 9333;
mkdirSync(OUT, { recursive: true });

const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${PROFILE}`, '--window-size=1366,900',
  '--hide-scrollbars', '--force-device-scale-factor=1', 'about:blank'
], { stdio: 'ignore' });

let wsUrl = null;
for (let i = 0; i < 40 && !wsUrl; i++) {
  await sleep(500);
  try { const r = await fetch(`http://localhost:${PORT}/json/version`); wsUrl = (await r.json()).webSocketDebuggerUrl; } catch {}
}
if (!wsUrl) { chrome.kill(); throw new Error('Chrome CDP not reachable'); }

const ws = new WebSocket(wsUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let nextId = 0; const pending = new Map();
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const id = ++nextId; pending.set(id, (m) => m.error ? rej(new Error(method + ': ' + JSON.stringify(m.error))) : res(m.result));
  ws.send(JSON.stringify({ id, method, params, sessionId }));
});

const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
const S = sessionId;
await send('Page.enable', {}, S);
await send('Runtime.enable', {}, S);
const desktop = () => send('Emulation.setDeviceMetricsOverride', { width: 1366, height: 900, deviceScaleFactor: 1, mobile: false }, S);
const mobile = () => send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true }, S);
await desktop();

const evaluate = async (expr) => (await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }, S)).result?.value;
const waitFor = async (expr, timeout = 15000) => { const t0 = Date.now(); while (Date.now() - t0 < timeout) { if (await evaluate(expr)) return true; await sleep(300); } return false; };
const nav = async (path) => {
  await send('Page.navigate', { url: BASE + path }, S);
  await sleep(1500);
  await waitFor(`!!document.querySelector('ion-card-title, .parc-plan, table')`);
  await sleep(2500);
};
const click = async (expr, wait = 2000) => { const ok = await evaluate(`(() => { const el = ${expr}; if (el) { el.click(); return true; } return false; })()`); await sleep(wait); return ok; };
const shot = async (name, fullPage = false) => {
  const params = { format: 'png' };
  if (fullPage) {
    const h = await evaluate(`Math.max(document.documentElement.scrollHeight, document.querySelector('ion-content')?.shadowRoot?.querySelector('.inner-scroll')?.scrollHeight || 0)`);
    params.captureBeyondViewport = true;
  }
  const { data } = await send('Page.captureScreenshot', params, S);
  const file = `${OUT}/${name}.png`;
  writeFileSync(file, Buffer.from(data, 'base64'));
  console.log('saved', name);
};
const firstButton = (label) => `[...document.querySelectorAll('ion-button')].find(b => b.textContent.trim().startsWith('${label}'))`;

try {
  await nav('/home'); await shot('01-tableau-de-bord');
  await click(`document.querySelector('ion-menu-button')`, 1500); await shot('02-menu-lateral');
  await click(`document.querySelector('ion-menu ion-list ion-item')`, 500);

  await nav('/parc'); await click(`document.querySelector('ion-router-outlet ion-list ion-item')`, 1500); await shot('03-parc-machines-plan');
  await click(`document.querySelector('.parc-room')`, 1500); await shot('04-parc-filtre-salle');
  await click(firstButton('Toutes les machines'), 1500);
  await click(`document.querySelector('ion-router-outlet ion-list ion-item')`, 1000);
  await click(firstButton('Modifier la machine'), 4000); await shot('05-fiche-machine');
  await click(`[...document.querySelectorAll('ion-router-outlet ion-item')].find(i => /achat/.test(i.textContent))`, 2500); await shot('06-fiche-machine-composant');
  await click(firstButton('Ajouter depuis le stock'), 2500); await shot('07-fiche-machine-stock');

  await nav('/lieux'); await click(`document.querySelector('.parc-room')`, 2000); await shot('08-gestion-lieux');
  await nav('/modeles-gestion'); await click(`document.querySelector('.parc-table tbody tr')`, 2000); await shot('09-gestion-modeles');
  await nav('/utilisateurs-gestion'); await click(`document.querySelector('.parc-table tbody tr')`, 2000); await shot('10-gestion-utilisateurs');
  await nav('/rapports'); await shot('11-etats-machines');
  await click(firstButton('Composants par machine'), 3000); await shot('12-etats-composants-par-machine');

  const kit = [['emplacements', '13-lieux'], ['utilisateurs', '14-utilisateurs'], ['fournisseurs', '15-fournisseurs'], ['modeles', '16-modeles'], ['machines', '17-machines'], ['composants', '18-composants']];
  for (const [seg, name] of kit) { await nav('/' + seg); await click(`document.querySelector('ion-router-outlet ion-list ion-item')`, 2500); await shot(name); }

  await mobile();
  await nav('/home'); await shot('19-mobile-tableau-de-bord');
  await nav('/parc'); await shot('20-mobile-parc');
  await nav('/emplacements'); await shot('21-mobile-lieux');
} finally {
  chrome.kill();
}

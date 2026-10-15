import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const assets = new Map([
  ['/index.html', 'text/html; charset=utf-8'],
  ['/app.js', 'text/javascript; charset=utf-8'],
  ['/native.js', 'text/javascript; charset=utf-8'],
  ['/mobile.css', 'text/css; charset=utf-8'],
  ['/preview.html', 'text/html; charset=utf-8'],
  ['/preview.js', 'text/javascript; charset=utf-8'],
]);
const port = Number(process.env.AKADEMI_PORT || 4173);
const host = process.env.AKADEMI_HOST || '127.0.0.1';
if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('Geçersiz port.');
const root = new URL('../www/', import.meta.url);
const server = http.createServer(async (request, response) => {
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.writeHead(405, { Allow: 'GET, HEAD' }); response.end(); return;
  }
  let path;
  try { path = new URL(request.url, 'http://local.invalid').pathname; }
  catch { response.writeHead(400); response.end(); return; }
  if (path === '/') path = '/index.html';
  if (path === '/favicon.ico') { response.writeHead(204); response.end(); return; }
  const contentType = assets.get(path);
  if (!contentType) { response.writeHead(404); response.end('Bulunamadı.'); return; }
  try {
    const body = await readFile(new URL(path.slice(1), root));
    response.writeHead(200, { 'Content-Type': contentType, 'Content-Length': body.length,
      'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' });
    response.end(request.method === 'HEAD' ? undefined : body);
  } catch {
    response.writeHead(503, { 'Content-Type': 'text/plain; charset=utf-8' });
    response.end('Web dosyaları hazır değil. Önce npm run build çalıştırın.');
  }
});
server.on('error', (error) => { console.error('Web sunucusu başlatılamadı:', error.code); process.exitCode = 1; });
server.listen(port, host, () => console.log(`Akademi AI web sunucusu çalışıyor; port ${port}; klasör ${fileURLToPath(root)}`));
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => server.close());

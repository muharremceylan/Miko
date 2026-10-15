import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { build } from 'esbuild';
const source = new URL('../../../akademi_ai_prototip/index.html', import.meta.url);
const destination = new URL('../www/', import.meta.url);
const hash = content => createHash('sha256').update(content).digest('hex').slice(0, 12);
await mkdir(destination, { recursive: true });
let html = await readFile(source, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/);
if (!script) throw new Error('Prototip uygulama scripti bulunamadı.');
const apiUrl=process.env.AKADEMI_API_URL||'';
if(apiUrl){const parsed=new URL(apiUrl);if(parsed.username||parsed.password||parsed.search||parsed.hash||(parsed.protocol!=='https:'&&!(parsed.protocol==='http:'&&['127.0.0.1','localhost'].includes(parsed.hostname))))throw new Error('API adresi HTTPS olmalı.');}
const math = await build({ define: { __AKADEMI_API_URL__: JSON.stringify(apiUrl) }, entryPoints: [new URL('../src/math/index.js', import.meta.url).pathname], bundle: true, write: false, format: 'iife', target: 'es2022' });
const application = script[1] + '\n;' + math.outputFiles[0].text;
await writeFile(new URL('app.js', destination), application);
const notesFont = await readFile(new URL('../src/math/assets/akademi-notes.woff', import.meta.url));
const fontLicense = await readFile(new URL('../src/math/assets/OFL.txt', import.meta.url), 'utf8');
const fontCss = '/* Caveat subset: Akademi Notes. Source: google/fonts/ofl/caveat.\n' + fontLicense + '\n*/\n@font-face{font-family:AkademiNotes;src:url(data:font/woff;base64,' + notesFont.toString('base64') + ') format("woff");font-weight:600;font-style:normal;font-display:swap}\n';
const css = fontCss + (await readFile(new URL('../src/mobile.css', import.meta.url), 'utf8')) + '\n' + (await readFile(new URL('../src/math/math.css', import.meta.url), 'utf8'));
await writeFile(new URL('mobile.css', destination), css);
await build({ entryPoints: [new URL('../src/native.js', import.meta.url).pathname],
  bundle: true, outfile: new URL('native.js', destination).pathname, format: 'iife', target: 'es2022', minify: false });
const native = await readFile(new URL('native.js', destination));
html = html.replace(script[0], `<script src="app.js?v=${hash(application)}"></script><script src="native.js?v=${hash(native)}" defer></script>`);
html = html.replace('</head>', `<link rel="stylesheet" href="mobile.css?v=${hash(css)}"></head>`);
await writeFile(new URL('index.html', destination), html);
const previewScript = await readFile(new URL('../src/preview.js', import.meta.url));
await writeFile(new URL('preview.js', destination), previewScript);
let preview = await readFile(new URL('../src/preview.html', import.meta.url), 'utf8');
preview = preview.replaceAll('./index.html', `./index.html?v=${hash(html)}`)
  .replace('./preview.js', `./preview.js?v=${hash(previewScript)}`);
await writeFile(new URL('preview.html', destination), preview);
console.log('Web uygulaması ve mobil önizleme hazır; varlıklar içerik kimlikleriyle yenilenir.');

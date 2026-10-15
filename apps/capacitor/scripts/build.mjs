import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { build } from 'esbuild';
const source = new URL('../../../akademi_ai_prototip/index.html', import.meta.url);
const destination = new URL('../www/', import.meta.url);
await mkdir(destination, { recursive: true });
let html = await readFile(source, 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/);
if (!script) throw new Error('Prototip uygulama scripti bulunamadı.');
await writeFile(new URL('app.js', destination), script[1]);
html = html.replace(script[0], '<script src="app.js"></script><script src="native.js" defer></script>');
html = html.replace('</head>', '<link rel="stylesheet" href="mobile.css"></head>');
await writeFile(new URL('index.html', destination), html);
await writeFile(new URL('mobile.css', destination), await readFile(new URL('../src/mobile.css', import.meta.url)));
await build({ entryPoints: [new URL('../src/native.js', import.meta.url).pathname],
  bundle: true, outfile: new URL('native.js', destination).pathname, format: 'iife', target: 'es2022', minify: false });
for (const name of ['preview.html', 'preview.js']) {
  await writeFile(new URL(name, destination), await readFile(new URL('../src/' + name, import.meta.url)));
}
console.log('Web uygulaması ve mobil önizleme hazır; özgün HTML değiştirilmedi.');

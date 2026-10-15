import { readFile, mkdir, writeFile, copyFile } from 'node:fs/promises';
const root = new URL('../www/', import.meta.url);
const output = new URL('../web-release/', import.meta.url);
await mkdir(output, { recursive: true });
for (const name of ['index.html', 'app.js', 'native.js', 'mobile.css', 'preview.html', 'preview.js']) {
  await copyFile(new URL(name, root), new URL(name, output));
}
let standalone = await readFile(new URL('index.html', root), 'utf8');
for (const name of ['app.js', 'native.js']) {
  const code = (await readFile(new URL(name, root), 'utf8')).replace(/<\/script/gi, '<\\/script');
  standalone = standalone.replace(new RegExp(`<script src="${name.replace('.', '\\.')}"(?: defer)?><\\/script>`), () => `<script>${code}</script>`);
}
const css = await readFile(new URL('mobile.css', root), 'utf8');
standalone = standalone.replace('<link rel="stylesheet" href="mobile.css">', () => `<style>${css}</style>`);
await writeFile(new URL('standalone.html', output), standalone);
// A published site opens in phone-preview mode. The actual app remains a
// separate page so the iframe never embeds the preview recursively.
const preview = (await readFile(new URL('preview.html', root), 'utf8')).replaceAll('./index.html', './app.html');
await copyFile(new URL('index.html', root), new URL('app.html', output));
await writeFile(new URL('index.html', output), preview);
await writeFile(new URL('preview.html', output), preview);
await writeFile(new URL('.nojekyll', output), '');
console.log('Statik web yayını ve tek dosyalık tarayıcı sürümü web-release/ altında hazır.');

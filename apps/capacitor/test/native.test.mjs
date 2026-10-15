import { test } from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { build } from 'esbuild';

const compiled = await build({ entryPoints: ['src/native.js'], bundle: true, write: false, format: 'iife',
  plugins: [{ name: 'device-boundary', setup(builder) {
    builder.onResolve({ filter: /^@capacitor/ }, args => ({ path: args.path, namespace: 'mock' }));
    builder.onLoad({ filter: /.*/, namespace: 'mock' }, ({ path }) => {
      const names = path === '@capacitor/core' ? ['Capacitor', 'SystemBars', 'SystemBarsStyle', 'SystemBarType'] : path === '@capacitor/app' ? ['App'] :
        path === '@capacitor/camera' ? ['Camera', 'CameraResultType', 'CameraSource'] : ['TextToSpeech'];
      return { contents: names.map(n => `export const ${n}=globalThis.nativeMocks.${n};`).join('\n') };
    });
  } }] });
const tick = () => new Promise(resolve => setImmediate(resolve));
async function device({ native = true } = {}) {
  const events = {}, labelEvents = {}, calls = { speak: [], photo: [], stop: 0, exit: 0, close: 0, load: [] };
  let active = 'home';
  const nodes = { speechStatus: { textContent: '' }, photoStatus: { textContent: '' }, audioSelect: { value: 'tarih' },
    lessonDetail: { style: { display: 'none' } } };
  const label = { setAttribute() {}, addEventListener: (k,v) => { labelEvents[k] = v; } };
  for (const id of ['home','lessons','audio','quiz']) nodes[id] = { classList: { contains: () => active === id } };
  const mocks = {
    SystemBars: { setStyle: async () => {} }, SystemBarsStyle: { Dark: 'DARK', Light: 'LIGHT' }, SystemBarType: { StatusBar: 'StatusBar', NavigationBar: 'NavigationBar' },
    Capacitor: { isNativePlatform: () => native, getPlatform: () => 'android' },
    App: { addListener: async (k,v) => { events[k] = v; return { remove() {} }; }, exitApp: async () => { calls.exit++; } },
    Camera: { getPhoto: async (o) => { calls.photo.push(o); return { webPath: 'https://localhost/_capacitor_file_/image.jpg', format: 'jpeg' }; } },
    CameraResultType: { Uri: 'uri' }, CameraSource: { Prompt: 'PROMPT' },
    TextToSpeech: { stop: async () => { calls.stop++; }, isLanguageSupported: async () => ({ supported: true }),
      speak: async (o) => { calls.speak.push(o); } }
  };
  const context = vm.createContext({ nativeMocks: mocks, console, File, Blob,
    document: { documentElement: { dataset: {} }, getElementById: (id) => nodes[id], querySelector: () => label },
    course: { tarih: { name: 'Tarih', short: '<p>Örnek özet</p>' } },
    DOMParser: class { parseFromString() { return { body: { textContent: 'Örnek özet' } }; } },
    fetch: async () => ({ ok: true, blob: async () => new Blob(['photo'], { type: 'image/jpeg' }) }),
    drawHome() {}, closeLesson() { calls.close++; nodes.lessonDetail.style.display = 'none'; },
    loadPhoto: (e) => calls.load.push(e), navTo: (tab) => { active = tab; },
    stopSpeech() {}, startSpeech() {}, confirm: () => true });
  context.window = context;
  vm.runInContext(compiled.outputFiles[0].text, context); await tick();
  return { context, nodes, events, labelEvents, mocks, calls };
}

test('web kullanımında native API çağrılmaz', async () => {
  const d = await device({ native: false }); assert.equal(Object.keys(d.events).length, 0); assert.equal(d.calls.stop, 0);
});
test('Türkçe cihaz sesi kullanılır ve konu metni aktarılır', async () => {
  const d = await device(); await d.context.startSpeech();
  assert.equal(d.calls.speak[0].lang, 'tr-TR'); assert.match(d.calls.speak[0].text, /Tarih.*Örnek özet/);
  assert.equal(d.nodes.speechStatus.textContent, 'Sesli tekrar tamamlandı.');
});
test('Türkçe ses yoksa üretilmiş gibi gösterilmez', async () => {
  const d = await device(); d.mocks.TextToSpeech.isLanguageSupported = async () => ({ supported: false });
  await d.context.startSpeech(); assert.equal(d.calls.speak.length, 0); assert.match(d.nodes.speechStatus.textContent, /Türkçe ses yok/);
});
test('ses başlatılırken ekran değişirse gecikmiş cevap oynatılmaz', async () => {
  const d = await device(); let resolve;
  d.mocks.TextToSpeech.isLanguageSupported = () => new Promise(r => { resolve = r; });
  const playing = d.context.startSpeech(); d.context.navTo('quiz'); resolve({ supported: true }); await playing;
  assert.equal(d.calls.speak.length, 0); assert.equal(d.nodes.speechStatus.textContent, 'Seslendirme durduruldu.');
});
test('arka plana geçiş cihaz sesini durdurur', async () => {
  const d = await device(); d.events.appStateChange({ isActive: false }); assert.equal(d.calls.stop, 1);
});
test('Android geri tuşu önce konu detayını, sonra ana ekranı açar', async () => {
  const d = await device(); d.context.navTo('lessons'); d.nodes.lessonDetail.style.display = 'block';
  d.events.backButton(); assert.equal(d.calls.close, 1); assert.equal(d.calls.exit, 0);
  d.events.backButton(); assert.equal(d.calls.exit, 0); d.events.backButton(); assert.equal(d.calls.exit, 1);
});
test('kamera/galeri sonucu mevcut görsel doğrulamasına gider', async () => {
  const d = await device(); d.labelEvents.click({ preventDefault() {} }); await tick();
  assert.equal(d.calls.photo[0].saveToGallery, false); assert.equal(d.calls.load.length, 1);
  assert.equal(d.calls.load[0].target.files[0].type, 'image/jpeg');
});
test('kamera izni reddi anlaşılır hata gösterir', async () => {
  const d = await device(); d.mocks.Camera.getPhoto = async () => { throw new Error('permission denied'); };
  d.labelEvents.click({ preventDefault() {} }); await tick(); assert.match(d.nodes.photoStatus.textContent, /iznini kontrol/);
});
test('fotoğraf seçimini iptal etmek izin hatası gibi sunulmaz', async () => {
  const d = await device(); d.mocks.Camera.getPhoto = async () => { throw new Error('User cancelled photos app'); };
  d.labelEvents.click({ preventDefault() {} }); await tick(); assert.equal(d.nodes.photoStatus.textContent, '');
});
test('Android etkinliği yeniden oluşunca kamera sonucu geri yüklenir', async () => {
  const d = await device();
  await d.events.appRestoredResult({ pluginId: 'Camera', methodName: 'getPhoto', success: true,
    data: { webPath: 'https://localhost/_capacitor_file_/restored.jpg', format: 'jpeg' } });
  assert.equal(d.calls.load.length, 1);
});
test('tamamlanmamış kamera dönüşü anlaşılır hata gösterir', async () => {
  const d = await device();
  await d.events.appRestoredResult({ pluginId: 'Camera', methodName: 'getPhoto', success: false });
  assert.match(d.nodes.photoStatus.textContent, /tamamlanamadı/); assert.equal(d.calls.load.length, 0);
});
test('hazırlık aşamasındaki sınavda cihaz seslendirmesi başlatılmaz', async () => {
  const d = await device(); d.context.isStudyReady = () => false;
  await d.context.startSpeech();
  assert.equal(d.calls.speak.length, 0);
});
test('Matematik konu geri dönüşü native çıkış veya eski ders kapatmayı tetiklemez',async()=>{
 const d=await device();let count=0;d.context.AcademiMath={back(){count++;return true;}};
 d.events.backButton();assert.equal(count,1);assert.equal(d.calls.exit,0);assert.equal(d.calls.close,0);
});

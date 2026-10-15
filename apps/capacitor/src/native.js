import { Capacitor, SystemBars, SystemBarsStyle, SystemBarType } from '@capacitor/core';
import { App } from '@capacitor/app';
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { TextToSpeech } from '@capacitor-community/text-to-speech';

async function initialize() {
  if (!Capacitor.isNativePlatform()) return;
  document.documentElement.dataset.native = Capacitor.getPlatform();
  SystemBars.setStyle({ style: SystemBarsStyle.Dark, bar: SystemBarType.StatusBar }).catch(() => {});
  SystemBars.setStyle({ style: SystemBarsStyle.Light, bar: SystemBarType.NavigationBar }).catch(() => {});
  let speechToken = 0;
  window.stopSpeech = function () {
    speechToken++;
    TextToSpeech.stop().catch(() => {});
    document.getElementById('speechStatus').textContent = 'Seslendirme durduruldu.';
  };
  window.startSpeech = async function () {
    window.stopSpeech();
    const token = speechToken;
    const status = document.getElementById('speechStatus');
    const id = document.getElementById('audioSelect').value;
    const data = course[id];
    const text = new DOMParser().parseFromString(data.short, 'text/html').body.textContent;
    try {
      const available = await TextToSpeech.isLanguageSupported({ lang: 'tr-TR' });
      if (token !== speechToken) return;
      if (!available.supported) {
        status.textContent = 'Cihazda Türkçe ses yok. Konunun kısa özetini Dersler ekranından okuyabilirsin.';
        return;
      }
      status.textContent = 'Sesli tekrar oynatılıyor...';
      await TextToSpeech.speak({ text: data.name + '. ' + text, lang: 'tr-TR', rate: 0.9, volume: 1, category: 'ambient' });
      if (token === speechToken) status.textContent = 'Sesli tekrar tamamlandı.';
    } catch {
      if (token === speechToken) status.textContent = 'Seslendirme kullanılamadı. Kısa özeti Dersler ekranından okuyabilirsin.';
    }
  };
  // navTo() in the original prototype checks browser speech support. Native
  // WebView may lack it, so the native wrapper always stops the plugin too.
  const navigate = window.navTo;
  window.navTo = function (tab) { if (tab !== 'audio') window.stopSpeech(); navigate(tab); };
  // Existing click listeners resolve navTo's global binding at click time.
  await App.addListener('appStateChange', ({ isActive }) => { if (!isActive) window.stopSpeech(); else drawHome(); });
  await App.addListener('backButton', () => {
    if (document.getElementById('lessons').classList.contains('active') && document.getElementById('lessonDetail').style.display !== 'none') {
      closeLesson();
    } else if (!document.getElementById('home').classList.contains('active')) {
      window.navTo('home');
    } else if (window.confirm('Uygulamadan çıkmak istiyor musun?')) {
      App.exitApp();
    }
  });
  const label = document.querySelector('label.upload');
  label.setAttribute('role', 'button');
  label.setAttribute('tabindex', '0');
  label.setAttribute('aria-label', 'Fotoğraf çek veya galeriden seç');
  let picking = false;
  const showPhoto = async (photo) => {
    if (!photo.webPath) throw new Error('missing-image');
    const response = await fetch(photo.webPath);
    if (!response.ok) throw new Error('missing-image');
    const blob = await response.blob();
    loadPhoto({ target: { files: [new File([blob], 'soru.' + photo.format, { type: blob.type || 'image/' + photo.format })], value: '' } });
  };
  await App.addListener('appRestoredResult', async (result) => {
    if (result.pluginId !== 'Camera' || result.methodName !== 'getPhoto') return;
    if (!result.success) {
      document.getElementById('photoStatus').textContent = 'Önceki fotoğraf işlemi tamamlanamadı. Yeniden görsel seçebilirsin.';
      return;
    }
    try { await showPhoto(result.data); window.navTo('camera'); }
    catch { document.getElementById('photoStatus').textContent = 'Önceki fotoğraf açılamadı. Yeniden görsel seçebilirsin.'; }
  });
  const pick = async () => {
    if (picking) return;
    picking = true;
    const status = document.getElementById('photoStatus');
    try {
      const photo = await Camera.getPhoto({ quality: 85, resultType: CameraResultType.Uri, source: CameraSource.Prompt,
        saveToGallery: false, width: 2048, height: 2048,
        promptLabelHeader: 'Soru görseli', promptLabelCancel: 'Vazgeç', promptLabelPhoto: 'Galeriden seç', promptLabelPicture: 'Fotoğraf çek' });
      await showPhoto(photo);
    } catch (error) {
      if (/cancel/i.test(String(error?.message))) return;
      status.textContent = 'Fotoğraf alınamadı. Kamera/galeri iznini kontrol edip yeniden dene.';
    } finally { picking = false; }
  };
  label.addEventListener('click', (event) => { event.preventDefault(); pick(); });
  label.addEventListener('keydown', (event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); pick(); } });
}
initialize().catch(() => {
  const el = document.getElementById('photoStatus');
  if (el) el.textContent = 'Cihaz araçları başlatılamadı. Ders ve soru ekranlarını kullanmaya devam edebilirsin.';
});

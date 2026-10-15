const selector = document.getElementById('device');
const button = document.getElementById('scaleToggle');
const phone = document.getElementById('phone');
const space = document.getElementById('deviceSpace');
const toolbar = document.getElementById('toolbar');
const stage = document.getElementById('stage');
let actualSize = false;
function resizePreview() {
  document.documentElement.style.setProperty('--toolbar-height', `${toolbar.offsetHeight}px`);
  const [width, height] = selector.value.split('x').map(Number);
  const scale = actualSize ? 1 : Math.max(0.1, Math.min(1, (stage.clientWidth - 32) / (width + 24), (stage.clientHeight - 85) / (height + 24)));
  phone.style.width = `${width}px`;
  phone.style.height = `${height}px`;
  phone.style.transform = `scale(${scale})`;
  space.style.width = `${(width + 24) * scale}px`;
  space.style.height = `${(height + 24) * scale}px`;
  document.getElementById('dimensions').textContent = `${width} × ${height} · %${Math.round(scale * 100)}`;
}
selector.addEventListener('change', resizePreview);
button.addEventListener('click', () => {
  actualSize = !actualSize;
  button.textContent = actualSize ? 'Ekrana sığdır' : '1:1 boyut';
  button.setAttribute('aria-pressed', String(actualSize));
  resizePreview();
});
window.addEventListener('resize', resizePreview);
new ResizeObserver(resizePreview).observe(toolbar);
resizePreview();

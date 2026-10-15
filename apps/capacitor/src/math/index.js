import audioSummaries from '../../../../akademi_ai_prototip/content/kpss/lisans/matematik/topics/temel-audio.json';
import { Capacitor } from '@capacitor/core';
import { TextToSpeech } from '@capacitor-community/text-to-speech';
import { DeviceSpeech } from './audio.js';
import { LearningServices, aiPanel, loginPanel } from './services.js';
import { lessonNotebook, summaryNotebook } from './notebook.js';
import lesson from '../../../../akademi_ai_prototip/content/kpss/lisans/matematik/topics/temel.json';
import { MathProgress, curriculum, nodes, tabs, eligibleQuestions, attemptSummary } from './engine.js';
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
const paragraphs = items => items.map(p => `<p>${esc(p)}</p>`).join('');
const labels = ['Konu Anlatımı','Kısa Özet','Formüller','Çözümlü Örnekler','Test Çöz','Sesli Dinle','Yapay Zekâya Sor'];
const original = { overview: window.renderSubjectOverview, close: window.closeLesson, open: window.openLesson,
  nav: window.navTo, drawHome: window.drawHome, drawAnalytics: window.drawAnalytics, examState:window.renderExamState, selectExam:window.selectExam, selectLevel:window.selectKpssLevel };
const store = new MathProgress({ getItem: k => window.localStorage.getItem(k), setItem: (k,v) => window.localStorage.setItem(k,v) });
let view = null;
function savedNotesStyle(){try{return localStorage.getItem('akademi_math_notes_style_v1')==='plain'?'plain':'notebook';}catch{return 'notebook';}}
const settings = { filter: 'all', mode: 'learn', summary: 'quick', notesStyle:savedNotesStyle(), rate:0.9 };
const ready = () => isStudyReady() && selectedExam === 'kpss' && selectedKpssLevel === 'lisans';
const contentReady = id => id === lesson.topicId && lesson.learningReady;
const serviceBase=typeof __AKADEMI_API_URL__==='string'?__AKADEMI_API_URL__:'';
const services=new LearningServices({base:window.AkademiConfig?.apiBase??serviceBase,onChange:()=>{if(view?.kind==='topic'&&['ai','audio'].includes(view.tab))renderTopic();}});
const deviceSpeech=new DeviceSpeech({environment:window,nativeTTS:Capacitor.isNativePlatform()?TextToSpeech:null,onChange:updateDeviceControls});
function stopLearningAudio(){deviceSpeech.stop(false);$('summaryAudioPlayer')?.pause();}
function ensureTopicServices(){
 if(view?.kind!=='topic')return;
 if(view.tab==='audio' && contentReady(view.id))deviceSpeech.detect();
 if(['ai','audio'].includes(view.tab) && services.state.status==='idle')services.check();
}
const screen = document.createElement('div'); screen.id = 'mathTopicScreen'; screen.hidden = true; screen.className = 'math-topic'; $('lessons').append(screen);
function notice() { const el = $(view?.kind === 'topic' ? 'mathTopicNotice' : 'mathSaveNotice'); if (el) { el.hidden = !store.notice; el.textContent = store.notice; } }
function status(id) {
  const topic = nodes.get(id);
  if (topic.children.length && topic.children.every(k => store.state.topics[k]?.completed)) return 'Tamamlandı';
  if (!contentReady(id)) return id === 'denklemler' ? 'Sınırlı örnek' : 'Hazırlanıyor';
  return store.state.topics[id]?.completed ? 'Tamamlandı' : store.state.topics[id] ? 'Devam ediyor' : 'Başlanmadı';
}
function checkpoint() {
  if (view?.kind === 'topic' && !view.menuOpened && ready() && contentReady(view.id)) store.touch(view.id, view.tab, window.scrollY);
}
function hide() { stopLearningAudio();services.cancel();checkpoint(); screen.hidden = true; view = null; }
function metrics() {
  const old = stats.topics.matematik ?? { solved: 0, correct: 0 }, current = store.stats();
  const solved = old.solved + current.solved, correct = old.correct + current.correct;
  return { solved, correct, rate: solved ? Math.round(100 * correct / solved) : null, old: old.solved };
}
function openHome() {
  if (!ready()) return;
  stopLearningAudio();checkpoint(); screen.hidden = true; view = { kind: 'home' }; original.overview('matematik');
  const p = store.progress(), m = metrics(), last = nodes.get(store.state.lastTopic), active = store.active();
  const intro = $('overviewBody').querySelector(':scope > p'); if (intro) intro.textContent = '17 ana konu · 22 alt konu · İlk içerik: Temel Kavramlar';
  const dashboard = document.createElement('div'); dashboard.className = 'math-dashboard';
  dashboard.innerHTML = `<div id="mathSaveNotice" class="note" role="status" hidden></div><div class="row"><b>Ders ilerlemen</b><b id="mathProgressPercent">%${p.percent}</b></div><div class="progress" role="progressbar" aria-label="Matematik konu tamamlama" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${p.percent}"><div style="width:${p.percent}%"></div></div><div class="math-metrics"><div><b id="mathCompleted">${p.complete}</b><span>Tamamlanan konu</span></div><div><b id="mathRemaining">${p.remaining}</b><span>Kalan konu</span></div><div><b id="mathSolved">${m.solved}</b><span>Çözülen soru</span></div><div><b id="mathAccuracy">${m.rate === null ? '—' : '%'+m.rate}</b><span>Cevap doğruluğu</span></div></div><p class="footnote">Tamamlama kendi işaretlemene dayanır; ${p.total} son düzey konu üzerinden hesaplanır. Başarı oranı ayrıca cevaplardan hesaplanır.${m.old ? ' Önceki '+m.old+' matematik demo cevabın toplama dahildir; ayrıntılı geçmiş yalnız yeni testlerde tutulur.' : ''}</p>${last ? `<div class="math-continue"><b>Son çalışılan: ${esc(last.title)}</b><button class="ghost full" data-math-action="resume" data-topic="${last.id}">Çalışmaya devam et →</button></div>` : '<p class="mini muted">Henüz konu çalışmadın. Temel Kavramlar ile başlayabilirsin.</p>'}${active ? `<div class="note"><b>Yarım kalan testin var</b><p>${esc(nodes.get(active.topicId).title)} · ${active.current+1} / ${active.questions.length} soru</p><button class="ghost full" data-math-action="resume-test">Teste devam et →</button></div>` : ''}<div class="line"></div>`;
  $('overviewBody').prepend(dashboard);
  $('mathTopicsPanel').innerHTML = `<p class="note mini">Temel Kavramlar özgün çalışma içeriği ve 30 soru içerir. Matematiksel kontroller yapıldı; uzman incelemesi bekleniyor. Diğer konular ders ders hazırlanacak.</p>` + curriculum.topics.filter(t => !t.parentId).map((t,i) => `<details class="topic-entry" data-math-topic="${t.id}" ${t.id === 'temel' || t.id === 'denklemler' ? 'open' : ''}><summary>${i+1}. ${esc(t.title)} <span class="math-status">${status(t.id)}</span></summary>${t.children.length ? `<ul>${t.children.map(id => `<li><button class="math-child" data-math-action="topic" data-topic="${id}">${esc(nodes.get(id).title)}</button></li>`).join('')}</ul>` : ''}<button class="ghost full" data-math-action="topic" data-topic="${t.id}">${t.children.length ? 'Ana konu ekranını aç' : 'Konuyu aç'} →</button>${t.id === 'denklemler' ? '<p class="mini muted">Önceki sınırlı denklem örneği korunuyor.</p><button class="back" id="mathExample" data-math-action="legacy-example">Birinci Dereceden Denklemler →</button>' : ''}</details>`).join('');
  notice();
}
function openTopic(id, requestedTab) {
  if (!ready() || !nodes.has(id)) return;
  stopLearningAudio();checkpoint();services.context(id);
  $('lessonList').style.display = 'none'; $('subjectOverview').hidden = true; $('lessonDetail').style.display = 'none'; screen.hidden = false;
  const tab = tabs.includes(requestedTab) ? requestedTab : store.state.topics[id]?.tab ?? 'lesson';
  view = { kind: 'topic', id, tab };
  const y = store.state.topics[id]?.scroll[tab] ?? 0;
  if (contentReady(id)) store.touch(id, tab, y);
  original.nav('lessons'); renderTopic(y);ensureTopicServices();
}
function solution(q) {
  return `<p><b>Doğru cevap: ${'ABCDE'[q.answer]}) ${esc(q.options[q.answer])}</b></p><ol>${q.steps.map(step => '<li>'+esc(step)+'</li>').join('')}</ol><p><b>Formül / kural:</b> ${esc(q.formula)}</p>${q.alternative ? '<p><b>Alternatif yöntem:</b> '+esc(q.alternative)+'</p>' : ''}`;
}
function topicBody() {
  const topic = nodes.get(view.id);
  if (!contentReady(view.id)) {
    if (view.tab === 'ai') return aiBody();
    return `<div class="note">${view.tab === 'audio' ? 'Sesli anlatım henüz hazırlanmadı.' : 'Bu bölümün içeriği hazırlanıyor.'}</div><p class="mini muted">${esc(topic.title)} için ${esc(labels[tabs.indexOf(view.tab)].toLowerCase())} ders ders eklenecek.</p>${topic.children.length ? '<div class="line"></div><b>Alt konular</b>'+topic.children.map(id => `<button class="math-topic-link" data-math-action="topic" data-topic="${id}">${esc(nodes.get(id).title)} <span class="arrow">›</span></button>`).join('') : ''}${view.id === 'denklemler' ? '<button class="ghost full" data-math-action="legacy-example">Mevcut Birinci Dereceden Denklemler örneğini aç →</button>' : ''}`;
  }
  switch (view.tab) {
    case 'lesson': return lessonNotebook(lesson,esc,settings.notesStyle)+`<div class="line"></div><p class="mini">Tamamlama bir öz bildirimdir; test başarısı ayrıca hesaplanır.</p><button class="cta full" data-math-action="complete">${store.state.topics[view.id]?.completed ? 'Tamamlandı işaretini kaldır' : 'Konuyu tamamladım ✓'}</button>`;
    case 'summary': return `<label class="mini" for="mathSummaryLevel">Özet uzunluğu</label><select id="mathSummaryLevel" data-math-change="summary"><option value="quick" ${settings.summary==='quick'?'selected':''}>1 dakikalık hızlı tekrar</option><option value="standard" ${settings.summary==='standard'?'selected':''}>5 dakikalık standart özet</option><option value="detailed" ${settings.summary==='detailed'?'selected':''}>Ayrıntılı tekrar notları</option></select><p class="footnote">Süreler yaklaşık okuma hedefidir; kişiye göre değişir.</p>${summaryNotebook(lesson,settings.summary,esc,settings.notesStyle)}<button class="ghost full" data-math-action="tab" data-math-tab="formulas">Formüllere ve kurallara geç →</button>`;
    case 'formulas': return lesson.formulas.map(f => `<div class="math-formula"><h3>${esc(f.name)}</h3><div class="math-expression">${esc(f.expression)}</div><p><b>Koşul:</b> ${esc(f.conditions)}</p><p><b>Örnek:</b> ${esc(f.example)}</p></div>`).join('');
    case 'examples': return `<p class="mini muted">Örnekler test sorularından ayrıdır. Kolaydan zora ilerle; çözümü açmadan önce kendin dene.</p>`+lesson.examples.map(q => `<article class="math-example"><span class="chip">${esc(q.difficulty)} · ${esc(q.skill)}</span><p><b>${esc(q.text)}</b></p><ol type="A">${q.options.map(o => '<li>'+esc(o)+'</li>').join('')}</ol><details><summary>Adım adım çözümü göster</summary>${solution(q)}</details></article>`).join('');
    case 'test': return testBody();
    case 'audio': return audioBody();
    case 'ai': return aiBody();
  }
}
function aiBody() { return aiPanel(services,esc); }
function audioBody(){
 const state=deviceSpeech.state,s=services.state;
 let server='';
 if(s.status==='ready'&&s.capabilities.speech_ready){
   server='<h4>AI ses kaydı</h4>'+(services.token?`<p class="mini">Seçilen özetten gerçek bir ses dosyası oluşturulur. Üretilen ses yapay zekâ sesidir.</p>${s.error?'<p class="note">'+esc(s.error)+'</p>':''}<button class="ghost full" data-math-action="server-speech" ${s.audioBusy?'disabled':''}>${s.audioBusy?'Ses oluşturuluyor…':'Bu özeti ses dosyasına dönüştür'}</button>${s.audioUrl&&s.audioLevel===settings.summary?`<audio id="summaryAudioPlayer" controls preload="metadata" src="${esc(s.audioUrl)}"></audio><label for="summaryAudioRate">Kayıt hızı</label><select id="summaryAudioRate"><option value="0.75">0,75×</option><option value="1" selected>1×</option><option value="1.25">1,25×</option><option value="1.5">1,5×</option></select><p class="footnote">Oynat/duraklat ve sarma gerçek ses dosyasının oynatıcısındadır. Arka planda oynatma tarayıcı ve cihaz desteğine bağlıdır.</p>`:''}`:loginPanel(services,esc));
 }else server='<p class="service-note mini">Kaydedilmiş sesli özet henüz hazırlanmadı. Gerçek ses dosyası için sunucu bağlantısı gerekiyor; cihaz sesi bunun için bir alternatif.</p>';
 return `<label for="audioSummaryLevel">Dinlenecek özet</label><select id="audioSummaryLevel" data-math-change="audio-summary"><option value="quick" ${settings.summary==='quick'?'selected':''}>1 dakikalık hızlı tekrar</option><option value="standard" ${settings.summary==='standard'?'selected':''}>5 dakikalık standart özet</option><option value="detailed" ${settings.summary==='detailed'?'selected':''}>Ayrıntılı tekrar notları</option></select><div class="device-speech-card"><h4>Cihaz sesiyle dinle</h4><p id="deviceSpeechStatus" role="status">${esc(state.message)}</p><div id="deviceSpeechControls" ${!state.available?'hidden':''}><label for="deviceSpeechRate">Okuma hızı</label><select id="deviceSpeechRate" data-math-change="speech-rate" ${state.playing?'disabled':''}>${[0.75,0.9,1,1.25].map(n=>`<option value="${n}" ${settings.rate===n?'selected':''}>${n.toString().replace('.',',')}×</option>`).join('')}</select><div class="speech-buttons"><button class="cta" id="deviceSpeechPlay" data-math-action="device-play" ${state.playing?'hidden':''}>▶ Dinle</button><button class="ghost" id="deviceSpeechPause" data-math-action="device-pause" ${!state.canPause||!state.playing||state.paused?'hidden':''}>Ⅱ Duraklat</button><button class="cta" id="deviceSpeechResume" data-math-action="device-resume" ${!state.paused?'hidden':''}>▶ Devam et</button><button class="ghost" id="deviceSpeechStop" data-math-action="device-stop" ${!state.playing?'hidden':''}>■ Durdur</button></div><label for="deviceSpeechProgress">Metin okuma ilerlemesi</label><progress id="deviceSpeechProgress" max="100" value="${state.progress}"></progress><p class="footnote">Bu bir podcast kaydı değildir. İlerleme, ses motorunun bildirdiği okuma konumuna dayanır; süre ve sarma gösterilmez.${!state.canPause?' Bu cihaz motoru duraklatmayı desteklemiyor; durdurup yeniden başlatabilirsin.':''}</p></div></div>${server}<h3>Temel Kavramlar — seslendirme metni</h3>${paragraphs(audioSummaries.summaries[settings.summary].split('\n\n'))}`;
}
function updateDeviceControls(){
 if(view?.kind!=='topic'||view.tab!=='audio')return;
 const state=deviceSpeech.state;
 if($('deviceSpeechStatus'))$('deviceSpeechStatus').textContent=state.message;
 if($('deviceSpeechControls'))$('deviceSpeechControls').hidden=!state.available;
 for(const [id,hidden] of [['deviceSpeechPlay',state.playing],['deviceSpeechPause',!state.canPause||!state.playing||state.paused],['deviceSpeechResume',!state.paused],['deviceSpeechStop',!state.playing]])if($(id))$(id).hidden=hidden;
 if($('deviceSpeechRate'))$('deviceSpeechRate').disabled=state.playing;
 if($('deviceSpeechProgress'))$('deviceSpeechProgress').value=state.progress;
}
function duration(ms) { const total = Math.floor(ms / 1000); return Math.floor(total/60)+' dk '+total%60+' sn'; }
function testBody() {
  const active = store.active();
  if (active) {
    if (active.topicId !== view.id) return `<div class="note">${esc(nodes.get(active.topicId).title)} için devam eden bir testin var. Önce bu testi tamamla.</div><button class="ghost full" data-math-action="resume-test">Teste dön →</button>`;
    const q = active.questions[active.current], answer = active.answers[active.current], revealed = answer !== null && active.mode === 'learn';
    return `<div id="mathTestQuestion"><div class="row"><span class="chip">${esc(q.difficulty)}</span><span class="mini">Soru ${active.current+1} / ${active.questions.length}</span></div><p class="footnote">${active.mode==='learn' ? 'Öğrenme modu · Açıklama cevaptan sonra' : 'Değerlendirme modu · Çözümler test sonunda'}</p><p class="question-card">${esc(q.text)}</p><div id="mathAnswers">${q.options.map((option,i) => `<button class="answer ${revealed && i===q.answer ? 'correct' : revealed && answer.choice===i ? 'wrong' : answer?.choice===i ? 'math-selected' : ''}" data-math-action="answer" data-choice="${i}" ${answer !== null ? 'disabled' : ''}><b>${'ABCDE'[i]})</b> ${esc(option)}</button>`).join('')}</div>${answer !== null ? `<div class="note" role="status">${answer.choice===null ? 'Bu soru boş bırakıldı.' : revealed ? (answer.choice===q.answer ? 'Doğru cevap.' : 'Cevabını birlikte inceleyelim.') : 'Cevabın kaydedildi. Çözüm test sonunda gösterilecek.'}</div>${revealed ? solution(q) : ''}<button class="cta full" data-math-action="next">${active.current+1===active.questions.length ? 'Test sonucunu gör →' : 'Sonraki soru →'}</button>` : '<button class="ghost full" data-math-action="skip">Boş bırak ve ilerle →</button>'}<button class="back full" data-math-action="finish">Testi şimdi bitir</button><p class="footnote">Cevaplar bu cihazda kaydedilir. Ayrılırsan Matematik ana sayfasından teste dönebilirsin.</p></div>`;
  }
  const pool = eligibleQuestions(view.id, settings.filter, store.state.attempts), recent = store.state.attempts.filter(a => a.topicId===view.id && a.finishedAt).at(-1);
  return `<div id="mathTestSettings"><label for="mathTestFilter">Soru havuzu</label><select id="mathTestFilter" data-math-change="filter"><option value="all" ${settings.filter==='all'?'selected':''}>Tüm sorular</option><option value="wrong" ${settings.filter==='wrong'?'selected':''}>Yalnızca yanlış yapılanlar</option><option value="unseen" ${settings.filter==='unseen'?'selected':''}>Daha önce çözülmemişler</option></select><label for="mathTestMode">Çözüm gösterimi</label><select id="mathTestMode" data-math-change="mode"><option value="learn" ${settings.mode==='learn'?'selected':''}>Öğrenme · Anında açıklama</option><option value="assessment" ${settings.mode==='assessment'?'selected':''}>Değerlendirme · Test sonunda</option></select><p class="note" id="mathPoolCount">Bu filtrede ${pool.length} uygun soru var.${!pool.length ? ' Başka bir havuz seçebilirsin.' : ''}</p><div class="math-test-sizes">${[10,20,30].map(n => `<button class="ghost" data-math-action="start" data-count="${n}" ${pool.length<n ? 'disabled' : ''}>${n} soru<br><small>${n===10?'Hızlı':n===20?'Standart':'Kapsamlı'}</small></button>`).join('')}</div>${pool.length>0 && pool.length<10 ? `<button class="ghost full" data-math-action="start" data-count="${pool.length}">Mevcut ${pool.length} soruyla kısa test</button>` : ''}<button class="cta full" data-math-action="start" data-count="1" ${!pool.length ? 'disabled' : ''}>Rastgele bir soru çöz</button><p class="footnote">Sorular bir test içinde tekrarlanmaz. Yanlışlar son cevaba göre belirlenir; geçmiş denemeler korunur. Çözülmemişler, henüz cevap kaydı olmayan sorulardır.</p></div>${recent ? resultsBody(recent) : ''}`;
}
function resultsBody(a) {
  const s = attemptSummary(a), skills = new Map();
  a.questions.forEach((q,i) => { const skill = q.skill, v = skills.get(skill) ?? { solved:0,correct:0 }; const answer = a.answers[i]; if (answer && answer.choice !== null) { v.solved++; if (answer.choice===q.answer) v.correct++; } skills.set(skill,v); });
  return `<div class="line"></div><section id="mathTestResult" aria-labelledby="mathResultHeading"><h3 id="mathResultHeading">Test sonucu</h3><p class="note" id="mathResultSummary">${s.total} soruda ${s.correct} doğru, ${s.wrong} yanlış, ${s.blank} boş. Cevap doğruluğu: ${s.rate===null?'—':'%'+s.rate}.</p><p class="mini">Başlangıçtan bitişe geçen süre (aralar dahil): ${duration(s.elapsedMs)}.</p><h3>Kazanım bazlı sonuç</h3>${[...skills].map(([skill,v])=>`<div class="list-item mini"><b>${esc(skill)}</b><br>${v.correct} doğru / ${v.solved} cevap · ${v.solved ? '%'+Math.round(100*v.correct/v.solved) : 'Henüz cevap yok'}</div>`).join('')}<p class="mini muted">${s.wrong || s.blank ? 'Yanlış ve boş bıraktığın soruların çözümünü incele; ilgili kuralı anlatım ve formüllerden tekrar et.' : 'Bu testteki doğrularını yeni sorularla pekiştir.'} Az sayıda soru tüm konuya hâkim olduğunu kanıtlamaz.</p><button class="ghost full" data-math-action="review-wrong">Yanlışları tekrar çöz →</button><button class="back full" data-math-action="tab" data-math-tab="lesson">Konu anlatımına dön</button><h3>Sorular ve adım adım çözümler</h3>${a.questions.map((q,i)=>`<details class="math-review"><summary>${i+1}. ${esc(q.text)}</summary><p>Senin cevabın: ${a.answers[i]?.choice===null || !a.answers[i] ? 'Boş' : 'ABCDE'[a.answers[i].choice]+') '+esc(q.options[a.answers[i].choice])}</p>${solution(q)}</details>`).join('')}</section>`;
}
function renderTopic(y = window.scrollY, goToContent=false) {
  if (!view || view.kind !== 'topic') return;
  const topic = nodes.get(view.id);
  screen.innerHTML = `<button class="back" data-math-action="home">← Matematik ana sayfası</button><div class="card"><div class="small-label">KPSS LİSANS · MATEMATİK</div><h1 class="t" id="mathTopicTitle">${esc(topic.title)}</h1><p class="mini muted">${status(view.id)}</p>${contentReady(view.id) ? '<p class="footnote">Çalışma taslağı · Uzman incelemesi bekleniyor.</p>' : ''}<div id="mathTopicNotice" class="note" role="status" hidden></div><div class="math-topic-tabs" role="tablist" aria-label="Konu bölümleri">${tabs.map((tab,i)=>`<button type="button" role="tab" class="pill ${view.tab===tab?'active':''}" id="math-tab-${tab}" aria-selected="${view.tab===tab}" aria-controls="mathTopicPanel" tabindex="${view.tab===tab?0:-1}" data-math-action="tab" data-math-tab="${tab}">${['📖','⚡','∑','✎','✓','♫','✦'][i]} <span>${labels[i]}</span></button>`).join('')}</div><button class="math-menu-jump" data-math-action="section-menu">${labels[tabs.indexOf(view.tab)]}<span>Bölümler ↑</span></button><div id="mathTopicPanel" class="article" role="tabpanel" aria-labelledby="math-tab-${view.tab}">${topicBody()}</div></div>`;
  notice();
  requestAnimationFrame(() => {const panel=$('mathTopicPanel');const jump=screen.querySelector('.math-menu-jump');const top=goToContent&&panel?window.scrollY+panel.getBoundingClientRect().top-(jump?.offsetHeight??0)-10:y;window.scrollTo(0,Math.max(0,top));});
}
function selectTab(tab, goToContent=true) {
  if (!tabs.includes(tab) || view?.kind !== 'topic') return;
  if(view.tab!==tab)stopLearningAudio();
  checkpoint(); view.tab = tab;view.menuOpened=false;
  const y = store.state.topics[view.id]?.scroll[tab] ?? 0;
  if (contentReady(view.id)) store.touch(view.id, tab, y);
  renderTopic(y,goToContent&&y===0);ensureTopicServices();
}
function refreshStats() { window.drawHome(); if ($('analytics').classList.contains('active')) window.drawAnalytics(); }
function action(event) {
  const target = event.target.closest('[data-math-action]'); if (!target || !ready() || target.disabled) return;
  const a = target.dataset.mathAction;
  if (a === 'topic' || a === 'resume') return openTopic(target.dataset.topic);
  if (a === 'home') return openHome();
  if (a === 'legacy-example') { hide(); return original.open('matematik',true); }
  if (a === 'resume-test') { const active=store.active(); if (active) openTopic(active.topicId,'test'); return; }
  if (view?.kind !== 'topic') return;
  if(a==='device-play'){window.stopSpeech();deviceSpeech.play(audioSummaries.summaries[settings.summary],settings.rate);return;}
  if(a==='device-pause'){deviceSpeech.pause();return;} if(a==='device-resume'){deviceSpeech.resume();return;} if(a==='device-stop'){deviceSpeech.stop();return;}
  if(a==='service-check'){services.check();return;}
  if(a==='service-login'){const code=$('aiAccessCode')?.value??'';if($('aiAccessCode'))$('aiAccessCode').value='';services.login(code);return;}
  if(a==='ai-solve'){services.state.question=$('aiQuestion')?.value??services.state.question;if(!services.state.question.trim()&&!services.state.image){services.state.error='Bir soru yaz veya fotoğraf ekle.';renderTopic();return;}services.solve(view.id);return;}
  if(a==='ai-cancel'){services.cancel();return;}
  if(a==='ai-clear-image'){services.state.image=null;renderTopic();return;}
  if(a==='server-speech'){stopLearningAudio();services.speech(view.id,settings.summary);return;}

  if(a==='section-menu'){checkpoint();view.menuOpened=true;screen.querySelector('.math-topic-tabs').scrollIntoView({block:'start'});$('math-tab-'+view.tab).focus({preventScroll:true});return;}
  if(a==='note-style' && ['notebook','plain'].includes(target.dataset.style)){settings.notesStyle=target.dataset.style;try{localStorage.setItem('akademi_math_notes_style_v1',settings.notesStyle);}catch{store.notice='Görünüm tercihi kaydedilemedi; bu oturumda kullanılabilir.';}renderTopic();return;}
  if (a === 'tab') return selectTab(target.dataset.mathTab);
  if (a === 'complete') { store.complete(view.id,!store.state.topics[view.id]?.completed); return renderTopic(); }
  if (a === 'review-wrong') { settings.filter='wrong'; renderTopic(); $('mathTestSettings').scrollIntoView({block:'start'}); return; }
  if (a === 'start') { try { store.start(view.id,settings.filter,Number(target.dataset.count),settings.mode); renderTopic(0,true); } catch { store.notice='Test başlatılamadı. Soru havuzunu kontrol edip tekrar dene.'; notice(); } return; }
  if (a === 'answer') { if (store.answer(Number(target.dataset.choice))) { renderTopic(); refreshStats(); } return; }
  if (a === 'skip') { if (store.answer(null)) { store.next(); renderTopic(0,true); } return; }
  if (a === 'next') { store.next(); renderTopic(0,true); return; }
  if (a === 'finish' && window.confirm('Testi bitirmek istiyor musun? Cevaplanmamış sorular boş sayılacak.')) { store.finish(); renderTopic(0,true); }
}
$('lessons').addEventListener('click',action);
$('lessons').addEventListener('change', event => {
  if (!ready() || view?.kind!=='topic') return;
  if(event.target.id==='summaryAudioRate'){if($('summaryAudioPlayer'))$('summaryAudioPlayer').playbackRate=Number(event.target.value);return;}
  if(event.target.id==='aiQuestionImage'){
    const file=event.target.files?.[0];if(!file)return;
    if(!['image/png','image/jpeg','image/webp'].includes(file.type)||file.size>4*1024*1024){services.state.error='En fazla 4 MB PNG, JPEG veya WebP seç.';renderTopic();return;}
    const topicId=view.id;const reader=new FileReader();reader.onload=()=>{if(view?.id===topicId){services.state.image=String(reader.result);services.state.error='';renderTopic();}};reader.onerror=()=>{services.state.error='Görsel açılamadı.';renderTopic();};reader.readAsDataURL(file);return;
  }
  const key=event.target.dataset.mathChange, value=event.target.value;
  if(key==='speech-rate'&&[0.75,0.9,1,1.25].includes(Number(value))){settings.rate=Number(value);return;}
  if(key==='audio-summary'&&['quick','standard','detailed'].includes(value)){stopLearningAudio();settings.summary=value;renderTopic();return;}

  const allowed={filter:['all','wrong','unseen'],mode:['learn','assessment'],summary:['quick','standard','detailed']};
  if (allowed[key]?.includes(value)) { settings[key]=value; renderTopic(); }
});
screen.addEventListener('input',event=>{if(event.target.id==='aiQuestion')services.state.question=event.target.value;});
screen.addEventListener('keydown',event=>{
  const button=event.target.closest('[role="tab"]'); if (!button) return;
  const current=tabs.indexOf(button.dataset.mathTab); let next=current;
  if (event.key==='ArrowRight') next=(current+1)%tabs.length;
  else if (event.key==='ArrowLeft') next=(current+tabs.length-1)%tabs.length;
  else if(event.key==='ArrowDown') next=Math.min(current+2,tabs.length-1);
  else if(event.key==='ArrowUp') next=Math.max(current-2,0);
  else if (event.key==='Home') next=0; else if(event.key==='End') next=tabs.length-1; else return;
  event.preventDefault(); selectTab(tabs[next],false); $('math-tab-'+tabs[next]).focus({preventScroll:true});
});
window.renderExamState = function(){original.examState();if(ready())$('examStatusDescription').textContent='6 ders alanı: Temel Kavramlar anlatımı, üç özet seviyesi ve 30 yeni matematik sorusu. Önceki dört örnek konu ve 10 demo soru korunur. Geometri ve Güncel Bilgiler içerikleri hazırlanıyor.';};
window.renderSubjectOverview = function(topic) { if (topic==='matematik' && ready()) return openHome(); hide(); return original.overview(topic); };
window.openLesson = function(topic,example=false) { if(topic==='matematik' && ready() && !example) return openHome(); hide(); return original.open(topic,example); };
window.selectExam = function(id) { stopLearningAudio();services.cancel();checkpoint(); return original.selectExam(id); };
window.selectKpssLevel = function(id) { stopLearningAudio();services.cancel();checkpoint(); return original.selectLevel(id); };
window.closeLesson = function() { hide(); original.close(); };
window.navTo = function(tab) { if(tab!=='lessons'){stopLearningAudio();services.cancel();checkpoint();} return original.nav(tab); };
window.drawHome = function() {
  original.drawHome(); if (!ready()) return;
  const added=store.stats(todayKey()), day=dailyStats(), solved=day.solved+added.solved,correct=day.correct+added.correct;
  $('qCount').textContent=solved; $('correctCount').textContent=correct; $('rate').textContent=solved?Math.round(100*correct/solved)+'%':'—';
  $('homeProgress').style.width=Math.min(100,solved/10*100)+'%'; $('successTag').textContent=solved>=10?'Hedef tamamlandı ✓':`${solved} / 10 soru`;
  if(view?.kind==='home' && $('mathSolved')){const math=metrics();$('mathSolved').textContent=math.solved;$('mathAccuracy').textContent=math.rate===null?'—':'%'+math.rate;}
};
window.drawAnalytics = function() {
  original.drawAnalytics(); if(!ready()) return;
  const added=store.stats(),solved=stats.solved+added.solved,correct=stats.correct+added.correct;
  $('aCount').textContent=solved; $('aCorrect').textContent=correct; $('aWrong').textContent=solved-correct; $('aProgress').style.width=(solved?100*correct/solved:0)+'%';
  const math=metrics();
  if(added.solved){
    const weak=studyCourses().map(([id,v])=>{const old=stats.topics[id]??{solved:0,correct:0};return {name:v.name.split(' · ')[0],solved:old.solved+(id==='matematik'?added.solved:0),correct:old.correct+(id==='matematik'?added.correct:0)};}).filter(v=>v.solved).sort((a,b)=>a.correct/a.solved-b.correct/b.solved)[0];
    $('personalTip').textContent=weak.name+' dersindeki cevaplarını inceleyip ilgili anlatım ve örnekleri tekrar edebilirsin. Bu öneri mevcut cevap geçmişine dayanır.';
  }
  for (const row of $('topicStats').children) if (row.textContent.includes('Matematik')) { row.querySelector('b').textContent=math.rate===null?'Henüz veri yok':math.rate+'%'; row.querySelector('.progress>div').style.width=(math.rate??0)+'%'; }
};
window.AcademiMath = {
  open:openHome, openTopic,
  back() { if(!ready() || !$('lessons').classList.contains('active')) return false; if(view?.kind==='topic'){openHome();return true;} if(view?.kind==='home'){window.closeLesson();return true;} return false; },
  resetAttempts() { if(ready()){store.clearAttempts();refreshStats();} }
};
window.addEventListener('pagehide',()=>{stopLearningAudio();services.cancel();checkpoint();});
document.addEventListener('visibilitychange',()=>{if(document.hidden){deviceSpeech.stop(false);checkpoint();}});
window.drawHome();
window.renderExamState();

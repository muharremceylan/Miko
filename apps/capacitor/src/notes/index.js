import library from '../../../../akademi_ai_prototip/content/pdf-notes/library.json' with {type:'json'};
import {lessonNotebook,summaryNotebook} from '../math/notebook.js';
export const noteLibrary=library;
const names={turkce:'Türkçe',tarih:'Tarih',vatandaslik:'Vatandaşlık',cografya:'Coğrafya'};
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const noteActions=html=>html.replaceAll('data-math-action=','data-notes-action=');
export function initializePDFNotes(){
 const $=id=>document.getElementById(id);
 const prior={close:window.closeLesson,open:window.openLesson,nav:window.navTo,exam:window.renderExamState,back:window.AcademiMath.back};
 const ready=()=>isStudyReady()&&selectedExam==='kpss'&&selectedKpssLevel==='lisans';
 let view=null,style='notebook',level='quick';
 try{style=localStorage.getItem('akademi_pdf_notes_style_v1')==='plain'?'plain':'notebook';}catch{}
 const screen=document.createElement('div');screen.id='pdfNotesScreen';screen.hidden=true;screen.className='math-topic';$('lessons').append(screen);
 const entries=[];
 for(const parent of [$('lessonList'),$('home').querySelector('[data-study-content]')]){
  const card=document.createElement('div');card.className='card';card.hidden=!ready();
  card.innerHTML='<div class="small-label">DERS NOTLARIN</div><b>Türkçe ve Tarih PDF notları</b><p class="mini muted">Paylaştığın notlardan hazırlanan ilk renkli çalışma taslakları ve kaynak durumları.</p><button class="ghost full" data-notes-action="library">PDF ders notlarını aç →</button>';
  parent.append(card);entries.push(card);
 }
 function close(){screen.hidden=true;view=null;}
 function openLibrary(){
  if(!ready())return;
  window.closeLesson();$('lessonList').style.display='none';$('subjectOverview').hidden=true;$('lessonDetail').style.display='none';screen.hidden=false;view={kind:'library'};
  screen.innerHTML=`<button class="back" data-notes-action="close">← Tüm dersler</button><section class="card"><div class="small-label">KPSS LİSANS · KAYNAK NOTLARI</div><h1 id="pdfNotesTitle">PDF ders notların</h1><p>Türkçe ve Tarih taramalarında toplam 373 sayfa var. Arama için OCR çıkarıldı; bütün sayfalar içerik doğrulamasından geçmiş değildir.</p><p class="note">İlk iki konu, görsel olarak kontrol edilen sayfalardan yeniden yazılmış çalışma taslaklarıdır. Uzman incelemesi bekleniyor.</p>${library.sources.map(source=>{const lessons=library.lessons.filter(l=>l.sourceRefs.some(r=>r.sourceId===source.id));return `<article class="math-source" data-pdf-source="${source.id}"><h3>${names[source.subject]}</h3><p class="mini">${esc(source.fileName)}</p>${source.pageCount?`<p>${source.pageCount} sayfa · El yazısı tarama</p><p class="footnote">OCR arama taslağı hazır. Konu ve doğruluk kontrolü sayfa sayfa ilerleyecek.</p>`:'<p class="note">Dosya aktarım sınırı nedeniyle henüz açılamadı. İnceleme için 32 MiB’den küçük PDF parçaları gerekiyor.</p>'}${lessons.map(l=>`<button class="ghost full" data-notes-action="topic" data-note-id="${l.id}">${esc(l.title)} →</button>`).join('')}</article>`;}).join('')}</section>`;
  prior.nav('lessons');window.scrollTo(0,0);
 }
 function openTopic(id,tab='lesson'){
  if(!ready()||!library.lessons.some(l=>l.id===id))return;
  window.closeLesson();$('lessonList').style.display='none';$('subjectOverview').hidden=true;$('lessonDetail').style.display='none';screen.hidden=false;view={kind:'topic',id,tab};render();prior.nav('lessons');window.scrollTo(0,0);
 }
 function render(){
  if(view?.kind!=='topic')return;
  const lesson=library.lessons.find(l=>l.id===view.id);
  const refs=lesson.sourceRefs.map(ref=>{const source=library.sources.find(s=>s.id===ref.sourceId);return `${esc(source.fileName)} · PDF sayfası ${ref.pages.join(', ')}`;}).join(' · ');
  const exercises=lesson.examples.map(q=>`<article class="math-example"><p><b>${esc(q.text)}</b></p><ol type="A">${q.options.map(o=>'<li>'+esc(o)+'</li>').join('')}</ol><details><summary>Açıklamayı incele</summary><p><b>Doğru cevap: ${'ABCDE'[q.answer]}) ${esc(q.options[q.answer])}</b></p><ol>${q.steps.map(s=>'<li>'+esc(s)+'</li>').join('')}</ol></details></article>`).join('');
  const body=view.tab==='lesson'?noteActions(lessonNotebook(lesson,esc,style))+`<h3>Özgün çözümlü örnekler</h3><p class="footnote">Bu örnekler editör taslağıdır; sayısal matematik kontrolü veya uzman onayı uygulanmış sorular olarak sunulmaz. Test istatistiğine eklenmez.</p>${exercises}`:`<label for="pdfNoteSummary">Özet uzunluğu</label><select id="pdfNoteSummary"><option value="quick" ${level==='quick'?'selected':''}>1 dakikalık hızlı tekrar</option><option value="standard" ${level==='standard'?'selected':''}>5 dakikalık standart özet</option><option value="detailed" ${level==='detailed'?'selected':''}>Ayrıntılı tekrar notları</option></select><p class="footnote">Süreler yaklaşık okuma hedefidir; kişiye göre değişir.</p>${noteActions(summaryNotebook(lesson,level,esc,style))}`;
  screen.innerHTML=`<button class="back" data-notes-action="library">← PDF ders notları</button><section class="card"><div class="small-label">${names[lesson.subject]} · ÖZGÜN ÇALIŞMA TASLAĞI</div><h1 id="pdfNoteTopicTitle">${esc(lesson.title)}</h1><p class="footnote">Kaynak eşleşmesi: ${refs}. Sayfa numarası PDF sırasıdır. Uzman incelemesi bekleniyor.</p><div class="pdf-note-tabs" role="group" aria-label="Ders notu bölümleri"><button class="pill ${view.tab==='lesson'?'active':''}" aria-pressed="${view.tab==='lesson'}" data-notes-action="section" data-section="lesson">✎ Konu anlatımı</button><button class="pill ${view.tab==='summary'?'active':''}" aria-pressed="${view.tab==='summary'}" data-notes-action="section" data-section="summary">⚡ Kısa özet</button></div><div class="article" id="pdfNoteBody">${body}</div></section>`;
 }
 function action(event){const button=event.target.closest('[data-notes-action]');if(!button||!ready())return;
  const action=button.dataset.notesAction;
  if(action==='library')return openLibrary();
  if(action==='close'){window.closeLesson();return;}
  if(action==='topic')return openTopic(button.dataset.noteId);
  if(action==='section'&&view?.kind==='topic'&&['lesson','summary'].includes(button.dataset.section)){view.tab=button.dataset.section;render();return;}
  if(action==='note-style'&&['notebook','plain'].includes(button.dataset.style)){style=button.dataset.style;try{localStorage.setItem('akademi_pdf_notes_style_v1',style);}catch{}render();}
 }
 $('lessons').addEventListener('click',action);$('home').addEventListener('click',action);
 screen.addEventListener('change',event=>{if(event.target.id==='pdfNoteSummary'&&['quick','standard','detailed'].includes(event.target.value)){level=event.target.value;render();}});
 window.closeLesson=function(){close();return prior.close();};
 window.openLesson=function(...args){close();return prior.open(...args);};
 window.navTo=function(tab){if(tab!=='lessons'&&view){close();prior.close();}return prior.nav(tab);};
 window.renderExamState=function(){prior.exam();entries.forEach(e=>e.hidden=!ready());if(!ready())close();};
 window.AcademiMath.back=function(){if(ready()&&$('lessons').classList.contains('active')&&view){if(view.kind==='topic')openLibrary();else window.closeLesson();return true;}return prior.back();};
 window.AcademiNotes={open:openLibrary,openTopic};
}

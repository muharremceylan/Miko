import { test } from 'node:test';
import assert from 'node:assert/strict';
import { MathProgress, STORAGE_KEY, curriculum, leaves, nodes, bank, validQuestion, validState, eligibleQuestions, selectQuestions, attemptSummary } from '../src/math/engine.js';
const memory = () => { const data = new Map(); return { data, getItem:k=>data.get(k)??null, setItem:(k,v)=>data.set(k,v) }; };
const complete = (store, wrong = false) => { const a=store.active(); while(store.active()){ const q=a.questions[a.current]; store.answer(wrong ? (q.answer+1)%5 : q.answer); store.next(); } return a; };
test('müfredatta 39 benzersiz düğüm ve 34 son konu vardır; ebeveyn/çocuk bağlantıları tutarlıdır',()=>{
 assert.equal(curriculum.topics.length,39);assert.equal(nodes.size,39);assert.equal(leaves.length,34);
 for(const t of curriculum.topics)for(const child of t.children)assert.equal(nodes.get(child).parentId,t.id);
});
test('30 test sorusu beş seçenekli ve benzersizdir; sorulardaki doğrulama kimliği korunur',()=>{
 assert.equal(bank.length,30);assert.equal(new Set(bank.map(q=>q.id)).size,30);assert.equal(new Set(bank.map(q=>q.text)).size,30);
 assert.ok(bank.every(validQuestion));assert.ok(bank.every(q=>q.verification===q.id));
});
test('10/20/30 sorular tekrarsız seçilir; oturum soru sürümünün bağımsız kopyasını saklar',()=>{
 for(const size of [10,20,30]){ const selected=selectQuestions(bank,size);assert.equal(new Set(selected.map(q=>q.id)).size,size);selected[0].options[0]='changed';assert.notEqual(bank.find(q=>q.id===selected[0].id).options[0],'changed'); }
 assert.throws(()=>selectQuestions(bank,31));assert.throws(()=>selectQuestions([],1));
});
test('çift cevap ve ilerleme engellenir; test bitişi sabittir; boşlar cevaplanan sayıya katılmaz',()=>{
 const s=new MathProgress(memory()),a=s.start('temel','all',10);
 assert.equal(s.next(),false);assert.equal(s.answer(6),false);assert.equal(s.answer(-1),false);
 assert.equal(s.answer(a.questions[0].answer),true);assert.equal(s.answer(0),false);s.next();s.answer(null);s.next();s.finish();
 const result=attemptSummary(a);assert.deepEqual([result.solved,result.correct,result.wrong,result.blank,result.rate],[1,1,0,9,100]);
 assert.equal(s.answer(0),false);assert.equal(s.next(),false);assert.equal(s.stats().solved,1);
});
test('yanlış filtresi son cevaba bakar; düzelen soru çıkar, geçmiş denemeler korunur',()=>{
 const s=new MathProgress(memory());s.start('temel','all',1);const a=complete(s,true);
 assert.equal(eligibleQuestions('temel','wrong',s.state.attempts).length,1);
 assert.equal(eligibleQuestions('temel','unseen',s.state.attempts).length,29);
 s.start('temel','wrong',1);complete(s,false);
 assert.equal(eligibleQuestions('temel','wrong',s.state.attempts).length,0);assert.equal(s.state.attempts.length,2);assert.equal(attemptSummary(a).wrong,1);
});
test('boş bırakılmış soru çözülmemiş sayılır, yanlış sayılmaz; boş havuzda test başlatılmaz',()=>{
 const s=new MathProgress(memory());s.start('temel','all',1);s.answer(null);s.next();
 assert.equal(eligibleQuestions('temel','unseen',s.state.attempts).length,30);
 assert.equal(eligibleQuestions('temel','wrong',s.state.attempts).length,0);
 assert.throws(()=>s.start('temel','wrong',10));assert.equal(s.state.attempts.length,1);
 assert.equal(eligibleQuestions('sayilar','all',s.state.attempts).length,0);
});
test('yarım test yenileme sonrası aynı soru sırasıyla sürer; cevap ikinci kez kaydolmaz',()=>{
 const db=memory(),s=new MathProgress(db),a=s.start('temel','all',20,'assessment');s.answer(a.questions[0].answer);s.next();
 const loaded=new MathProgress(db);assert.ok(validState(loaded.state));assert.equal(loaded.active().id,a.id);assert.equal(loaded.active().mode,'assessment');
 assert.deepEqual(loaded.active().questions,a.questions);assert.equal(loaded.active().current,1);assert.equal(loaded.stats().solved,1);
 assert.throws(()=>loaded.start('temel','all',10),/active/);
 complete(loaded);assert.equal(loaded.stats().solved,20);assert.equal(loaded.active(),null);
});
test('tamamlama başarıdan ayrıdır; yalnız hazır konu işaretlenir ve payda 34 kalır',()=>{
 const s=new MathProgress(memory());s.start('temel','all',30);complete(s);assert.equal(s.progress().complete,0);
 s.complete('sayilar',true);assert.equal(s.progress().complete,0);s.complete('temel',true);
 assert.deepEqual(s.progress(),{complete:1,total:34,remaining:33,percent:3});s.complete('temel',false);assert.equal(s.progress().percent,0);
});
test('geçersiz JSON, konu, soru ve tekrar eden deneme kaydı güvenle reddedilir; açılışta silinmez',()=>{
 for(const raw of ['broken','null','[]',JSON.stringify({version:1,topics:{}})]){
  const db=memory();db.setItem(STORAGE_KEY,raw);const s=new MathProgress(db);assert.ok(s.notice);assert.equal(db.getItem(STORAGE_KEY),raw);assert.equal(s.state.attempts.length,0);
 }
 const s=new MathProgress(memory());s.start('temel','all',1);const bad=structuredClone(s.state);bad.attempts[0].questions[0].options.pop();assert.equal(validState(bad),false);
 const repeated=structuredClone(s.state);repeated.attempts.push(structuredClone(repeated.attempts[0]));assert.equal(validState(repeated),false);
});
test('depolama engelinde oturum çalışır ve kalıcılık uyarısı gösterilir',()=>{
 const s=new MathProgress({getItem(){throw Error('blocked')},setItem(){throw Error('quota')}});assert.ok(s.notice);
 const a=s.start('temel','all',10);s.answer(a.questions[0].answer);assert.equal(s.stats().solved,1);assert.match(s.notice,/kaydedilemedi/);
});
test('denemeleri temizlemek konu tamamlama/sekme tercihini ve eski sayaç anahtarlarını silmez',()=>{
 const db=memory();db.setItem('akademi_stats_v1','legacy');const s=new MathProgress(db);s.touch('temel','formulas',120);s.complete('temel',true);s.start('temel','all',1);complete(s);s.clearAttempts();
 assert.equal(s.stats().solved,0);assert.equal(s.progress().complete,1);assert.equal(s.state.topics.temel.tab,'formulas');assert.equal(db.getItem('akademi_stats_v1'),'legacy');
});
test('boş testte doğruluk gösterilmez; günlük sayaç tarihine göre ayrılır',()=>{
 const s=new MathProgress(memory()),a=s.start('temel','all',1);s.finish();assert.equal(attemptSummary(a).rate,null);
 s.start('temel','all',1);complete(s);assert.equal(s.stats('1900-01-01').solved,0);assert.equal(s.stats().solved,1);
});

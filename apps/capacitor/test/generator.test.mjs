import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildGeneratedQuestion, templateCatalog, availableVariants, generateQuestions, seededRandom } from '../src/math/generator.js';
import { checkGeneratedQuestion, expectedAnswer } from '../src/math/generation-check.js';
import { sourcesFor, safeSourceUrl } from '../src/math/sources.js';
import { MathProgress, validState, validQuestion, eligibleQuestions, mistakes, descendantIds } from '../src/math/engine.js';
const topics=[...new Set(templateCatalog.map(t=>t.topicId))];
const memory=()=>{const data=new Map();return {getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v)};};
function finish(s,correct){const a=s.active();while(s.active()){const q=a.questions[a.current];s.answer(correct?q.answer:(q.answer+1)%5);s.next();}return a;}
test('16 özgün kalıbın 1706 sonlu varyasyonu beş farklı seçenek ve bağımsız sayısal kontrolü geçer',()=>{
 assert.equal(templateCatalog.length,16);
 const specs=availableVariants(topics);assert.equal(specs.length,1706);
 const ids=new Set(),texts=new Set();
 for(const spec of specs){const q=buildGeneratedQuestion(spec.templateId,spec.parameters);assert.ok(validQuestion(q));assert.ok(checkGeneratedQuestion(q));assert.equal(q.origin.expertApproved,false);assert.equal(q.reviewStatus,'generated-math-checked');ids.add(q.id);texts.add(q.text);}
 assert.equal(ids.size,specs.length);assert.equal(texts.size,specs.length);
 for(const topic of topics)for(const difficulty of ['Kolay','Orta'])assert.ok(availableVariants([topic],difficulty).length>=30,topic+difficulty);
});
test('kısa yol dışındaki bağımsız kontrol, bilinen köşe durumlarını hesaplar ve bozuk cevabı reddeder',()=>{
 assert.equal(expectedAnswer('factorial-zeros',[125]),31);
 assert.equal(expectedAnswer('integer-product',[-9,2,1]),-17);
 assert.equal(expectedAnswer('natural-digits',[17,8]),0);
 assert.equal(expectedAnswer('sets-interval',[-8,2,0]),3);
 assert.equal(expectedAnswer('divisibility-nine',[8,1]),9);
 assert.equal(expectedAnswer('base-find',[8,7,0]),8);
 const q=buildGeneratedQuestion('factorial-zeros',[125]);
 for(const change of [q=>q.answer=(q.answer+1)%5,q=>q.options[0]=q.options[1],q=>q.origin.parameters=[999999],q=>q.topicId='temel',q=>q.origin.templateVersion=2,q=>q.text='',q=>q.steps=[],q=>q.options[0]='1;alert(1)']){const bad=structuredClone(q);change(bad);assert.equal(checkGeneratedQuestion(bad),false);}
 assert.throws(()=>expectedAnswer('unknown',[2]));assert.throws(()=>expectedAnswer('factorial-zeros',['125']));
 assert.throws(()=>buildGeneratedQuestion('temel-digits',[0,0]));
});
test('aynı kalıp/parametre sabit soru kimliği ve seçenekler üretir; tohumlu taslak tekrarlanabilir',()=>{
 const first=generateQuestions(['temel'],30,{random:seededRandom('pilot-1')});
 assert.deepEqual(first,generateQuestions(['temel'],30,{random:seededRandom('pilot-1')}));
 assert.deepEqual(buildGeneratedQuestion('temel-digits',[9,0]),buildGeneratedQuestion('temel-digits',[9,0]));
 assert.equal(new Set(first.map(q=>q.origin.templateId)).size,2);
 assert.deepEqual(new Set(first.map(q=>q.difficulty)),new Set(['Kolay','Orta']));
});
test('üretilmiş testler eski ilerlemeyi korur, yenilenince aynı sorular sürer ve ikinci test açılmaz',()=>{
 const db=memory(),s=new MathProgress(db);s.complete('temel',true);
 const a=s.startGenerated('sayilar-bolme',30,'Orta','assessment');assert.ok(a.questions.every(q=>q.difficulty==='Orta'));
 s.answer(a.questions[0].answer);s.next();assert.ok(validState(s.state));
 const loaded=new MathProgress(db);assert.deepEqual(loaded.active(),a);assert.equal(loaded.progress().complete,1);
 assert.throws(()=>loaded.startGenerated('temel',10),/active/);assert.throws(()=>loaded.start('temel','all',10),/active/);
 finish(loaded,true);assert.equal(loaded.stats().solved,30);
 const used=new Set(a.questions.map(q=>q.id)),b=loaded.startGenerated('sayilar-bolme',30,'Orta');assert.ok(b.questions.every(q=>!used.has(q.id)));
});
test('otomatik yanlışlar defterde ve yanlış filtresinde görünür; tekrar doğruda çıkar ve geçmiş korunur',()=>{
 const s=new MathProgress(memory()),a=s.startGenerated('temel',1);s.answer((a.questions[0].answer+1)%5);
 assert.equal(mistakes(s.state.attempts).length,0);s.next();assert.equal(mistakes(s.state.attempts).length,1);
 assert.equal(eligibleQuestions('temel','all',s.state.attempts).length,30);
 const wrong=eligibleQuestions('temel','wrong',s.state.attempts);assert.equal(wrong.length,1);assert.deepEqual(wrong[0],a.questions[0]);
 s.start('temel','wrong',1);finish(s,true);assert.equal(mistakes(s.state.attempts).length,0);assert.equal(eligibleQuestions('temel','wrong',s.state.attempts).length,0);assert.equal(s.state.attempts.length,2);
});
test('bitmiş sonlu havuz, geçersiz ayar ve kapsam dışında konu yeni deneme yazmaz',()=>{
 const specs=availableVariants(['sayilar-sayi-kumeleri'],'Orta'),attempts=[{questions:specs.map(s=>({id:s.id}))}];
 assert.equal(availableVariants(['sayilar-sayi-kumeleri'],'Orta',attempts).length,0);
 assert.throws(()=>generateQuestions(['sayilar-sayi-kumeleri'],10,{difficulty:'Orta',attempts}),/insufficient/);
 const s=new MathProgress(memory());for(const [topic,count,level,mode] of [['denklemler',10,'mixed','learn'],['temel',31,'mixed','learn'],['temel',10,'Zor','learn'],['temel',10,'mixed','invalid']]){assert.throws(()=>s.startGenerated(topic,count,level,mode));assert.equal(s.state.attempts.length,0);}
 const all=generateQuestions(descendantIds('sayilar'),30,{random:seededRandom('mixed')});assert.equal(new Set(all.map(q=>q.topicId)).size,7);
});
test('kaynak kataloğu amaçları ayırır; aday/genel kaynaklar aktarım izni kazanmaz',()=>{
 const all=sourcesFor('temel');assert.equal(all.length,6);
 assert.ok(all.every(s=>s.reviewStatus==='candidate'&&s.coverage==='general-reference'&&s.rights.importAllowed===false&&s.rights.licenseStatus==='not-reviewed'));
 assert.ok(all.every(s=>s.access.status==='blocked-in-environment'));
 assert.ok(sourcesFor('temel','questions').some(s=>s.id==='osym'));
 assert.ok(!sourcesFor('temel','questions').some(s=>s.id==='kitapsec-user'));
 assert.equal(sourcesFor('temel','invalid').length,0);
 for(const url of ['javascript:alert(1)','http://example.com','https://user:password@example.com','not a URL'])assert.equal(safeSourceUrl(url),null);
 assert.equal(safeSourceUrl('https://www.osym.gov.tr/'),'https://www.osym.gov.tr/');
});

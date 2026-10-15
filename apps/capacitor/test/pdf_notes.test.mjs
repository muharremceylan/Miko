import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const path=new URL('../../../akademi_ai_prototip/content/pdf-notes/library.json',import.meta.url);
const library=JSON.parse(await readFile(path,'utf8'));
test('PDF kayıtları erişilen, OCR yapılan ve görsel incelenen kapsamı ayrı tutar',()=>{
 assert.equal(library.sources.length,4);
 const available=library.sources.filter(s=>s.pageCount);
 assert.equal(available.reduce((n,s)=>n+s.pageCount,0),373);
 for(const s of available){assert.equal(s.ocrPageCount,s.pageCount);assert.equal(s.ocrStatus,'completed-unreviewed');assert.equal(s.fullContentReviewed,false);assert.equal(s.textLayer,false);assert.match(s.sha256,/^[0-9a-f]{64}$/);assert.ok(s.visuallyReviewedPages.length<s.pageCount);assert.equal(s.usage.originalFilePublished,false);assert.equal(s.usage.bulkTextPublished,false);}
 for(const s of library.sources.filter(s=>!s.pageCount)){assert.equal(s.status,'transfer-size-blocked');assert.equal(s.sha256,null);assert.equal(s.ocrStatus,'not-accessible');assert.deepEqual(s.visuallyReviewedPages,[]);}
});
test('iki ders taslağı gerçek kaynak sayfasına bağlıdır; özet/kart/örnekler tutarlıdır',()=>{
 assert.equal(library.lessons.length,2);
 for(const l of library.lessons){
  assert.equal(l.reviewStatus,'editorial-draft');assert.equal(l.sections.length,l.memoryNotes.length);
  for(const r of l.sourceRefs){const source=library.sources.find(s=>s.id===r.sourceId);assert.ok(source);assert.ok(r.pages.every(p=>source.visuallyReviewedPages.includes(p)));}
  for(const level of ['quick','standard','detailed']){const s=l.summaries[level];assert.ok(s.paragraphs.length);if(s.headings){assert.equal(s.headings.length,s.paragraphs.length);assert.ok(s.noteIndices.every(i=>i>=0&&i<l.memoryNotes.length));}}
  for(const q of l.examples){assert.equal(q.options.length,5);assert.equal(new Set(q.options).size,5);assert.ok(Number.isInteger(q.answer)&&q.answer>=0&&q.answer<5);assert.ok(q.steps.length>1);assert.equal(q.reviewStatus,'editorial-draft');}
 }
});

import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {checkGeneratedQuestion} from '../src/math/generation-check.js';
const script=new URL('../../../scripts/content-generation/generate.mjs',import.meta.url).pathname;
test('CLI yalnız incelenecek taslak çıkarır; aynı dosyanın üzerine yazmaz',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'akademi-draft-test-'));
 try{
  const file=join(dir,'draft.json'),args=['--topic','sayilar','--count','30','--seed','test','--output',file];
  const result=spawnSync(process.execPath,[script,...args],{encoding:'utf8'});assert.equal(result.status,0,result.stderr);
  const raw=await readFile(file,'utf8'),data=JSON.parse(raw);
  assert.equal(data.status,'draft');assert.equal(data.expertApproved,false);assert.equal(data.rights.externalContentImported,false);
  assert.equal(data.questions.length,30);assert.ok(data.questions.every(checkGeneratedQuestion));
  assert.equal(spawnSync(process.execPath,[script,...args]).status,1);assert.equal(await readFile(file,'utf8'),raw);
 }finally{await rm(dir,{recursive:true,force:true});}
});
test('CLI geçersiz parametreleri kabul etmez ve dosya oluşturmaz',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'akademi-draft-test-'));
 try{for(const args of [['--unknown','x'],['--count','100'],['--topic','denklemler'],['--difficulty','Zor'],['--count','10','--count','20']])assert.equal(spawnSync(process.execPath,[script,...args,'--output',join(dir,'none.json')]).status,1);}
 finally{await rm(dir,{recursive:true,force:true});}
});

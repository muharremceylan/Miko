import { writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { generateQuestions, seededRandom, templateCatalog } from '../../apps/capacitor/src/math/generator.js';
import { descendantIds } from '../../apps/capacitor/src/math/engine.js';
const args=process.argv.slice(2),options={};
const allowed=new Set(['--topic','--count','--difficulty','--seed','--output']);
try{
 for(let i=0;i<args.length;i+=2){if(!allowed.has(args[i])||!args[i+1]||args[i+1].startsWith('--')||Object.hasOwn(options,args[i]))throw Error('Geçersiz veya yinelenen seçenek.');options[args[i]]=args[i+1];}
 if(!options['--output'])throw Error('--output ile yeni bir taslak dosyası belirt.');
 const topic=options['--topic']??'sayilar',count=Number(options['--count']??30),difficulty=options['--difficulty']??'mixed',seed=options['--seed']??'akademi-pilot-1';
 const questions=generateQuestions(descendantIds(topic),count,{difficulty,random:seededRandom(seed)});
 const templateIds=new Set(questions.map(q=>q.origin.templateId));
 const bundle={schemaVersion:1,status:'draft',exam:'kpss',level:'lisans',subject:'matematik',topicId:topic,generatorVersion:1,seed,expertApproved:false,rights:{source:'akademi-original-templates',externalContentImported:false},templates:templateCatalog.filter(t=>templateIds.has(t.id)),questions};
 const output=resolve(options['--output']);await writeFile(output,JSON.stringify(bundle,null,2)+'\n',{flag:'wx'});
 console.log(`${count} soru sayısal kontrolden geçti; inceleme taslağı: ${output}. Uzman onayı veya otomatik yayın yapılmadı.`);
}catch(error){console.error(error.code==='EEXIST'?'Çıktı zaten var; mevcut dosya değiştirilmedi.':error.message);process.exitCode=1;}

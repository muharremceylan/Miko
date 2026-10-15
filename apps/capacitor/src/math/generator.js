import { checkGeneratedQuestion, generatedId } from './generation-check.js';
const range=(a,b)=>Array.from({length:b-a+1},(_,i)=>a+i);
const cross=(...axes)=>axes.reduce((rows,axis)=>rows.flatMap(row=>axis.map(n=>[...row,n])),[[]]);
const label=n=>n<0?`(${n})`:String(n);
const entry=(id,topicId,difficulty,parameters,make)=>({id,topicId,difficulty,parameters,make});
// Kalıplar Akademi AI için özgün yazıldı; dış kaynak sorusu veya AI yanıtı kopyalanmaz.
const templates=[
 entry('temel-digits','temel','Kolay',cross(range(2,9),range(0,8)).filter(([a,b])=>b<a),([a,b])=>({
  text:`Rakamları toplamı ${a+b} olan iki basamaklı bir sayının onlar rakamı, birler rakamından ${a-b} fazladır. Bu sayı kaçtır?`,value:10*a+b,
  steps:[`Onlar rakamına x, birler rakamına y de: x + y = ${a+b}, x − y = ${a-b}.`,`Eşitlikleri topla: 2x = ${2*a}, x = ${a}; y = ${b}.`,`Sayı 10 × ${a} + ${b} = ${10*a+b}. Rakamlar ve ilk basamak koşulu uygundur.`],formula:'İki basamaklı sayı: 10x + y.',alternative:'Seçeneklerde rakamların toplamını ve farkını kontrol et.',errors:[10*b+a,a+b,10*a+b+9]})),
 entry('temel-sequence','temel','Orta',cross(range(-9,20),range(3,9)),([a,n])=>({
  text:`${a} ile ${a+n-1} arasındaki tüm tam sayıların (iki uç dahil) toplamı kaçtır?`,value:n*(2*a+n-1)/2,
  steps:[`Terim sayısı ${a+n-1} − ${label(a)} + 1 = ${n}.`,`İlk ve sonun toplamı ${2*a+n-1}.`,`Toplam ${n} × ${label(2*a+n-1)} / 2 = ${n*(2*a+n-1)/2}.`],formula:'Eşit aralıklı toplam = adet × (ilk + son)/2.',alternative:'Tam sayıları tek tek topla; karşıt işaretlileri eşleştir.',errors:[n*(2*a+n-1),n*(2*a+n-1)/2+a]})),
 entry('sets-interval','sayilar-sayi-kumeleri','Kolay',cross(range(-8,-2),range(2,8),[0,1]),([a,b,k])=>({
  text:`${a} ≤ x ≤ ${b} koşulunu sağlayan kaç ${k===0?'doğal sayı':'negatif tam sayı'} vardır? (Bu soruda 0 doğal sayıdır.)`,value:k===0?b+1:-a,
  steps:[k===0?`Doğal sayılar 0’dan başlar; uygun değerler 0 ile ${b} arasındadır.`:`Negatifler ${a} ile −1 arasındadır; sıfır alınmaz.`,k===0?`İki uç dahil adet ${b} − 0 + 1 = ${b+1}.`:`Adet −1 − ${label(a)} + 1 = ${-a}.`],formula:'Aralıktaki tam sayı adedi: son − ilk + 1.',errors:[b-a+1,k===0?b:-a+1]})),
 entry('sets-intersection','sayilar-sayi-kumeleri','Orta',cross(range(-4,5),range(1,5)),([a,s])=>({
  text:`A = {${range(a,a+5).join(', ')}} ve B = {${range(a+s,a+s+5).join(', ')}} ise A ∩ B kaç elemanlıdır?`,value:6-s,
  steps:[`Kesişim her iki kümede de bulunan elemanları içerir.`,`Ortak elemanlar: ${range(a+s,a+5).join(', ')}.`,`Her elemanı bir kez say: ${6-s} eleman.`],formula:'A ∩ B: A ve B’nin ortak elemanları.',alternative:'Birleşim adedini bulup |A ∩ B| = |A| + |B| − |A ∪ B| kullan.',errors:[6,6+s,s]})),
 entry('natural-odd-sum','sayilar-dogal-sayilar','Kolay',range(4,60).map(n=>[n]),([n])=>({
  text:`İlk ${n} pozitif tek tam sayının toplamı kaçtır?`,value:n*n,
  steps:[`Dizi 1, 3, …, ${2*n-1} biçiminde ve ${n} terimlidir.`,`İlk ve sonun ortalaması (1 + ${2*n-1}) / 2 = ${n}.`,`Toplam ${n} × ${n} = ${n*n}.`],formula:'İlk n pozitif tek sayının toplamı n².',errors:[n*(n+1),2*n-1,n*(n-1)]})),
 entry('natural-digits','sayilar-dogal-sayilar','Orta',cross(range(7,17),range(0,9)),([sum,d])=>{
  const values=range(1,9).filter(a=>sum-a>=0&&sum-a<=9&&a!==d&&sum-a!==d).map(a=>10*a+sum-a);
  return {text:`Rakamları toplamı ${sum} olan ve hiçbir basamağında ${d} rakamı bulunmayan iki basamaklı kaç doğal sayı vardır?`,value:values.length,
   steps:[`Onlar rakamı 1–9; birler rakamı 0–9 aralığında olmalı. İki basamaktan da ${d} rakamını çıkar.`,`Koşulları sağlayan sayılar: ${values.length?values.join(', '):'yok'}.`,`Uygun sayı adedi ${values.length}.`],formula:'İki basamaklı xy için x + y verilen toplama eşittir; x ≠ 0.',errors:[values.length+1,9,10]};}),
 entry('integer-product','sayilar-tam-sayilar','Kolay',cross(range(-9,-2),range(2,8),range(1,4)),([a,b,c])=>({
  text:`${label(a)} × ${b} + ${c} işleminin sonucu kaçtır?`,value:a*b+c,
  steps:[`Önce çarpma: ${label(a)} × ${b} = ${a*b}.`,`Sonra toplama: ${a*b} + ${c} = ${a*b+c}.`],formula:'Çarpma toplama işleminden önce yapılır; farklı işaretli çarpım negatiftir.',errors:[a*(b+c),-a*b+c,a*b-c]})),
 entry('integer-power','sayilar-tam-sayilar','Orta',cross(range(2,10),range(2,8)),([a,b])=>({
  text:`(−${a})² − ${b} × (−${a} + 2) işleminin sonucu kaçtır?`,value:a*a-b*(-a+2),
  steps:[`Parantez içi −${a} + 2 = ${-a+2}; (−${a})² = ${a*a}.`,`Çarpım ${b} × ${label(-a+2)} = ${b*(-a+2)}.`,`Sonuç ${a*a} − ${label(b*(-a+2))} = ${a*a-b*(-a+2)}.`],formula:'Önce parantez/kuvvet, sonra çarpma, en son çıkarma.',errors:[-a*a-b*(-a+2),a*a+b*(-a+2),a*a-b*(-a)-2]})),
 entry('factorial-ratio','sayilar-faktoriyel','Kolay',cross(range(6,30),[2,3]),([n,k])=>{
  const factors=range(n-k+1,n),value=factors.reduce((v,n)=>v*n,1);
  return {text:`${n}! / ${n-k}! işleminin sonucu kaçtır?`,value,
   steps:[`${n}! ifadesini ${n-k}! çarpanına kadar aç.`,`Ortak ${n-k}! sadeleşince ${factors.join(' × ')} kalır.`,`Çarpım ${value}.`],formula:'n! = n(n − 1)!; ortak faktöriyeli sadeleştir.',errors:[n,n-k,n*(n-k)]};}),
 entry('factorial-zeros','sayilar-faktoriyel','Orta',range(30,180).map(n=>[n]),([n])=>{
  const contributions=[];for(let power=5;power<=n;power*=5)contributions.push(Math.floor(n/power));
  const value=contributions.reduce((s,n)=>s+n,0);
  return {text:`${n}! sayısının onluk yazımının sonunda kaç sıfır bulunur?`,value,
   steps:['Her son sıfır için bir 2 ve bir 5 çarpanı gerekir; faktöriyelde 5 sayısı sınırlayıcıdır.',`${n} içinde 5’in kuvvetlerinin katkılarını topla: ${contributions.join(' + ')} = ${value}.`],formula:'Son sıfırlar = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + … .',alternative:'Asal çarpanlardaki 5’leri tek tek say; 25 ve 125’in ek katkısını unutma.',errors:[Math.floor(n/5),Math.floor(n/2),value+1]};}),
 entry('base-value','sayilar-sayma-sistemleri','Kolay',cross(range(3,8),range(1,7),range(0,7)).filter(([t,a,b])=>a<t&&b<t),([t,a,b])=>({
  text:`(${a}${b}) sayısı ${t} tabanında yazılmıştır. Onluk sistemdeki değeri kaçtır?`,value:a*t+b,
  steps:[`İki basamaklı sayının açılımı ${a} × ${t} + ${b}.`,`Sonuç ${a*t} + ${b} = ${a*t+b}; iki rakam da tabandan küçüktür.`],formula:'(ab)ₜ = a·t + b; a ≠ 0, 0 ≤ rakam < t.',errors:[10*a+b,a+b,a*t-b]})),
 entry('base-find','sayilar-sayma-sistemleri','Orta',cross(range(3,8),range(1,7),range(0,7)).filter(([t,a,b])=>a<t&&b<t),([t,a,b])=>({
  text:`(${a}${b})ₜ = ${a*t+b} eşitliğinde sağ taraf onluk sistemdedir. t tabanı kaçtır?`,value:t,
  steps:[`Basamak açılımı ${a}t + ${b} = ${a*t+b}.`,`${a}t = ${a*t}; t = ${t}.`,`Taban en az 2 olan tam sayıdır; ${a} ve ${b} rakamları ${t}’den küçüktür.`],formula:'Tabanı denklemden bul, sonra tüm rakamların tabandan küçük olduğunu denetle.',errors:[t+1,t-1,a*t+b]})),
 entry('division-remainder','sayilar-bolme','Kolay',cross(range(0,15).map(i=>37+4*i),range(4,11)),([n,b])=>{
  const q=Math.floor(n/b),r=n-b*q;
  return {text:`${n} sayısının ${b} ile bölümünden kalan kaçtır?`,value:r,
   steps:[`${n}’yi aşmayan en büyük ${b} katı ${b} × ${q} = ${b*q}.`,`Kalan ${n} − ${b*q} = ${r}.`,`0 ≤ ${r} < ${b} koşulu sağlanır.`],formula:'Bölünen = bölen × bölüm + kalan; 0 ≤ kalan < bölen.',errors:[b,q,b-r]};}),
 entry('division-rebuild','sayilar-bolme','Orta',cross(range(5,12),range(6,15)),([b,q])=>({
  text:`Bir doğal sayının ${b} ile bölümünde bölüm ${q}, kalan ${b-1} oluyor. Bu doğal sayı kaçtır?`,value:b*q+b-1,
  steps:[`Bölünen = ${b} × ${q} + ${b-1}.`,`Sonuç ${b*q} + ${b-1} = ${b*q+b-1}.`,`Kalan ${b-1}, bölen ${b}’den küçüktür.`],formula:'Bölünen = bölen × bölüm + kalan.',errors:[b*q,b*q-b+1,b+q+b-1]})),
 entry('divisibility-nine','sayilar-bolunebilme-kurallari','Kolay',cross(range(2,9),range(1,8)),([h,u])=>{
  const d=9-(h+u)%9;
  return {text:`${h}a${u} üç basamaklı sayısı 9’a tam bölünüyor. a rakamının alabileceği en büyük değer kaçtır?`,value:d,
   steps:[`Rakamlar toplamı ${h+u} + a, 9’un katı olmalıdır.`,`0–9 arasındaki rakamları denetleyince en büyük uygun rakam ${d} olur.`,`Kontrol: ${h+u+d}, 9’un katıdır; a = ${d} uygundur.`],formula:'9’a bölünebilme: rakamlar toplamı 9’un katı.',errors:[(9-(h+u)%9)%9,h+u,d-1]};}),
 entry('divisibility-twelve','sayilar-bolunebilme-kurallari','Orta',cross(range(1,9),[0,2,4,6,8]),([h,u])=>{
  const digits=range(0,9).filter(d=>(h+d+u)%3===0&&(10*d+u)%4===0),d=Math.max(...digits);
  return {text:`${h}a${u} üç basamaklı sayısı 12’ye tam bölünüyor. a rakamının alabileceği en büyük değer kaçtır?`,value:d,
   steps:['12 = 3 × 4 ve bu çarpanlar aralarında asaldır; hem 3 hem 4 kuralı sağlanmalı.',`Rakamlar toplamı ${h+u} + a, 3’ün katı; son iki basamak 10a + ${u}, 4’ün katı olmalı.`,`İki koşulu sağlayan rakamlar ${digits.join(', ')}; en büyüğü ${d}.`],formula:'12’ye bölünebilme: hem 3’e hem 4’e tam bölünme.',alternative:'0–9 rakamlarını sayıda yerine koyup doğrudan 12’ye bölerek kontrol et.',errors:[d-1,d+1,h+u]};})
];
export const templateCatalog=templates.map(({id,topicId,difficulty})=>({id,version:1,topicId,difficulty,sourceId:'akademi-templates-v1'}));
const byId=new Map(templates.map(t=>[t.id,t]));
function seeded(seed){let x=2166136261;for(const c of seed)x=Math.imul(x^c.charCodeAt(0),16777619);return ()=>{x+=0x6D2B79F5;let n=x;n=Math.imul(n^n>>>15,n|1);n^=n+Math.imul(n^n>>>7,n|61);return ((n^n>>>14)>>>0)/4294967296;};}
export const seededRandom=seed=>seeded(String(seed));
function shuffle(values,random){const copy=[...values];for(let i=copy.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[copy[i],copy[j]]=[copy[j],copy[i]];}return copy;}
export function buildGeneratedQuestion(templateId,parameters){
 const t=byId.get(templateId);
 if(!t||!Array.isArray(parameters)||!t.parameters.some(p=>p.length===parameters.length&&p.every((n,i)=>n===parameters[i])))throw Error('invalid-template-parameters');
 const {text,value,steps,formula,alternative,errors=[]}=t.make(parameters), id=generatedId(templateId,parameters);
 const domainCount=['sets-interval','sets-intersection','natural-digits','factorial-zeros','division-remainder','divisibility-nine','divisibility-twelve'].includes(templateId);
 const values=[value];
 for(const n of [...errors,...range(1,20).flatMap(d=>[value-d,value+d])]){
  if(values.length===5)break;
  if(Number.isSafeInteger(n)&&(!domainCount||n>=0)&&!values.includes(n))values.push(n);
 }
 const options=shuffle(values.map(String),seeded(id));
 const q={id,version:1,topicId:t.topicId,skill:formula,difficulty:t.difficulty,text,options,answer:options.indexOf(String(value)),steps,formula,alternative:alternative??null,reviewStatus:'generated-math-checked',origin:{kind:'template',templateId,templateVersion:1,parameters:[...parameters],sourceId:'akademi-templates-v1',expertApproved:false},verification:{kind:'template',checkerVersion:1,status:'passed'}};
 if(!checkGeneratedQuestion(q))throw Error('generation-check-failed');
 return q;
}
export function availableVariants(topicIds,difficulty='mixed',attempts=[]){
 if(!Array.isArray(topicIds)||!['mixed','Kolay','Orta'].includes(difficulty))throw Error('invalid-generation-settings');
 const used=new Set(attempts.flatMap(a=>a.questions.map(q=>q.id)));
 return templates.filter(t=>topicIds.includes(t.topicId)&&(difficulty==='mixed'||t.difficulty===difficulty)).flatMap(t=>t.parameters.map(parameters=>({templateId:t.id,parameters,id:generatedId(t.id,parameters)}))).filter(v=>!used.has(v.id));
}
export function generateQuestions(topicIds,count,{difficulty='mixed',attempts=[],random=Math.random}={}){
 const pool=availableVariants(topicIds,difficulty,attempts);
 if(!Number.isInteger(count)||count<1||count>30||pool.length<count)throw Error('insufficient-generated-pool');
 // Kalıpları sırayla örnekle: karma seçenekte ilk 30 sorunun tek kalıptan gelmesini önle.
 const groups=new Map();for(const spec of shuffle(pool,random)){if(!groups.has(spec.templateId))groups.set(spec.templateId,[]);groups.get(spec.templateId).push(spec);}
 const keys=shuffle([...groups.keys()],random),chosen=[];
 while(chosen.length<count){for(const key of keys){const spec=groups.get(key).pop();if(spec)chosen.push(spec);if(chosen.length===count)break;}}
 const questions=shuffle(chosen,random).map(s=>buildGeneratedQuestion(s.templateId,s.parameters));
 if(new Set(questions.map(q=>q.id)).size!==count||new Set(questions.map(q=>q.text)).size!==count)throw Error('duplicate-generated-question');
 return questions;
}

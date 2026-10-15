import { test } from 'node:test';
import assert from 'node:assert/strict';
import { DeviceSpeech } from '../src/math/audio.js';
import { LearningServices, aiPanel } from '../src/math/services.js';
function environment(voices=[{lang:'tr-TR',name:'Test voice'}]){
 const calls={speak:[],pause:0,resume:0,cancel:0};
 return {calls,SpeechSynthesisUtterance:class{constructor(text){this.text=text;}},speechSynthesis:{getVoices:()=>voices,addEventListener(){},speak:u=>calls.speak.push(u),pause:()=>calls.pause++,resume:()=>calls.resume++,cancel:()=>calls.cancel++}};
}
test('Türkçe ses yokken cihaz okuması kullanılabilir gibi gösterilmez',async()=>{
 const env=environment([]),speech=new DeviceSpeech({environment:env});await speech.detect();assert.equal(speech.state.available,false);await speech.play('Merhaba.');assert.equal(env.calls.speak.length,0);
});
test('Türkçe ses/hız kullanılır, ilerleme yalnız ses motoru olaylarından güncellenir',async()=>{
 const env=environment(),speech=new DeviceSpeech({environment:env});await speech.detect();await speech.play('Birinci cümle. İkinci cümle.',0.75);
 const u=env.calls.speak[0];assert.equal(u.lang,'tr-TR');assert.equal(u.rate,0.75);assert.equal(speech.state.progress,0);
 u.onboundary({charIndex:7});assert.ok(speech.state.progress>0);u.onend();assert.equal(env.calls.speak.length,2);env.calls.speak[1].onend();assert.equal(speech.state.progress,100);assert.equal(speech.state.playing,false);
});
test('duraklat/devam ve durdurma; gecikmiş ses bitişi yeniden oynatma başlatmaz',async()=>{
 const env=environment(),speech=new DeviceSpeech({environment:env});await speech.detect();await speech.play('Bir. İki.');speech.pause();assert.equal(speech.state.paused,true);speech.resume();assert.equal(speech.state.paused,false);
 const old=env.calls.speak[0];await speech.stop();old.onend();assert.equal(env.calls.speak.length,1);assert.equal(speech.state.playing,false);assert.equal(env.calls.pause,1);assert.equal(env.calls.resume,1);
});
test('native ses motoru duraklatmayı desteklemiyorsa bu kontrol sunulmaz',async()=>{
 const native={isLanguageSupported:async()=>({supported:true}),stop:async()=>{},speak:async()=>{}};
 const speech=new DeviceSpeech({environment:{},nativeTTS:native});await speech.detect();assert.equal(speech.state.canPause,false);await speech.play('Merhaba.');assert.equal(speech.state.progress,100);
});
test('native durdurma beklenirken ayrılınca geç gelen oynatma başlamaz',async()=>{
 const stops=[];let count=0;
 const native={isLanguageSupported:async()=>({supported:true}),stop:()=>new Promise(resolve=>stops.push(resolve)),speak:async()=>count++};
 const speech=new DeviceSpeech({environment:{},nativeTTS:native});await speech.detect();const play=speech.play('Merhaba.');const stop=speech.stop();stops.forEach(r=>r());await Promise.all([play,stop]);assert.equal(count,0);
});
test('ses hatası tamamlanmış ses olarak bildirilmez',async()=>{
 const env=environment(),speech=new DeviceSpeech({environment:env});await speech.detect();await speech.play('Merhaba.');env.calls.speak[0].onerror();assert.equal(speech.state.playing,false);assert.notEqual(speech.state.progress,100);assert.match(speech.state.message,/kesildi/);
});
test('sunucu adresi yokken veya HTTPS olmayan uzak adreste API isteği yapılmaz',async()=>{
 let calls=0;for(const base of ['', 'http://unsafe.example']){const service=new LearningServices({base,fetcher:async()=>calls++});await service.check();assert.equal(service.state.status,'unconfigured');assert.match(aiPanel(service,x=>x),/henüz bağlı değil/);}assert.equal(calls,0);
});
test('sunucu kapalı AI bildirdiğinde gerçek sonuç veya gönderme kontrolü gösterilmez',async()=>{
 const service=new LearningServices({base:'https://api.example',fetcher:async()=>Response.json({solver_ready:false,speech_ready:false})});await service.check();assert.match(aiPanel(service,x=>x),/henüz etkinleştirilmedi/);assert.doesNotMatch(aiPanel(service,x=>x),/<textarea/);
});
test('oturum anahtarı yalnız bellekte taşınır; 401 sonrası temizlenir',async()=>{
 const calls=[];const service=new LearningServices({base:'https://api.example',fetcher:async(url,options)=>{calls.push(options);return url.endsWith('/session')?Response.json({access_token:'test-session-only'}):Response.json({detail:'Oturum süresi doldu.'},{status:401});}});
 await service.login('test-access-code');assert.equal(service.token,'test-session-only');await assert.rejects(()=>service.request('/v1/solve',{question:'test'}));assert.equal(service.token,'');assert.equal(calls[1].headers.Authorization,'Bearer test-session-only');
});
test('başarısız sağlayıcı yanıtı yerine örnek AI sonucu uydurulmaz',async()=>{
 const service=new LearningServices({base:'https://api.example',fetcher:async()=>Response.json({detail:'AI yanıtı alınamadı.'},{status:502})});service.context('temel');service.token='test';service.state.question='2+2?';await service.solve('temel');assert.equal(service.state.result,null);assert.match(service.state.error,/alınamadı/);
});
test('geçerli gerçek AI yanıtı doğrulama durumuyla korunur',async()=>{
 const result={source:'ai',solution:{steps:[{explanation:'Topla.',calculation:'2+2=4'}],final_answer:'4'},verification:{status:'partial'}};
 const service=new LearningServices({base:'https://api.example',fetcher:async()=>Response.json(result)});service.context('temel');service.token='test';await service.solve('temel');assert.deepEqual(service.state.result,result);
});
test('iptal ve konu değişiminde eski AI sonucu yeni konuya taşınmaz',async()=>{
 const service=new LearningServices({base:'https://api.example',fetcher:(_url,options)=>new Promise((_resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('aborted','AbortError'))))});
 service.context('temel');service.token='test';const pending=service.solve('temel');service.context('sayilar');await pending;assert.equal(service.state.result,null);assert.equal(service.state.error,'');assert.equal(service.state.busy,false);
});

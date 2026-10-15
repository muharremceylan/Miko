// Yalnız herkese açık sunucu adresi istemcidedir. Sağlayıcı anahtarı sunucuda kalır.
export class LearningServices {
  constructor({base='',fetcher=globalThis.fetch.bind(globalThis),onChange=()=>{}}={}) {
    this.base=base.replace(/\/$/,'');this.fetcher=fetcher;this.onChange=onChange;this.token='';this.controller=null;this.topicId=null;
    this.state={status:base?'idle':'unconfigured',capabilities:null,error:'',busy:false,result:null,question:'',image:null,audioUrl:null,audioBusy:false};
    if(base){try{const url=new URL(base);if(url.username||url.password||url.search||url.hash||(url.protocol!=='https:' && !(url.protocol==='http:' && ['127.0.0.1','localhost'].includes(url.hostname))))throw Error();}catch{this.base='';this.state.status='unconfigured';}}
  }
  async request(path,body,signal){
    const response=await this.fetcher(this.base+path,{method:body?'POST':'GET',headers:{...(body?{'Content-Type':'application/json'}:{}),...(this.token?{Authorization:'Bearer '+this.token}:{})},...(body?{body:JSON.stringify(body)}:{}),signal});
    if(!response.ok){if(response.status===401)this.token='';let message='Hizmete ulaşılamadı. Daha sonra tekrar deneyebilirsin.';try{const data=await response.json();if(typeof data.detail==='string')message=data.detail;}catch{}throw Error(message);}
    return response;
  }
  async check(){
    if(!this.base || this.state.status==='checking')return;
    this.state.status='checking';this.onChange();
    try{const response=await this.request('/v1/capabilities',null,AbortSignal.timeout(10000));const data=await response.json();if(typeof data.solver_ready!=='boolean' || typeof data.speech_ready!=='boolean')throw Error();this.state.capabilities=data;this.state.status='ready';this.state.error='';}
    catch{this.state.status='unavailable';this.state.error='AI ve ses hizmetine şu anda ulaşılamıyor.';}this.onChange();
  }
  async login(code){
    if(!this.base)return;this.state.busy=true;this.state.error='';this.onChange();
    try{const response=await this.request('/v1/session',{access_code:code},AbortSignal.timeout(15000));const data=await response.json();if(typeof data.access_token!=='string')throw Error('Oturum açılamadı.');this.token=data.access_token;}
    catch(error){this.state.error=error.message;}finally{this.state.busy=false;this.onChange();}
  }
  async solve(topicId){
    if(!this.token || this.state.busy)return;
    this.controller=new AbortController();const timeout=setTimeout(()=>this.controller?.abort(),65000);
    this.state.busy=true;this.state.error='';this.state.result=null;this.onChange();
    try{const response=await this.request('/v1/solve',{topic_id:topicId,question:this.state.question,image_data_url:this.state.image},this.controller.signal);const data=await response.json();if(data.source!=='ai' || !data.solution || !Array.isArray(data.solution.steps) || !data.verification)throw Error('Çözüm yanıtı okunamadı.');if(this.topicId===topicId && !this.controller?.signal.aborted)this.state.result=data;}
    catch(error){if(this.topicId===topicId)this.state.error=error.name==='AbortError'?'İstek iptal edildi veya zaman aşımına uğradı.':error.message;}
    finally{clearTimeout(timeout);this.controller=null;this.state.busy=false;this.onChange();}
  }
  async speech(topicId,level){
    if(!this.token || this.state.audioBusy)return;
    this.state.audioBusy=true;this.state.error='';this.onChange();
    try{const response=await this.request('/v1/speech',{topic_id:topicId,level},AbortSignal.timeout(70000));const blob=await response.blob();if(!blob.type.startsWith('audio/'))throw Error('Ses dosyası okunamadı.');if(this.state.audioUrl)URL.revokeObjectURL(this.state.audioUrl);this.state.audioUrl=URL.createObjectURL(blob);this.state.audioLevel=level;this.state.audioTopic=topicId;}
    catch(error){this.state.error=error.name==='TimeoutError'?'Ses üretimi zaman aşımına uğradı.':error.message;}
    finally{this.state.audioBusy=false;this.onChange();}
  }
  context(topicId){if(this.topicId!==topicId){this.cancel();this.topicId=topicId;this.state.question='';this.state.image=null;this.state.result=null;this.state.error='';}}
  cancel(){this.controller?.abort();}
}
export function aiPanel(service,esc){
 const s=service.state;
 if(s.status==='unconfigured')return '<div class="service-note"><b>Yapay zekâ öğretmen henüz bağlı değil.</b><p>Soruyu yazıp veya fotoğrafını yükleyip gerçek çözüm alacağın bağlantı hazırlanıyor. Şimdilik bu konudaki çözümlü örneklerden yararlanabilirsin.</p></div>';
 if(s.status==='idle' || s.status==='checking')return '<p role="status">AI bağlantısı kontrol ediliyor…</p>';
 if(s.status==='unavailable')return `<p class="note">${esc(s.error)}</p><button class="ghost full" data-math-action="service-check">Bağlantıyı tekrar dene</button>`;
 if(!s.capabilities.solver_ready)return '<div class="service-note">AI hizmeti henüz etkinleştirilmedi. Sabit bir örnek gerçek AI sonucu olarak gösterilmez.</div>';
 if(!service.token)return loginPanel(service,esc);
 const result=s.result;
 let output='';
 if(result){const r=result.solution,v=result.verification;
  const status=v.status==='inconsistent'?'Sayısal adımlarda çelişki bulundu. Bu sonucu kesin cevap olarak kullanma.':v.status==='partial'?'Bazı sayısal adımlar kontrol edildi; çözümün bütünü uzman onaylı değildir.':'Bu AI çözümü bağımsız olarak doğrulanmadı.';
  output=`<section class="ai-result" aria-live="polite"><span class="chip">Gerçek AI yanıtı</span><p class="note">${esc(status)}</p><h3>Okunan soru</h3><p>${esc(r.transcribed_question)}</p>${r.needs_clarification?'<h3>Ek bilgi gerekli</h3><p>'+esc(r.clarification)+'</p>':'<h3>Adım adım çözüm</h3><ol>'+r.steps.map(step=>'<li><p>'+esc(step.explanation)+'</p><code>'+esc(step.calculation)+'</code></li>').join('')+'</ol><h3>AI’ın önerdiği sonuç</h3><p>'+esc(r.final_answer)+'</p>'}${r.assumptions?.length?'<h4>Varsayımlar</h4><ul>'+r.assumptions.map(a=>'<li>'+esc(a)+'</li>').join('')+'</ul>':''}</section>`;
 }
 return `<p class="mini muted">Metin ve görsel, çözüm için AI sağlayıcısına gönderilir. AI yanıtları hata içerebilir; soru çözümünü kontrol ederek çalış.</p><label for="aiQuestion">Sorun</label><textarea id="aiQuestion" maxlength="3000" rows="5" placeholder="Sorunu buraya yaz…" ${s.busy?'disabled':''}>${esc(s.question)}</textarea><label class="service-upload" for="aiQuestionImage">Fotoğraf ekle <small>PNG, JPEG veya WebP · en fazla 4 MB</small></label><input id="aiQuestionImage" type="file" accept="image/png,image/jpeg,image/webp" ${s.busy?'disabled':''}>${s.image?`<img class="ai-question-image" src="${esc(s.image)}" alt="Eklenen soru görseli"><button class="back" data-math-action="ai-clear-image" ${s.busy?'disabled':''}>Görseli kaldır</button>`:''}${s.error?'<p class="note" role="alert">'+esc(s.error)+'</p>':''}<button class="cta full" data-math-action="ai-solve" ${s.busy?'disabled':''}>${s.busy?'Çözüm hazırlanıyor…':'Adım adım çöz'}</button>${s.busy?'<button class="ghost full" data-math-action="ai-cancel">İsteği iptal et</button>':''}${output}`;
}
export function loginPanel(service,esc){
 return `<p class="mini">Bu pilotta AI ve ses hizmeti davet koduyla açılır. Sağlayıcı API anahtarı istenmez.</p><label for="aiAccessCode">Davet kodu</label><input id="aiAccessCode" type="password" autocomplete="off" maxlength="200">${service.state.error?'<p class="note" role="alert">'+esc(service.state.error)+'</p>':''}<button class="ghost full" data-math-action="service-login" ${service.state.busy?'disabled':''}>${service.state.busy?'Açılıyor…':'Hizmete giriş yap'}</button>`;
}

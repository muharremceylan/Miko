// Cihaz TTS'si ses dosyası değildir. İlerleme okunan karakterlere dayanır.
export class DeviceSpeech {
  constructor({environment,onChange=()=>{},nativeTTS=null}) {
    this.env=environment;this.onChange=onChange;this.native=nativeTTS;
    this.state={available:false,checking:true,playing:false,paused:false,progress:0,message:'Türkçe cihaz sesi kontrol ediliyor…',canPause:!nativeTTS};
    this.token=0;this.voice=null;this.utterance=null;this.listening=false;
  }
  async detect() {
    if(this.native){
      try{const result=await this.native.isLanguageSupported({lang:'tr-TR'});this.state.available=!!result.supported;}catch{this.state.available=false;}
      this.state.checking=false;this.state.message=this.state.available?'Türkçe cihaz sesi hazır. Bu bir podcast kaydı değildir.':'Cihazda Türkçe ses kullanılamıyor. Metni aşağıdan okuyabilirsin.';this.onChange();return;
    }
    const synth=this.env.speechSynthesis;
    const update=()=>{this.voice=synth?.getVoices().find(v=>/^tr(?:-|$)/i.test(v.lang));this.state.available=!!this.voice;this.state.checking=false;if(!this.state.playing)this.state.message=this.voice?'Türkçe cihaz sesi hazır. Ses kalitesi cihazına bağlıdır.':'Bu tarayıcıda Türkçe ses bulunamadı. Metni okuyabilir veya Türkçe ses paketi olan cihazda deneyebilirsin.';this.onChange();};
    if(!this.listening && synth?.addEventListener){synth.addEventListener('voiceschanged',update);this.listening=true;}
    update();
  }
  async stop(emit=true) {
    this.token++;this.env.speechSynthesis?.cancel();if(this.native)await this.native.stop().catch(()=>{});
    this.utterance=null;this.state.playing=false;this.state.paused=false;this.state.message='Sesli özet durduruldu.';if(emit)this.onChange();
  }
  async play(text,rate=0.9) {
    const stopped=this.stop(false),token=this.token;await stopped;if(token!==this.token)return;
    if(!this.state.available){this.state.message='Türkçe cihaz sesi kullanılamıyor.';this.onChange();return;}
    this.state.playing=true;this.state.paused=false;this.state.progress=0;this.state.message='Cihaz sesiyle okunuyor…';this.onChange();
    if(this.native){try{await this.native.speak({text,lang:'tr-TR',rate,volume:1,category:'ambient'});if(token!==this.token)return;this.state.playing=false;this.state.progress=100;this.state.message='Sesli özet tamamlandı.';}catch{if(token!==this.token)return;this.state.playing=false;this.state.message='Cihaz seslendirmesi başlatılamadı.';}this.onChange();return;}
    const chunks=text.match(/[^.!?]+[.!?]?/g)??[text];let offset=0;
    const next=()=>{
      if(token!==this.token)return;
      if(!chunks.length){this.state.playing=false;this.state.progress=100;this.state.message='Sesli özet tamamlandı.';this.onChange();return;}
      const chunk=chunks.shift(),start=offset;offset+=chunk.length;
      const utterance=new this.env.SpeechSynthesisUtterance(chunk);this.utterance=utterance;
      utterance.lang='tr-TR';utterance.voice=this.voice;utterance.rate=rate;
      utterance.onboundary=event=>{if(token===this.token){this.state.progress=Math.min(99,Math.round(100*(start+Math.max(0,event.charIndex??0))/text.length));this.onChange();}};
      utterance.onend=next;
      utterance.onerror=()=>{if(token===this.token){this.state.playing=false;this.state.message='Cihaz sesi kesildi. Tekrar dinlemeyi deneyebilirsin.';this.onChange();}};
      try{this.env.speechSynthesis.speak(utterance);}catch{utterance.onerror();}
    };next();
  }
  pause(){if(!this.native && this.state.playing && !this.state.paused){this.env.speechSynthesis.pause();this.state.paused=true;this.state.message='Sesli özet duraklatıldı.';this.onChange();}}
  resume(){if(!this.native && this.state.playing && this.state.paused){this.env.speechSynthesis.resume();this.state.paused=false;this.state.message='Cihaz sesiyle okunuyor…';this.onChange();}}
}

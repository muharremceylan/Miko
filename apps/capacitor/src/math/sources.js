import catalog from '../../../../akademi_ai_prototip/content/kpss/lisans/matematik/sources.json' with {type:'json'};
export const sourceUses={all:'Tüm kaynaklar',lesson:'Konu anlatımı',questions:'Soru ve alıştırma',exam:'Resmî sınav bilgisi',scope:'Konu listesi'};
export function safeSourceUrl(value){try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password?u.href:null;}catch{return null;}}
export function sourcesFor(topicId,use='all'){
 if(!Object.hasOwn(sourceUses,use))return [];
 return catalog.sources.filter(s=>(s.topicIds.includes('*')||s.topicIds.includes(topicId))&&(use==='all'||s.uses.includes(use))&&safeSourceUrl(s.url));
}
export function sourceCards(topicId,use,esc){
 return sourcesFor(topicId,use).map(s=>`<article class="math-source"><span class="chip">Aday kaynak · ${s.language==='tr'?'Türkçe':'İngilizce'}</span><h3>${esc(s.title)}</h3><p class="mini muted">${esc(s.owner)}</p><p>${esc(s.note)}</p><p class="footnote">Genel başvuru bağlantısı; bu konuya ait belirli bir bölüm henüz doğrulanmadı. Bağlantı kontrolü: ${esc(s.access.attemptedOn)} — bu ortamda erişim engeli.</p><a class="source-external" href="${esc(safeSourceUrl(s.url))}" target="_blank" rel="noopener noreferrer">Kaynağı aç ↗</a></article>`).join('');
}

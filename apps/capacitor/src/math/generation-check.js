// Üreticideki kısa yolları tekrarlamadan sayma/arama/çarpma ile kontrol eder.
// Bu kontrol sayısaldır; dil, pedagojik kalite veya uzman onayı değildir.
const ints = (a,b) => Array.from({length:b-a+1},(_,i)=>a+i);
const fact = n => {let v=1n;for(let i=2;i<=n;i++)v*=BigInt(i);return v;};
export const generatedId = (templateId,parameters) => `auto-${templateId}-v1-${parameters.join('_')}`;
export function expectedAnswer(templateId,p) {
  if(!Array.isArray(p)||p.length>3||!p.every(Number.isSafeInteger))throw Error('invalid-parameters');
  const [a,b,c]=p;
  switch(templateId){
    case 'temel-digits':{
      if(p.length!==2||a<2||a>9||b<0||b>=a)break;
      const candidates=ints(10,99).filter(n=>Math.floor(n/10)+n%10===a+b&&Math.floor(n/10)-n%10===a-b);
      if(candidates.length===1)return candidates[0];break;
    }
    case 'temel-sequence':if(p.length===2&&a>=-9&&a<=20&&b>=3&&b<=9)return ints(a,a+b-1).reduce((s,n)=>s+n,0);break;
    case 'sets-interval':if(p.length===3&&a>=-8&&a<=-2&&b>=2&&b<=8&&[0,1].includes(c))return ints(a,b).filter(n=>c===0?n>=0:n<0).length;break;
    case 'sets-intersection':{
      if(p.length!==2||a<-4||a>5||b<1||b>5)break;
      const left=new Set(ints(a,a+5));return ints(a+b,a+b+5).filter(n=>left.has(n)).length;
    }
    case 'natural-odd-sum':if(p.length===1&&a>=4&&a<=60)return ints(1,2*a-1).filter(n=>n%2!==0).reduce((s,n)=>s+n,0);break;
    case 'natural-digits':if(p.length===2&&a>=7&&a<=17&&b>=0&&b<=9)return ints(10,99).filter(n=>Math.floor(n/10)+n%10===a&&Math.floor(n/10)!==b&&n%10!==b).length;break;
    case 'integer-product':if(p.length===3&&a>=-9&&a<=-2&&b>=2&&b<=8&&c>=1&&c<=4)return -ints(1,b).reduce(s=>s+Math.abs(a),0)+c;break;
    case 'integer-power':if(p.length===2&&a>=2&&a<=10&&b>=2&&b<=8){const square=ints(1,a).reduce(s=>s+a,0);return square-ints(1,b).reduce(s=>s+(-a+2),0);}break;
    case 'factorial-ratio':if(p.length===2&&a>=6&&a<=30&&[2,3].includes(b))return Number(fact(a)/fact(a-b));break;
    case 'factorial-zeros':{
      if(p.length!==1||a<30||a>180)break;
      const digits=String(fact(a));return digits.length-digits.replace(/0+$/,'').length;
    }
    case 'base-value':if(p.length===3&&a>=3&&a<=8&&b>=1&&b<a&&c>=0&&c<a){let result=c;for(let i=0;i<b;i++)result+=a;return result;}break;
    case 'base-find':if(p.length===3&&a>=3&&a<=8&&b>=1&&b<a&&c>=0&&c<a){const result=b*a+c;const matches=ints(Math.max(b,c)+1,16).filter(t=>b*t+c===result);if(matches.length===1)return matches[0];}break;
    case 'division-remainder':if(p.length===2&&a>=37&&a<=97&&(a-37)%4===0&&b>=4&&b<=11){let r=a;while(r>=b)r-=b;return r;}break;
    case 'division-rebuild':if(p.length===2&&a>=5&&a<=12&&b>=6&&b<=15){let total=a-1;for(let i=0;i<b;i++)total+=a;return total;}break;
    case 'divisibility-nine':if(p.length===2&&a>=2&&a<=9&&b>=1&&b<=8){const digits=ints(0,9).filter(d=>(100*a+10*d+b)%9===0);return Math.max(...digits);}break;
    case 'divisibility-twelve':if(p.length===2&&a>=1&&a<=9&&[0,2,4,6,8].includes(b)){const digits=ints(0,9).filter(d=>(100*a+10*d+b)%12===0);return Math.max(...digits);}break;
  }
  throw Error('unsupported-template-or-parameters');
}
const topicFor = id => id.startsWith('temel-')?'temel':id.startsWith('sets-')?'sayilar-sayi-kumeleri':id.startsWith('natural-')?'sayilar-dogal-sayilar':id.startsWith('integer-')?'sayilar-tam-sayilar':id.startsWith('factorial-')?'sayilar-faktoriyel':id.startsWith('base-')?'sayilar-sayma-sistemleri':id.startsWith('division-')?'sayilar-bolme':id.startsWith('divisibility-')?'sayilar-bolunebilme-kurallari':null;
export function checkGeneratedQuestion(q) {
  try {
    const origin=q.origin;
    if(origin?.kind!=='template'||origin.templateVersion!==1||q.version!==1||q.id!==generatedId(origin.templateId,origin.parameters))return false;
    if(q.topicId!==topicFor(origin.templateId)||typeof q.text!=='string'||!q.text.trim()||!Array.isArray(q.steps)||!q.steps.length||!q.steps.every(s=>typeof s==='string'&&s.trim())||typeof q.formula!=='string'||!q.formula)return false;
    const expected=expectedAnswer(origin.templateId,origin.parameters);
    if(!Number.isSafeInteger(expected)||!Array.isArray(q.options)||q.options.length!==5||!q.options.every(s=>typeof s==='string'&&/^-?\d+$/.test(s)))return false;
    const options=q.options.map(Number);
    return options.every(Number.isSafeInteger)&&new Set(options).size===5&&Number.isInteger(q.answer)&&q.answer>=0&&q.answer<5&&options[q.answer]===expected&&options.filter(n=>n===expected).length===1;
  }catch{return false;}
}

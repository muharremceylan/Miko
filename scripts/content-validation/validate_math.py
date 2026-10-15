"""Özgün Temel Kavramlar sorularını bağımsız hesaplarla doğrular; uzman incelemesi yerine geçmez."""
import json
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'akademi_ai_prototip/content/kpss/lisans/matematik'
questions = json.loads((CONTENT / 'questions/temel.json').read_text())
lesson = json.loads((CONTENT / 'topics/temel.json').read_text())

def sole(values):
    unique = set(values)
    assert len(unique) == 1, unique
    return unique.pop()

def solve(number):
    if number == 1: return min(n for n in range(10,100) if n//10 != n%10)
    if number == 2: return sole(10*a+b for a in range(1,10) for b in range(10) if a+b==11 and a-b==3)
    if number == 3: return sole(a-b for a in range(1,10) for b in range(1,10) if 10*a+b-(10*b+a)==27)
    if number == 4: return min(2*a+3*b for a in range(1,10) for b in range(1,10) if a!=b)
    if number == 5: return (-3)**2-2*5
    if number == 6: return -4+3*(2-5)
    if number == 7: return -(-6)+(-2)*4
    if number == 8: return (-2)**4+(-3)**3
    if number == 9: return Fraction(36,3*2)+5
    if number == 10: return -(3**2)+(-3)**2
    if number == 11:
        # Parite polinomlarında tek sayının tüm kalıntı sınıfı (mod 2) kapsanır.
        indices=[i for i in range(5) if all([n+2,2*n+1,3*n+4,n+1,n*n][i]%2==0 for n in [-3,-1,1,3])]
        return ['n + 2','2n + 1','3n + 4','n + 1','n²'][sole(indices)]
    if number == 12:
        indices=[i for i in range(5) if all([a+b,a+1,a*b,2*a+b,b*b][i]%2==1 for a in [-3,-1,1,3] for b in [-2,0,2])]
        return ['a + b','a + 1','ab','2a + b','b²'][sole(indices)]
    if number == 13:
        indices=[i for i in range(5) if all([a*b,a+b,a*a+b*b,(a+b)**2,a-b][i]%2==0 for a in range(2) for b in range(2) if (a+b)%2)]
        return ['ab','a + b','a² + b²','(a + b)²','a − b'][sole(indices)]
    if number == 14:
        indices=[i for i in range(5) if all([a+b,a*b,a-b,2*a,2*b][i]%2==1 for a in [-3,-1,1,3] for b in [-3,-1,1,3])]
        return ['a + b','ab','a − b','2a','2b'][sole(indices)]
    if number == 15:
        assert all(b-abs(a)>0 for a in range(-20,0) for b in range(1,21) if a+b>0)
        return 'Pozitiftir'  # Sayısal örnek kontrolü; genel cebirsel gerekçe çözüm adımlarında.
    if number == 16:
        assert all(a*a>max(a,b,a*b,b*b) for a in range(-20,0) for b in range(a+1,0))
        return 'a²'  # Negatifler için genel ispat çözüm metninde.
    if number == 17: return sole(x for x in range(-100,101) if sum(range(x,x+3))==72)
    if number == 18: return sole(x+8 for x in range(-100,101,2) if sum(range(x,x+9,2))==130)
    if number == 19: return sole(x+6 for x in range(1,101,2) if sum(range(x,x+7,2))==80)
    if number == 20: return sum(range(7,28))
    if number == 21: return sum(range(1,21))
    if number == 22: return sum(range(1,24,2))
    if number == 23:
        # Polinom katsayıları: (x+1)(x+2) - x(x+3) = [2,3,1] - [0,3,1].
        coefficients=[a-b for a,b in zip([2,3,1],[0,3,1])]
        assert coefficients[1:]==[0,0]
        return coefficients[0]
    if number == 24: return max(a*b for a in range(1,14) for b in range(1,14) if a+b==14)
    if number == 25: return max(a*b for a in range(1,14) for b in range(1,14) if a+b==14 and a!=b)
    if number == 26: return min(a+b for a in range(1,6) for b in range(1,9) if 3*a+2*b==17)
    if number == 27: return sum(1 for a in range(7) for b in range(10) if 3*a+2*b==18)
    if number == 28: return max(a*b for a in range(-3,5) for b in range(-3,5) if a!=b)
    if number == 29: return sum(x for x in range(-3,6) if -2<x<=4)
    if number == 30: return min(a+b for a in range(1,37) for b in range(1,37) if a*b==36)
    raise AssertionError(number)

assert len(questions)==30 and len({q['id'] for q in questions})==30
assert len({q['text'] for q in questions})==30
for item in questions+lesson['examples']:
    assert len(item['options'])==len(set(item['options']))==5
    assert 0<=item['answer']<5 and item['steps'] and item['formula'] and item['topicId']=='temel'
    if item['id'].startswith('temel-'): expected=solve(int(item['id'].split('-')[1]))
    elif item['id']=='ornek-1': expected=5-2*(3-7)
    elif item['id']=='ornek-2': expected=sole(x for x in range(2,85,2) if x+(x+2)+(x+4)==84)
    else: expected=max(a*(18-a) for a in range(1,18) if a!=18-a)
    actual=item['options'][item['answer']]
    if isinstance(expected,(int,Fraction)): assert Fraction(actual)==expected,(item['id'],actual,expected)
    else: assert actual==expected,(item['id'],actual,expected)
assert set(lesson['summaries'])=={'quick','standard','detailed'}
assert len(lesson['sections'])==9 and len(lesson['formulas'])==8 and lesson['audioScript']
print('30 test sorusu ve 3 ayrı çözümlü örnek: beş seçenek, benzersizlik, doğru cevap ve bağımsız matematik kontrolleri geçti. Uzman onayı değildir.')

# Yeni içerik: kısıtlı ifadeler, tam sayı kümeleri ve bölme bağıntısı ile ayrı hesap.
# eval kullanılmaz. Soru yazarı tarafından verilen cevap hesap sonucuyla karşılaştırılır.
import ast
import math
import operator
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow}
CMP={ast.Eq:operator.eq,ast.NotEq:operator.ne,ast.Gt:operator.gt,ast.GtE:operator.ge,ast.Lt:operator.lt,ast.LtE:operator.le,ast.In:lambda a,b:a in b,ast.NotIn:lambda a,b:a not in b}
def calculate(source,x=None):
    def visit(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,bool)):return Fraction(n.value)
        if isinstance(n,ast.Name) and n.id=='x' and x is not None:return Fraction(x)
        if isinstance(n,ast.List):return [visit(t) for t in n.elts]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):return -visit(n.operand) if isinstance(n.op,ast.USub) else visit(n.operand)
        if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](visit(n.left),visit(n.right))
        if isinstance(n,ast.BoolOp):return (all if isinstance(n.op,ast.And) else any)(visit(t) for t in n.values)
        if isinstance(n,ast.Compare):
            vals=[visit(n.left)]+[visit(t) for t in n.comparators]
            return all(CMP[type(op)](a,b) for op,a,b in zip(n.ops,vals,vals[1:]))
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name):
            args=[visit(a) for a in n.args]
            if n.func.id=='factorial':return math.factorial(int(args[0]))
            if n.func.id=='range':return range(*map(int,args))
            if n.func.id=='sum':return sum(args[0])
        raise AssertionError(ast.dump(n))
    return visit(ast.parse(source,mode='eval').body)
def verified(check):
    kind,args=check['kind'],check['args']
    if kind=='expression':return calculate(args)
    if kind=='count':
        start,stop,pred=args
        return sum(bool(calculate(pred,x)) for x in range(int(start),int(stop)+1))
    if kind=='base':
        a,b,total=args
        return sole(t for t in range(max(a,b)+1,100) if a*t+b==total)
    if kind=='factorial_inverse':return sole(n for n in range(15) if math.factorial(n)==args)
    if kind=='digit':
        base,place,divisor=args
        return sole(d for d in range(10) if (base+place*d)%divisor==0)
    if kind=='remainder':return args[0]%args[1]
    if kind=='quotient':return args[0]//args[1]
    if kind=='dividend':
        b,q,r=args
        assert 0<=r<b
        return b*q+r
    raise AssertionError(kind)
package=json.loads((CONTENT/'topics/sayilar.json').read_text())
new_questions=[];new_examples=[]
for tid,l in package['lessons'].items():
    bank=json.loads((CONTENT/'questions'/f'{tid}.json').read_text())
    assert len(bank)==10 and len(l['examples'])==2
    assert len(l['sections'])==len(l['memoryNotes'])==4
    assert l['topicId']==tid and l['learningReady'] and len(l['formulas'])>=2
    assert set(l['summaries'])=={'quick','standard','detailed'}
    for level in ['standard','detailed']:
        summary=l['summaries'][level]
        assert len(summary['paragraphs'])==len(summary['headings'])==len(summary['noteIndices'])
        assert all(0<=i<len(l['memoryNotes']) for i in summary['noteIndices'])
    for card in l['memoryNotes']:assert all(card.get(k) for k in ['key','tip','example','warning','question','answer'])
    audio=package['audio'][tid]
    assert audio['topicId']==tid and audio['version']==l['version']
    assert set(audio['summaries'])=={'quick','standard','detailed'}
    assert all(100<len(text)<=4096 for text in audio['summaries'].values())
    for item in bank+l['examples']:
        assert item['topicId']==tid
        assert len(item['options'])==len(set(item['options']))==5
        assert item['steps'] and item['formula'] and item['reviewStatus']=='demo-math-checked'
        actual=Fraction(item['options'][item['answer']])
        expected=verified(item['verification'])
        assert actual==expected,(item['id'],actual,expected)
    new_questions+=bank;new_examples+=l['examples']
all_items=questions+lesson['examples']+new_questions+new_examples
assert len({q['id'] for q in all_items})==len(all_items)
assert len({q['text'] for q in all_items})==len(all_items)
assert len(package['lessons'])==7 and len(new_questions)==70 and len(new_examples)==14
print('Sayılar: 7 alt konu, 70 test sorusu ve 14 ayrı örnek; bağımsız işlem, küme, taban, bölme ve ses metni kontrolleri geçti.')

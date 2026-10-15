"""Sınırlı sayısal eşitlik kontrolü; genel matematik ispatı değildir. eval kullanılmaz."""
import ast
from fractions import Fraction

class NotNumeric(Exception):
    pass

def number(node, depth=0):
    if depth>12:raise NotNumeric()
    if isinstance(node,ast.Constant) and type(node.value) in (int,float):
        value=Fraction(str(node.value))
    elif isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
        value=number(node.operand,depth+1)*(-1 if isinstance(node.op,ast.USub) else 1)
    elif isinstance(node,ast.BinOp):
        a,b=number(node.left,depth+1),number(node.right,depth+1)
        if isinstance(node.op,ast.Add):value=a+b
        elif isinstance(node.op,ast.Sub):value=a-b
        elif isinstance(node.op,ast.Mult):value=a*b
        elif isinstance(node.op,ast.Div):value=a/b
        elif isinstance(node.op,ast.Pow) and b.denominator==1 and abs(b)<=8:value=a**int(b)
        else:raise NotNumeric()
    else:raise NotNumeric()
    if abs(value)>10**9 or value.denominator>10**6:raise NotNumeric()
    return value

def check_equation(text):
    if len(text)>120 or text.count('=')!=1:return 'not_checked'
    text=text.replace('×','*').replace('÷','/').replace('−','-').replace('²','**2').replace('³','**3')
    try:
        trees=[ast.parse(part.strip(),mode='eval') for part in text.split('=')]
        if any(sum(1 for _ in ast.walk(tree))>40 for tree in trees):return 'not_checked'
        values=[number(tree.body) for tree in trees]
        return 'passed' if values[0]==values[1] else 'mismatch'
    except (SyntaxError,ValueError,ZeroDivisionError,OverflowError,NotNumeric,RecursionError):return 'not_checked'

def verify(solution):
    checks=[{'step':i+1,'status':check_equation(step.calculation)} for i,step in enumerate(solution.steps)]
    status='inconsistent' if any(c['status']=='mismatch' for c in checks) else 'partial' if any(c['status']=='passed' for c in checks) else 'not_verified'
    return {'status':status,'checks':checks,'expert_approved':False}

def isEmpty(stack):
    return True if len(stack) == 0 else False


def peek(stack):
    return stack[-1]


def hasLessOrEqualPriority(a, b):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    if b == '':
        return True
    x = precedence[a] <= precedence[b]
    return x

     
def initial_expression(expression):
    temp = ''
    l = []
    for i in expression:
        if i.isnumeric():
            temp = temp + i
        elif i == ' ':
            continue
        else:
            l.append(temp)
            temp = ''
            l.append(i)
    if temp:
        l.append(temp)
    return l


def toPostfix(infix):
    stack = []
    postfix = []
    for c in range(len(infix)):
        if infix[c].isnumeric():
            postfix.append(infix[c])
        else:
            while (not isEmpty(stack)) and hasLessOrEqualPriority(infix[c], peek(stack)):
                postfix.append(stack.pop())
            stack.append(infix[c])

    while not isEmpty(stack):
        postfix.append(stack.pop())
    return postfix


def calc(val2, i, val1):
    if i == "+":
        return float(val2) + float(val1)
    elif i == '-':
        return float(val2) - float(val1)
    elif i == '*':
        return float(val2) * float(val1)
    elif i == '/':
        return float(val2) / float(val1)


def evalPostfix(postfix):
    stack = []
    for i in postfix:
        if i.isnumeric():
            stack.append(i)
        else:
            val1 = stack.pop()
            val2 = stack.pop()
            stack.append(calc(val2, i, val1))
    return stack[0]


def calculate(exp):
    exp_v1 = initial_expression(exp)
    exp_v2 = toPostfix(exp_v1)
    final = evalPostfix(exp_v2)
    return final

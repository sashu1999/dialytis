def math_expression_generator(arr):
    op = {
        10,  # = "/"
        11,  # = "+"
        12,  # = "-"
        13  # = "*"
    }

    m_exp = []
    temp = []

    'creating a list separating all elements'
    for item in arr:
        if item not in op:
            temp.append(item)
        else:
            m_exp.append(temp)
            m_exp.append(item)
            temp = []
    if temp:
        m_exp.append(temp)

    'converting the elements to numbers and operators'
    i = 0
    num = 0
    for item in m_exp:
        if type(item) == list:
            if not item:
                m_exp[i] = ""
                i = i + 1
            else:
                num_len = len(item)
                for digit in item:
                    num_len = num_len - 1
                    num = num + ((10 ** num_len) * digit)
                m_exp[i] = str(num)
                num = 0
                i = i + 1
        else:
            m_exp[i] = str(item)
            m_exp[i] = m_exp[i].replace("10", "/")
            m_exp[i] = m_exp[i].replace("11", "+")
            m_exp[i] = m_exp[i].replace("12", "-")
            m_exp[i] = m_exp[i].replace("13", "*")

            i = i + 1

    'joining the list of strings to create the mathematical expression'
    separator = ' '
    m_exp_str = separator.join(m_exp)

    return (m_exp_str)

def caluclate(eq):
    while True:
        try:
            answer = eval(eq)  # evaluating the answer
            answer = round(answer, 2)
            equation = eq + " = " + str(answer)
            return [1,eq,answer]
            break

        except SyntaxError:
            return [0,eq,"Invalid"]
            break

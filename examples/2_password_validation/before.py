q1 = 'QWERTYUIOPASDFGHJKLZXCVBNM'  # fixme есть string.ascii_uppercase
q2 = 'qwertyuiopasdfghjklzxcvbnm'
q3 = '!@#$%&*+'
q4 = '1234567890'

def q(q, s):
    f = False
    for S in s:
        for Q in q:  # fixme в этом цикле нет необходимости
            if(S == Q):
                f = True
                s = s.replace(Q, "")
    return f, s

print("Введите число количества паролей:")
flag = True  # fixme не нужен
while (flag):
    try:
        n = int(input())
        flag = False
    except:
        print("Введено не число")
        print("Повторите ввод:")

for i in range(n):
    print("Введите пароль:")
    s = input()
    F = True
    if(len(s) < 12):
        F = False
    if (F):
        F, s = q(q1, s)
    if (F):
        F, s = q(q2, s)
    if (F):
        F, s = q(q3, s)
    if (F):
        F, s = q(q4, s)
    if (len(s) > 0):
        F = False
    if (F):
        print('Valid')
    else:
        print('Invalid')

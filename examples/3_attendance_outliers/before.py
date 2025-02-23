import math
print("Введите количество пар, на которых отмечалось посещаемость:")
flag = True
while (flag):
  try:
    N = int(input())
    flag = False
  except:
    print("Введено не число")
    print("Повторите ввод:")
s = []
for i in range(0, N):
  print("Введите посещаемость на " + str(i + 1) + " паре:")
  flag = True
  while (flag):
    try:
      s.append(int(input()))
      flag = False
    except:
      print("Введено не число")
      print("Повторите ввод:")

s.sort()

def q (s):
    N = len(s)
    if (N % 2 == 0):
        return (s[int(N / 2)] + s[int(N / 2 - 1)]) / 2  # int(a / 2) == a // 2
    else:
        return s[int((N - 1) / 2)]

s1 = s[0 : int(N / 2)]
s2 = s[math.ceil(N / 2) : N]
q1 = q(s1)
q3 = q(s2)
kmin = q1 - 1.5 * (q3 - q1)
kmax = q3 + 1.5 * (q3 - q1)
Q = 0
for i in range(0, N):
    if(s[i] < kmin or s[i] > kmax):
        Q += 1
print("Количество отмеченых пар, которые можно считать некоректными: " + str(Q))

st = str(input("Введите сообщение: "))
s1 = ''
k = 1

for i in range(0,len(st)-1):
    if st[i]==st[i+1]:
        k+=1
    else:
        if k==1:
            s1+=st[i]
        else:
            s1+=str(k)+st[i]
            k=1

if k>1:
    s1+=str(k)+st[-1]
else:
    s1+=st[-1]

print("Сжатое сообщение", s1)
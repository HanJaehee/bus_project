tmp = [0]*24
print(tmp)
b = []
for i in range(5):
    b.append(tmp)
c = b[:]
c[0] = 24
print(b)
print(c)
# coding: utf-8
import re

f = open("test.csv","r",encoding="utf-8")

headers = re.split(r';|\n',f.readline())
headers.pop()
notas = []
func = ""
nota = 0

def funcDef(func,notas):
    n = len(notas)
    total = 0
    if func == "sum":
        for i in range(n):
            total = total + notas[i]
    elif func == "avg":
        total = funcDef("sum",notas)/len(notas)
    elif func == "max":
        total = max(notas)
    elif func == "min":
        total = min(notas)
    else:
        total = -1
    return total

for line in f:
    i = 4
    res = re.split(r'\W+',line)
    res.pop()

    aux = re.split(r'\*|\n',headers[3]) 

    if '*' in headers[3]:
        aux = re.split(r'\*|\n',headers[3])

        if aux[len(aux)-1] == '':
            aux.pop()
            func = aux[0]
            i = 4
            while i < len(res):
                notas.append(int(res[i]))
                i = i+1
        else:
            func = aux[0] + aux[1]
            i = 4
            while i < len(res):
                notas.append(int(res[i]))
                i = i+1
            nota = funcDef(aux[1],notas)
    else:
        func = headers[3]

print("]")
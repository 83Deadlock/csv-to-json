# coding: utf-8
import re
import sys

file_name = sys.argv[1]

f = open(file_name,"r",encoding="utf-8")
json = open("result.json","w")

fLines = f.readlines()
output = 0

headers = re.split(r';|\n',fLines[0])
headers.pop()
notas = []
func = ""
nota = 0

json.write("[")

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

def printJson(headers,values,func,nota):
    json.write("\n\t{")
    json.write(f"\n\t\t\"{headers[0]}\": \"{values[0]}\",")
    json.write(f"\n\t\t\"{headers[1]}\": \"{values[1]} {values[2]}\",")
    json.write(f"\n\t\t\"{headers[2]}\": \"{values[3]}\",")
    if(isinstance(nota,float)):
        fNota = "{:.2f}".format(nota)
        json.write(f"\n\t\t\"{func}\": {fNota}")    
    else:
        json.write(f"\n\t\t\"{func}\": {nota}")
    
    if len(fLines) == lines_checked:
        json.write("\n\t}")
    else:
        json.write("\n\t},")

fLines.pop(0)

lines_checked = 0

for line in fLines:
    lines_checked = lines_checked + 1
    values = []
    notas = []
    i = 4
    values = re.split(r'\W+',line)
    values.pop()

    aux = re.split(r'\*|\n',headers[3]) 

    if '*' in headers[3]:
        aux = re.split(r'\*|\n',headers[3])

        if aux[len(aux)-1] == '':
            aux.pop()
            func = aux[0]
            i = 4
            while i < len(values):
                notas.append(int(values[i]))
                i = i+1
            printJson(headers,values,func,notas)
        else:
            func = aux[0] + '_' + aux[1]
            i = 4
            while i < len(values):
                notas.append(int(values[i]))
                i = i+1
            printJson(headers,values,func,funcDef(aux[1],notas))
    else:
        func = headers[3]
        printJson(headers,values,func,notas)

json.write("\n]")
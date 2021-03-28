# coding: utf-8
import re
import sys

file_name = sys.argv[1] # Gets name of .csv file to be converted

f = open(file_name,"r",encoding="utf-8")    # Opens the file with permissions to read
json = open("result.json","w",encoding="utf-8") # Opens/Creates the output file with permissions to write

fLines = f.readlines()                      # Read every line to a list       

headers = re.split(r';|\n',fLines[0])       # The first line contains the headers for the rest of the data
headers.pop()                               # Last item captured is an empty string, we could just leave it, wouldn't make any trouble
notas = []                                  # List of grades read from each line read from the file
func = ""                                   # Function to be executed on the list of grades we read
nota = 0                                    # Result of the function executed on the list

json.write("[")                             # Every JSON file begins with an opening square bracket and ends with a closing square bracket

# Given a function and a list of grades, execute the given function on the list and returns the result (or -1 if it is an invalid function)
# Functions allowed as of the moment of implementation: max,min,avg,sum
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

# We can trat each line on .csv file as a block of information on .json files. This function will print each block.
def printJson(headers,values,func,nota):
    json.write("\n\t{")
    json.write(f"\n\t\t\"{headers[0]}\": \"{values[0]}\",")
    json.write(f"\n\t\t\"{headers[1]}\": \"{values[1]} {values[2]}\",")
    json.write(f"\n\t\t\"{headers[2]}\": \"{values[3]}\",")
    if(isinstance(nota,float)):                 # There's a possiblity that the function called returns a float value, in which case we limit the decimal points to 2
        fNota = "{:.2f}".format(nota)
        json.write(f"\n\t\t\"{func}\": {fNota}")    
    else:
        json.write(f"\n\t\t\"{func}\": {nota}")
    
    if len(fLines) == lines_checked:            #Each block of information is followed by a comma, except the last one
        json.write("\n\t}")
    else:
        json.write("\n\t},")

fLines.pop(0)      #After reading the values of the first line to determine our headers, we remove that line from our list of strings (where each string is a line from the file)

lines_checked = 0   # Number of lines we checked -> we use this number in the print function to know if the current line is the last one

for line in fLines:
    lines_checked = lines_checked + 1
    values = []     #reset the list of values
    notas = []      #reset the list of grades
    i = 4           #index where grades start to be shown after we split the string

    values = re.split(r'\W+',line)
    values.pop()    # Last item captured is an empty string, in this case it would make things a bit harder

    if '*' in headers[3]:               # Treat input as a list
        aux = re.split(r'\*|\n',headers[3]) # To know the function to be executed we must separate the two strings by the char '*' 

        if aux[len(aux)-1] == '':       # Case where Function is "notas*" which is to simply display the list of grades read
            aux.pop()
            func = aux[0]
            i = 4
            while i < len(values):
                notas.append(int(values[i]))
                i = i+1
            printJson(headers,values,func,notas)
        else:
            func = aux[0] + '_' + aux[1] # Case where Function is either "notas*avg", "notas*sum", "notas*min" or "notas*max"
            i = 4
            while i < len(values):
                notas.append(int(values[i]))
                i = i+1
            printJson(headers,values,func,funcDef(aux[1],notas))
    else:                               # Treat input as an integer 
        func = headers[3]
        printJson(headers,values,func,notas)

json.write("\n]")
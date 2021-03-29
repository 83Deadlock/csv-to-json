# coding: utf-8
import re
import sys

file_name = sys.argv[1] # Gets name of .csv file to be converted

f = open(file_name,"r",encoding="utf-8")    # Opens the file with permissions to read

fileOutName = re.sub(r"\.csv",".json",file_name)
json = open(fileOutName,"w",encoding="utf-8") # Opens/Creates the output file with permissions to write

fLines = f.readlines()                      # Read every line to a list       

headers = re.split(r';|\n',fLines[0])       # The first line contains the headers for the rest of the data
headers.pop()                               # Last item captured is an empty string, we could just leave it, wouldn't make any trouble

listsIndex = []
headers_size = len(headers)
for i in range(headers_size):
    if '*' in headers[i]:
        listsIndex.append(i)

fLines.pop(0)       # After knowing the headers, we can remove the first line 
lines_checked = 0   # Number of lines we checked -> we use this number in the print function to know if the current line is the last one
lines_total = len(fLines)   # Total number of lines on the file

for i in range(headers_size):
    headers[i] = re.sub('\*','_',headers[i])

# Given a function and a list of grades, execute the given function on the list and returns the result (or -1 if it is an invalid function)
# Functions allowed as of the moment of implementation: max,min,avg,sum
def funcDef(func,listArg):
    if listArg is str:
        return listArg
    n = len(listArg)
    total = 0
    if func == "sum":
        for i in range(n):
            total = total + listArg[i]
    elif func == "avg":
        total = funcDef("sum",listArg)/len(listArg)
    elif func == "max":
        total = max(listArg)
    elif func == "min":
        total = min(listArg)
    else:
        total = -1
    return total

# We can trat each line on .csv file as a block of information on .json files. This function will print each block.
def printJson(headers,values):
    json.write("\n\t{")
    
    for i in range(headers_size):
        if i + 1 == len(headers):
            if(isinstance(values[i],float)):                 # There's a possiblity that the function called returns a float value, in which case we limit the decimal points to 2
                fNota = "{:.2f}".format(values[i])
                json.write(f"\n\t\t\"{headers[i]}\": {fNota}")    
            elif(isinstance(values[i], int) or isinstance(values[i], list)):
                json.write(f"\n\t\t\"{headers[i]}\": {values[i]}")
            else:
                json.write(f"\n\t\t\"{headers[i]}\": \"{values[i]}\"")
        else:
            if(isinstance(values[i],float)):                 # There's a possiblity that the function called returns a float value, in which case we limit the decimal points to 2
                fNota = "{:.2f}".format(values[i])
                json.write(f"\n\t\t\"{headers[i]}\": {fNota},")    
            elif(isinstance(values[i], int) or isinstance(values[i], list)):
                json.write(f"\n\t\t\"{headers[i]}\": {values[i]},")
            else:
                json.write(f"\n\t\t\"{headers[i]}\": \"{values[i]}\",")
        
        
    if len(fLines) == lines_checked:            #Each block of information is followed by a comma, except the last one
        json.write("\n\t}")
    else:
        json.write("\n\t},")

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def RepresentFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

json.write("[")                             # Every JSON file begins with an opening square bracket and ends with a closing square bracket

for i in range(lines_total):
    lines_checked = lines_checked + 1
    values = []
    values = re.split(r';|\n',fLines[i])
    if(values[len(values)-1] == ''):
        values.pop()
    
    for n in listsIndex:
        aux = re.split(r'\(|\)|\,',values[n])
        aux.pop()
        aux.pop(0)
        
        if '_' in headers[n]:
            funcs = re.split(r'_',headers[n])

            if(funcs[1] == ''):
                if RepresentsInt(aux[0]):
                    listInts = []
                    for index in range(len(aux)):
                        aux[index] = int(aux[index])
                elif RepresentFloat(aux[0]):
                    listFloats = []
                    for index in range(len(aux)):
                        aux[index] = float(aux[index])
                values[n] = aux
                
            else:
                if RepresentsInt(aux[0]):
                    listInts = []
                    for index in range(len(aux)):
                        aux[index] = int(aux[index])
                elif RepresentFloat(aux[0]):
                    listFloats = []
                    for index in range(len(aux)):
                        aux[index] = float(aux[index])
                else:
                    aux = "INVALID_INPUT"
                func = funcs[1]
                values[n] = funcDef(func, aux) 
            
    printJson(headers, values)
            
json.write("\n]")
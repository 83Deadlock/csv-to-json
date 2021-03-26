# coding: utf-8
import re

f = open("test.csv","r",encoding="utf-8")

headers = re.split(r'\W+',f.readline())

print("[")
for line in f:
    res = re.split(r'\W+',line)
    res.pop()
    print(res)

headers.pop()
print(headers)

print("]")
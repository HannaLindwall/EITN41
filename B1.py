from H0 import *
import fileinput


def luhnify(string):
    string = string[::-1]
    multiplier = 1
    val = 0
    multX = 0
    totalSum = 0
    x = 0
    for s in string:
      if(s!='X'):
         val = multiplier * hexaToInt(s)
         if(val>=10):
             val -= 9
         totalSum += val
      else:
         multX = multiplier
      if (multiplier==1):
          multiplier = 2
      else:
          multiplier = 1
    val = totalSum % 10
    dnom = 10 - val
    if (dnom==10):
        x=0
    else:
        if (dnom % 2 != 0 and multX==2):
            dnom += 9
        x = dnom / multX
    x = int(x)
    return str(x)

result = ""
for line in fileinput.input():
    result += luhnify(line.strip())
print(result)

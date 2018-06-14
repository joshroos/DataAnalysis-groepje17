import re
with open('corrcoef.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = re.findall(r"[-+]?\d*\.\d+|\d+", line)
       
        if float(value[0]) > 0.9:
            print(line)
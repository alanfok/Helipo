import os
files =[]
temp = []
tmpDic ={}

for dirpath, dirnames, filenames in os.walk('.'):
    for f in filenames:
        if '.txt' and 'invert' in f:
            files.append(f)
print(sorted(files))


simpleQuery = "during"





for file in files:
    fo = open(file, "r")
    for line in fo:
        key, value = line.split(":::")
        if key == simpleQuery:
            temp = (value.translate({ord(i): None for i in ",[\']"}).split())
            tmpDic = {key: temp}

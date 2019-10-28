import os
files =[]
initPosting = []
args = []


for dirpath, dirnames, filenames in os.walk('.'):
    for f in filenames:
        if '.txt' and 'invert' in f:
            files.append(f)
print(sorted(files))

simpleQuery = "Jimmy AND Carter"
#simpleQuery = "Green AND Party"
#simpleQuery = "Innovations AND in AND telecommunication"
#simpleQuery = "factors AND affecting AND liquidity"
#simpleQuery = "environmentalist OR ecologist"

args = simpleQuery.split()


if len(args) == 0:
    print("you missing a query")
elif len(args) == 1:
    for file in files:
        fo = open(file, "r")
        for line in fo:
            key, value = line.split(":::")
            if key == args[0]:
                initPosting = (value.translate({ord(i): None for i in ",[\']"}).split())
                initPosting = list(map(int, initPosting))
else:
    index = 0
    for word in args:
        if index == 0 :
            for file in files:
                fo = open(file, "r")
                for line in fo:
                    key, value = line.split(":::")
                    if key == args[0]:
                        initPosting = (value.translate({ord(i): None for i in ",[\']"}).split())
                        initPosting = list(map(int, initPosting))
            print(initPosting)
        if args[index] == "AND" and index > 0:
            tmp =[]
            for file in files:
                fo = open(file, "r")
                for line in fo:
                    key, value = line.split(":::")
                    if key == args[index+1]:
                        tmp = (value.translate({ord(i): None for i in ",[\']"}).split())
            tmp = list(map(int, tmp))
            print(tmp)
            print("i like u")
            print(initPosting)
            initPosting = list(set(initPosting).intersection(tmp))
        if args[index] == "OR" and index > 0:
            tmp=[]
            for file in files:
                fo = open(file, "r")
                for line in fo:
                    key, value = line.split(":::")
                    if key == args[index+1]:
                        tmp = (value.translate({ord(i): None for i in ",[\']"}).split())
            tmp = list(map(int, tmp))
            print(tmp)
            print("i hate u")
            print(initPosting)
            initPosting = list(set(initPosting) ^ set(tmp))
        index += 1

print(simpleQuery + str(sorted(initPosting)))




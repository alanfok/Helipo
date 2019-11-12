
import os
import ast
import math
import json
files =[]
initPosting = []
args = []
k1 = 1.8
b = 0.5

for dirpath, dirnames, filenames in os.walk('.'):
    for f in filenames:
        if '.txt' and 'invert' in f:
            files.append(f)
print(sorted(files))
N = 0
avg_len = 0
ld_dictionry ={}


#for ranking
fo = open("DocTemp.txt", "r")
for line in fo:
    key , value = line.split("<:::>")
    if key == "N":
        N = int(value)
    if key == "average_length":
        avg_len = float(value)

fo = open("ld.txt", "r")
for line in fo:
    key , value = line.split("<:::>")
    ld_dictionry[key] = value



#simpleQuery = "Jimmy AND Carter"
#simpleQuery = "Green AND Party"
#simpleQuery = "Innovations AND in AND telecommunication"
#simpleQuery = "factors AND affecting AND liquidity"
#simpleQuery = "environmentalist OR ecologist"


#simpleQuery = "Democrats AND welfare And and AND healthcare AND reform AND policies"
#simpleQuery = "Drug AND company AND bankruptcies"
#simpleQuery = "George AND Bush"
#simpleQuery = "Democrats OR welfare OR and OR healthcare OR reform OR policies"
#simpleQuery = "war OR death"
simpleQuery = "Drug OR company OR bankruptcies"
#simpleQuery = "George OR Bush"
#simpleQuery = "victory"


args = simpleQuery.split()
df = {}
queryArr= []

test = {}
if len(args) == 0:
    print("you missing a query")
elif len(args) == 1:
    for file in files:
        fo = open(file, "r")
        for line in fo:
            key, value = line.split(":::")
            #for v in value:
            if key == args[0]:
                queryArr.append(key)
                initPosting = (value.translate({ord(i): None for i in ",[\']"}).split())
                initPosting = list(map(int, initPosting))
                df[key] = len(initPosting)
else:
    index = 0
    for word in args:
        if index == 0 :
            for file in files:
                fo = open(file, "r")
                for line in fo:
                    key, value = line.split(":::")
                    if key == args[0]:
                        queryArr.append(key)
                        initPosting = (value.translate({ord(i): None for i in ",[\']"}).split())
                        initPosting = list(map(int, initPosting))
                        #df.append(len(initPosting))
                        df[key] = len(initPosting)
            print(initPosting)
        if args[index] == "AND" and index > 0:
            tmp =[]
            print(args[index+1])
            for file in files:
                fo = open(file, "r")
                for line in fo:
                    key, value = line.split(":::")
                    if key == args[index+1]:

                        queryArr.append(key)
                        tmp = (value.translate({ord(i): None for i in ",[\']"}).split())
                        df[args[index + 1]] = len(tmp)
                tmp = list(map(int, tmp))
            print(tmp)
            #df.append(len(tmp))
            df[args[index+1]] = len(tmp)
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
                        queryArr.append(key)
                        tmp = (value.translate({ord(i): None for i in ",[\']"}).split())
                        print(args[index+1])
                tmp = list(map(int, tmp))
            df[args[index+1]] = len(tmp)
            print(tmp)
            print("i hate u")
            print(initPosting)
            tempinitPosting = list(set(initPosting).intersection(tmp))
            initPosting = tempinitPosting + list(set(initPosting) ^ set(tmp))
        index += 1

print(simpleQuery + str(sorted(initPosting)))

print("################################################")
print(list(initPosting))
print("################################################")


BM25Score = {}
fre = {}
fo = open("tf.txt", "r")
for line in fo:
    key, value = line.split("<:::>")
    for number in list(initPosting):
        if str(key) == str(number):
            d = ast.literal_eval(str(value))
            score = 0.0
            arr=[]
            for query in queryArr:
                if query in d:
                    x = d[query]
                    tf = int(x)
                    y = query +" "+ str(tf)
                    arr.append(y)
                    # the formula from taxtbook 11.32
                    weight = ((k1 + 1) * tf) / (tf + k1 * (((1 - b) + b * (int(ld_dictionry[key]) / avg_len))))
                    idf = math.log((N) / (df[query]))
                    resultBM25 = (weight) * idf
                    print(str(key) + " " + query + " " + str(resultBM25))
                    score = score + resultBM25
            fre[key]=arr
            #print(str(key) + " " + str(score))
            BM25Score[key] = score

            '''
                tf = int(x)
                weight = ((k1 + 1) * tf) / (tf + k1 * (((1 - b) + b * (int(ld) / avg_len))))
                idf = math.log((N) / (df[query]))
                resultBM25 = (weight) * idf
                score = score + resultBM25

            BM25Score[key] = score

            for query in queryArr:
                if query in d:
                    tf = d[query]
                    weight = ((k1 + 1) * tf) / (tf + k1 * (((1 - b) + b * (ld / avg_len))))
                    idf = math.log((N) / (df[query]))
                    resultBM25 = (weight) * idf
                    score = score + resultBM25
            BM25Score[key] = score
            print(key + "  " + str(score))
            
            '''
#return the top 10 highest doc
print("################################################")
print(queryArr)
print("We calculation "+str(N))
print("the avg len "+str(avg_len))
print("We have "+ str(df) + " in all Document")
print("################################################")
print("Top 10 Document return")
BM25Scores = sorted(BM25Score ,key=BM25Score.get,  reverse=True)
top10 = 0
for doc in BM25Scores:
    top10 +=1
    print("TOP"+str(top10)+" : "+str(doc) +"   Score: "+ str(BM25Score[doc])+" Document Length "+str(int(ld_dictionry[doc]))+" "+str(fre[doc]))
    if top10 == 10:
        break


#print(df)
#print(N)
#print(avg_len)

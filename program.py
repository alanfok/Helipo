#https://stackoverflow.com/questions/10525867/extracting-tag-attributes-with-beautifulsoup
from bs4 import BeautifulSoup
from FileRetrival import FileRetrival
from Dictionary import Dictionary
from Merge import  Merge


import nltk
import string
import json
import os


files = []
secondFile = []
dictPost = {}
jsonFiles = []
fr = FileRetrival()
dic = Dictionary()

fr.retrivalSMGFile(files)

index = 0
blockNumber = 0
articleCount = 0
dictionary = {}

for fileName in sorted(files):
    f = open("reuters21578/"+fileName, "r", encoding="ISO-8859-1")
    data = f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll("reuters")
    for content in contents:
        newid = (content['newid'])
        if str(content.title) != "None":
            #print(newid)
            #print(content.title.text)

            tileTokens = nltk.word_tokenize((content.title.text).lower().translate({ord(i): None for i in string.punctuation}))
            #print(tileTokens)
            tileTokens = set(tileTokens)
            for tileToken in tileTokens:
                if not tileToken.isdigit():
                    if tileToken in dictionary:
                        dictionary[tileToken].append(newid)
                    else:
                        dictionary[tileToken] = [newid]
        if str(content.body) != "None":
            #tokens = str((content.body.text).translate({ord(i): None for i in '<>()/",.-&+\''})).lower().split()
            tokens = nltk.word_tokenize((content.body.text).lower().translate({ord(i): None for i in string.punctuation}))
            tokens = set(tokens)
            for token in tokens:
                if not token.isdigit():
                    if token in dictionary:
                        if newid not in dictionary[token]:
                            dictionary[token].append(newid)
                    else:
                        dictionary[token] = [newid]

        articleCount += 1
        if articleCount % 499 == 0:
            if not os.path.exists("./disk"):
                os.makedirs("./disk")
            dictionary.pop('\u0003', None)
            dictionary.pop('$', None)
            fileNameCreate = "./disk/block" + str(blockNumber) + ".json"
            print(fileNameCreate)
            jsonFiles.append(fileNameCreate)
            with open(fileNameCreate, 'w') as fp:
                json.dump(dictionary, fp, sort_keys=True)
            dictionary = {}
            blockNumber += 1

#check the last reminding
if(dictionary):
    dictionary.pop('\u0003', None)
    fileNameCreate = "./disk/block" + str(blockNumber) + ".json"
    jsonFiles.append(fileNameCreate)
    with open(fileNameCreate, 'w') as fp:
        json.dump(dictionary, fp, sort_keys=True)
    dictionary = {}

mergeDictionary={}
for jsonFile in jsonFiles:
    with open(jsonFile, 'r') as f:
        datastore = json.load(f)
        for key in datastore:
            if key in mergeDictionary:
                for newid in datastore[key]:
                    mergeDictionary[key].append(newid)
            else:
                idlist = []
                for newid in datastore[key]:
                    idlist.append(newid)
                mergeDictionary[key] = idlist

'''
with open('merged.json', 'w') as fp:
    json.dump(mergeDictionary, fp, sort_keys=True)
'''


blockNumber = 0
nbTerm = 0
nbPosting = 0
tempMergeDiction= {}
for key in sorted(mergeDictionary.keys()):
    nbPosting = nbPosting + len(mergeDictionary[key])
    tempMergeDiction[key] = mergeDictionary[key]
    nbTerm = nbTerm + 1
    if nbTerm % 24999 == 0:
        mergeCreatefile = "mergedBlock"+str(blockNumber)+".json"
        with open(mergeCreatefile, 'w') as fp:
            json.dump(tempMergeDiction, fp, sort_keys=True)
            blockNumber = blockNumber + 1
            tempMergeDiction = {}

if(tempMergeDiction):
    mergeCreatefile = "mergedBlock"+str(blockNumber)+".json"
    with open(mergeCreatefile, 'w') as fp:
        json.dump(tempMergeDiction, fp, sort_keys=True)
    tempMergeDiction = {}

print("Term"+ str(nbTerm))
print("Posting" + str(nbPosting))

#the Qeury
SimpleQeury = "offering AND increase"

SimpleQeuryArr = SimpleQeury.split()

mergeFiles = []
tempList = []

for dirpath, dirnames, filenames in os.walk('./'):
    for f in filenames:
        if 'mergedBlock' in f:
            mergeFiles.append(f)

if len(SimpleQeuryArr) == 1:
    for mergeFile in mergeFiles:
        with open(mergeFile, 'r') as f:
            datastore = json.load(f)
            for key in datastore:
                if key == SimpleQeuryArr[0]:
                    print(str(key)+":::"+str(datastore[key]))
elif len(SimpleQeuryArr):
    nbIndex = 0
    for mergeFile in mergeFiles:
        with open(mergeFile, 'r') as f:
            datastore = json.load(f)
            for key in datastore:
                if key == SimpleQeuryArr[0]:
                    tempList = datastore[key]
    for word in SimpleQeuryArr:
        print(word)
        if str(word) == "AND":
            for mergeFile in mergeFiles:
                with open(mergeFile, 'r') as f:
                    datastore = json.load(f)
                    for key in datastore:
                        if str(key) == SimpleQeuryArr[nbIndex + 1]:
                            print("I love train")
                            tempList = set(tempList).intersection(datastore[key])
        nbIndex += 1
    print(sorted(tempList))
else:
    print("it has not query")
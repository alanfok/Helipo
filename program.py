#https://stackoverflow.com/questions/10525867/extracting-tag-attributes-with-beautifulsoup
from bs4 import BeautifulSoup
from FileRetrival import FileRetrival
from Dictionary import Dictionary
import json
import os


files = []
id = []
secondFile = []
dictPost = {}
jsonFiles = []
fr = FileRetrival()
dic = Dictionary()



fr.retrivalSMGFile(files)


'''
#print(fileName)
for fileName in sorted(files):
    f = open(fileName, "r",encoding="ISO-8859-1")
    for line in f:
        for word in line.split():
            if "NEWID" in word:
                temp = word.translate({ord(i): None for i in 'NEWID=">'})
                id.append(temp)
'''
index = 0
blockNumber = 0
articleCount = 0
dictionary = {}
for fileName in sorted(files):
    f = open(fileName, "r", encoding="ISO-8859-1")
    data = f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll("reuters")
    for content in contents:
        newid = (content['newid'])
        if str(content.title) != "None":
            print(newid)
            print(content.title.text)
            tileTokens = str((content.title.text).translate({ord(i): None for i in '<>()/",.-&+\''})).split()
            tileTokens = set(tileTokens)
            for tileToken in tileTokens:
                if not tileToken.isdigit():
                    if tileToken in dictionary:
                        dictionary[tileToken].append(newid)
                    else:
                        dictionary[tileToken] = [newid]
        if str(content.body) != "None":
            tokens = str((content.body.text).translate({ord(i): None for i in '()/",.-&+\''})).split()
            tokens = set(tokens)
            for token in tokens:
                if not token.isdigit():
                    if token in dictionary:
                        dictionary[token].append(newid)
                    else:
                        dictionary[token] = [newid]
        #index += 1
        articleCount += 1
        if articleCount % 499 == 0:
            dictionary.pop('\u0003', None)
            fileNameCreate = "block" + str(blockNumber) + ".json"
            print(fileNameCreate)
            jsonFiles.append(fileNameCreate)
            with open(fileNameCreate, 'w') as fp:
                json.dump(dictionary, fp, sort_keys=True)
            dictionary = {}
            blockNumber += 1

mergeDictionary={}
for jsonFile in jsonFiles:
    print(jsonFile)
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


with open('merged.json', 'w') as fp:
    json.dump(mergeDictionary, fp, sort_keys=True)

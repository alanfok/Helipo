from bs4 import BeautifulSoup
from FileRetrival import FileRetrival
from Dictionary import Dictionary
import json

files = []
id = []
secondFile = []
dictPost = {}

fr = FileRetrival()
dic = Dictionary()



fr.retrivalSMGFile(files)



#print(fileName)
for fileName in sorted(files):
    f = open(fileName, "r",encoding="ISO-8859-1")
    for line in f:
        for word in line.split():
            if "NEWID" in word:
                temp = word.translate({ord(i): None for i in 'NEWID=">'})
                id.append(temp)

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
        if str(content.body) != "None":
            print(id[index])
            print(blockNumber)
            tokens = str(content.body.text).split()
            tokens = set(tokens)
            for token in tokens:
                if token in dictionary:
                    dictionary[token].append(id[index])
                else:
                    dictionary[token] = [id[index]]
        index += 1
        articleCount += 1
        if articleCount % 499 == 0:
            fileNameCreate = "block" + str(blockNumber) + ".json"
            print(fileNameCreate)
            with open(fileNameCreate, 'w') as fp:
                json.dump(dictionary, fp, sort_keys=True)
            dictionary = {}
            blockNumber += 1


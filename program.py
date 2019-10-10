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
print(files)

for fileName in files:
    print(fileName)
    f = open(fileName, "r",encoding="ISO-8859-1")
    for line in f:
        for word in line.split():
            if "NEWID" in word:
                temp = word.translate({ord(i): None for i in 'NEWID=">'})
                id.append(temp)

newIDListIndex = 0
blockNumber = 0
articleCount = 0
Dictionaryss = {}
for fileName in files:
    f = open(fileName, "r", encoding="ISO-8859-1")
    data = f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll('body')
    for content in contents:
        token = content.text.split()
        token.sort()
        token = set(token)
        for tokens in token:
            if tokens in Dictionaryss:
                Dictionaryss.get(tokens).append(str(id[newIDListIndex]))
            else:
                lists = []
                Dictionaryss[tokens] = [str(id[newIDListIndex])]
        newIDListIndex = newIDListIndex + 1
        articleCount = articleCount + 1
        if articleCount % 499 == 0:
            '''
            fileNameCreate = "block" + str(blockNumber) + ".xml"
            fa = open(fileNameCreate, "a")
            for key in sorted(Dictionaryss.keys()):
                fa.write("<TERM>"+key+"</TERM>"+"<NEWID>"+str(Dictionaryss[key])+"</NEWID>")
                '''
            fileNameCreate = "block" + str(blockNumber) + ".json"
            #fa = open(fileNameCreate, "a")
            with open(fileNameCreate, 'w') as fp:
                json.dump(Dictionaryss, fp)
            # json.dump(Dictionaryss, fa)
            Dictionaryss = {}
            blockNumber = blockNumber + 1

with open('block0.json') as json_file:
    data = json.load(json_file)
    print(data)
#with open('block0.txt', encoding='utf-8') as f:

#fr.retrivalTXTFile(secondFile)


#dic.createDictionaryIndex(secondFile[0])
'''        fileNameCreate = "block"+str(blockNumber)+".xml"
        fa = open(fileNameCreate,"a")
        fa.writelines("<NEWID>" + id[newIDListIndex]+"</NEWID>\n")
        fa.writelines("<BODY>"+content.text+"</BODY>\n")
        print("NEWID:" + id[newIDListIndex])
        print(content.text)
        newIDListIndex = newIDListIndex + 1
        articleCount = articleCount+1
        '''
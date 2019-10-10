from bs4 import BeautifulSoup


class Dictionary:

    def createDictionary(self, file):
        newidArr = []
        index = 0
        fe = open(file, "r", encoding="ISO-8859-1")
        data = fe.read()
        soup = BeautifulSoup(data)
        newid = soup.findAll('newid')
        for newids in newid:
            newidArr.append(newids.text)
        contents = soup.findAll('body')
        for content in contents:
            x = content.text.split()
            print(x)
            #print(str(newidArr[index])+" "+content.text+"\n")
            #print("========================================")
            index = index + 1

    def createDictionaryIndex(self, file):
        fe = open(file, "r", encoding="ISO-8859-1")
        data = fe.read()
        soup = BeautifulSoup(data)
        newid = soup.findAll('newid')
        for newids in newid:
            print(newids.text)


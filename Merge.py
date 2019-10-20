import json
import linecache


'''
https://www.tutorialspoint.com/random-access-to-text-lines-in-python-linecache
'''
class Merge:
    fullBufferReader = []
    lineCounting = []
    file = []
    indexWillUpdate = []
    term = ""
    postingList =[]
    invertDictionary = {}
    stopARR = []
    docLength = []
    max = 0
    theLastword =""


    def mergeInit(self, file ,stopARR,max):
        self.stopARR = stopARR
        self.max = max
        i = 1
        j = 0
        for fileName in file:
            fo = open(fileName, "r")
            for line in fo:
                if i == j:
                    self.file.append(fileName)
                    self.lineCounting.append(0)
                    self.fullBufferReader.append(line[0:len(line)-1])
                    break
                else:
                    j += 1

    def run(self):
        int = 0
        block = 0
        while True:
            #temp= []
            tempHeader = []
            tempPosting = []
            #for key in self.fullBufferReader:
                #temp.append(key[0:len(key)-1])
            #print(temp)
            for k in self.fullBufferReader:
                key, value = k.split(":::")
                #print(key)
                #print(value)
                tempHeader.append(key)
                tempPosting.append(value)
                #print(tempHeader)
                #print(tempPosting)
            int += 1

            minKey = min(tempHeader);
            if minKey == "zzzzzzzzzzzzzz----":
                break
            else:
                self.term = minKey
            #print(tempHeader)
            #print(tempPosting)
            self.indexWillUpdate = [i for i, n in enumerate(tempHeader) if n == minKey]
            for index in self.indexWillUpdate:
                tmp = tempPosting[index]
                #tmpList = tmp.translate({ord(i): None for i in ",[\']"}).split()
                if self.term in self.invertDictionary:
                    for num in tmp.translate({ord(i): None for i in ",[\']"}).split():
                        self.invertDictionary[self.term].append(num)
                else:
                    self.invertDictionary[self.term] = tmp.translate({ord(i): None for i in ",[\']"}).split()

                self.lineCounting[index] = self.lineCounting[index] + 1
                if self.lineCounting[index] < self.stopARR[index]:
                    line = linecache.getline(self.file[index], self.lineCounting[index]+1)
                    #print(line)
                    self.fullBufferReader[index] = line
                '''
                self.lineCounting[index] = self.lineCounting[index] + 1
                fo = open(self.file[index], "r")
                for i, line in enumerate(fo):
                    if i == self.lineCounting[index] and self.lineCounting[index] < self.stopARR[index]:
                        self.fullBufferReader[index] = line
'''
            #print(self.fullBufferReader)
            print(int)
            fp = open("log"+str(block)+".txt", 'a')
            fp.write(str(self.fullBufferReader)+"\n")
            if int % 4999 == 0:
                block += 1
        #print(self.stopARR)
        #print(self.invertDictionary)
        fp = open("inverst.txt", 'a')
        for key in self.invertDictionary:
            fp.write(str(key)+str(self.invertDictionary[key])+"\n")

    '''
      
            self.updateIndexBuffer(tempHeader)
            self.updateALL(tempPosting)
            self.update_dictionary()
            #print("dictionary")
            #print(self.invertDictionary)
            self.postingList = []
            with open("log"+str(block)+".txt", 'a') as fp:
                fp.write(str(int)+"_->"+str(self.fullBufferReader)+"\n")
            print(int)
            #print(str(self.invertDictionary))
            #print(self.stopArr)
            #print(self.fullBufferReader)
            int += 1
            if int % 24999 == 0:
                with open("invertDic"+str(block)+".json", 'w') as fp:
                    json.dump(self.invertDictionary, fp, sort_keys=True)
                block += 1
            print(self.indexWillUpdate)
            for num in self.indexWillUpdate:
                print(self.file[num])
            self.updataLineCounter()
            print("ssss")
            print(self.lineCounting)
            print("tttt")
            self.upadateFullfullBufferReader()
            self.updataPostingList(tempPosting)
            print(self.postingList)
            self.update_dictionary()
            print(self.invertDictionary)
            self.postingList = []
            int += 1
        '''


    def updateIndexBuffer(self, lst):
        self.indexWillUpdate.clear()
        self.term = min(lst)
        index = 0
        for word in lst:
            if str(word) == str(min(lst)):
                self.indexWillUpdate.append(index)
            index += 1

    def updateALL(self, posting):
        for num in self.indexWillUpdate:
            tmp = self.lineCounting[num]
            tmp += 1
            self.lineCounting[num] = tmp
            tmp = posting[num].translate({ord(i): None for i in "[']"})
            tmp2 = tmp.split();
            for num2 in tmp2:
                self.postingList.append(num2)
            fo = open(self.file[num], "r")
            #print(fo)
            i = 0
            for line in fo:
                if i == self.lineCounting[num] and i <self.stopARR[num]:
                   # print("line" + line)
                    #print("before")
                    #print(self.fullBufferReader)
                    self.fullBufferReader[num] = line
                    #print("after")
                    #print(self.fullBufferReader)
                    break
                else:
                        i += 1

    def updataLineCounter(self):
        for num in self.indexWillUpdate:
            tmp = self.lineCounting[num]
            tmp += 1
            self.lineCounting[num] = tmp

    def updataPostingList(self, lst):
        for num in self.indexWillUpdate:
            tmp = lst[num].translate({ord(i): None for i in "[']"})
            tmp2 = tmp.split();
            for num2 in tmp2:
                self.postingList.append(num2)

    def upadateFullfullBufferReader(self):
        for num in self.indexWillUpdate:
            fo = open(self.file[num], "r")
            print(fo)
            i = 0
            for line in fo:
                if i == self.lineCounting[num]:
                    print("before")
                    print(self.fullBufferReader)
                    self.fullBufferReader[num] = line
                    print("after")
                    print(self.fullBufferReader)
                    break
                else:
                    i += 1

    def update_dictionary(self):
        if self.term in self.invertDictionary:
                for post in self.postingList:
                    self.invertDictionary[self.term].append(post)
        else:
            self.invertDictionary[self.term] = self.postingList

    '''
i = 3
fo = open("./disk/block0.txt", "r")
j = 0
for line in fo:
    j += 1
    print(line)
    if j == i:
        break

# Assuming file has following 5 lines
# This is 1st line
# This is 2nd line
# This is 3rd line
# This is 4th line
# This is 5th line

line = fo.readline()
print ("Read Line: %s" % (line))

line = fo.readline(1)
print ("Read Line: %s" % (line))

# Close opend file
fo.close()
'''
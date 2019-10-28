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
    invertDictionaryCounter = {}
    stopARR = []
    docLength = []
    max = 0


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
        invertblock = 0
        term = 0
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
            if int % 25000 == 0:
                fp = open("invert" +str(invertblock)+ ".txt", 'a')
                for key in self.invertDictionary:
                    fp.write(str(key) +":::"+ str(self.invertDictionary[key]) + "\n")
                self.invertDictionary = {}
                invertblock +=1
            minKey = min(tempHeader);
            if minKey == "zzzzzzzzzzzzzz----":
                break
            else:
                self.term = minKey
            self.indexWillUpdate = [i for i, n in enumerate(tempHeader) if n == minKey]
            for index in self.indexWillUpdate:
                tmp = tempPosting[index]
                #tmpList = tmp.translate({ord(i): None for i in ",[\']"}).split()
                if self.term in self.invertDictionary:
                    for num in tmp.translate({ord(i): None for i in ",[\']"}).split():
                        self.invertDictionary[self.term].append(num)
                        self.invertDictionaryCounter[self.term].append(num)
                else:
                    self.invertDictionary[self.term] = tmp.translate({ord(i): None for i in ",[\']"}).split()
                    self.invertDictionaryCounter[self.term] = tmp.translate({ord(i): None for i in ",[\']"}).split()

                self.lineCounting[index] = self.lineCounting[index] + 1
                if self.lineCounting[index] < self.stopARR[index]:
                    line = linecache.getline(self.file[index], self.lineCounting[index]+1)
                    #print(line)
                    self.fullBufferReader[index] = line
            print(int)
            fp = open("log"+str(block)+".txt", 'a')
            fp.write(str(self.fullBufferReader)+"\n")
            if int % 4999 == 0:
                block += 1


        if(self.invertDictionary):
            fp = open("invert" + str(invertblock) + ".txt", 'a')
            for key in self.invertDictionary:
                fp.write(str(key) + ":::"+str(self.invertDictionary[key]) + "\n")
            self.invertDictionary = {}

        term = 0
        leng = 0
        for key in self.invertDictionaryCounter:
            term = term +1
            leng = leng + len(self.invertDictionaryCounter[key])

        print("term has " + str(term) +" and " +str(leng))

    '''
      
      if(dictionary):
    dictionary.pop('\u0003', None)
    fileNameCreate = "./disk/block"+ str(blockNumber) +".txt"
    fileLists.append(fileNameCreate)
    with open(fileNameCreate, 'a') as fp:
        #json.dump(dictionary, fp, sort_keys=True)
        keyArr = sorted(dictionary)
        #stopArr.append(max(keyArr))
        #stopArr.append(str(max(keyArr) + ":" + str(dictionary[max(keyArr)])+"\n"))
        for key in keyArr:
            fp.write(str(key) + ":::" + str(dictionary[key])+"\n")
        fp.write("zzzzzzzzzzzzzz----:::[]")
    dictionary = {}
    print(fileNameCreate)
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
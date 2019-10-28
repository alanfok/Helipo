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
        n_index = 0
        block = 0
        invertblock = 0
        while True:
            tempHeader = []
            tempPosting = []
            for k in self.fullBufferReader:
                key, value = k.split(":::")

                tempHeader.append(key)
                tempPosting.append(value)
            n_index += 1
            if n_index % 25000 == 0:
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
            print(n_index)
            fp = open("log"+str(block)+".txt", 'a')
            fp.write(str(self.fullBufferReader)+"\n")
            if n_index % 4999 == 0:
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

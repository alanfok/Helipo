import linecache


'''
https://www.tutorialspoint.com/random-access-to-text-lines-in-python-linecache
'''
class Merge:
    fullBufferReader = [] #buffer
    lineCounting = [] #to track which line we need to read in the text file
    file = [] #contain the file name , e.g [block0.txt, block1.txt]
    indexWillUpdate = [] #to track which index in lineCounting and fullbufferReader that need to update
    term = "" #the smallest term
    invertDictionary = {} #invert index
    invertDictionaryCounter = {} # backup invert index, use to create the report table
    stopARR = [] # lenght for all the bock
    max = 0


    def mergeInit(self, file ,stopARR,max): #put all blocks first line into buffer
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
            minKey = min(tempHeader) #find the smallest term in the buffer
            if minKey == "zzzzzzzzzzzzzz----": # hit the bottom in all the blocks , then break the while loop
                break
            else:
                self.term = minKey
            self.indexWillUpdate = [i for i, n in enumerate(tempHeader) if n == minKey] #find the index that it has to update
            for index in self.indexWillUpdate:
                tmp = tempPosting[index]
                if self.term in self.invertDictionary:
                    for num in tmp.translate({ord(i): None for i in ",[\']"}).split(): #create the term if the term is not in dictionary
                        self.invertDictionary[self.term].append(num)                    #,else put the posting list  in the exsit term
                        self.invertDictionaryCounter[self.term].append(num)
                else:
                    self.invertDictionary[self.term] = tmp.translate({ord(i): None for i in ",[\']"}).split()
                    self.invertDictionaryCounter[self.term] = tmp.translate({ord(i): None for i in ",[\']"}).split()

                self.lineCounting[index] = self.lineCounting[index] + 1
                if self.lineCounting[index] < self.stopARR[index]: # if the line in linecounting is smaller the lenght in block
                    line = linecache.getline(self.file[index], self.lineCounting[index]+1)
                    #print(line)
                    self.fullBufferReader[index] = line
            print(n_index)
            #fp = open("log"+str(block)+".txt", 'a')# for debug using
            #fp.write(str(self.fullBufferReader)+"\n")
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

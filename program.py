#https://stackoverflow.com/questions/10525867/extracting-tag-attributes-with-beautifulsoup
#https://github.com/igorbrigadir/stopwords/blob/master/en/nltk.txt
from bs4 import BeautifulSoup
from FileRetrival import FileRetrival
from Dictionary import Dictionary
from Merge import Merge


import math
import nltk
import string
import os

#k 1.5
#b 0.5

stopWordIn30 = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it',
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',' what']

stopWordIn150 = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "youre",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
    'his', 'himself', 'she', "shes", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they',
    'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "thatll",
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
    "dont", 'should', "shouldve", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "arent",
    'couldn', "couldnt", 'didn', "didnt", 'doesn', "doesnt", 'hadn', "hadnt", 'hasn', "hasnt", 'haven', "havent", 'isn',
    "isn't", 'ma', 'mightn', "mightnt", 'mustn', "mustnt", 'needn', "neednt", 'shan', "shant", 'shouldn', "shouldnt",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldnt"]

files = []
secondFile = []
dictPost = {}
fileLists = []
mg = Merge()
fr = FileRetrival()
dic = Dictionary()
stopArr = []
fr.retrivalSMGFile(files)

index = 0
max = 0
weight = 0
blockNumber = 0
articleCount = 0
dictionary = {}
tf_dictionary = {}
idf = {}
df = {}
N = 0
ld_dictionary = {}

documentLen = {}

df2 = {}
length_document = 0
average_length_document = 0
Bm25ScoreDictionary = {}

average_length_document2 = 0
length_document2 = 0
k1 = 0.5
b = 0.5
'''
#first loop to collect the df
for fileName in sorted(files):
    f = open("reuters21578/" + fileName, "r", encoding="ISO-8859-1")
    data = f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll("reuters")
    for content in contents:
        newid = (content['newid'])
        N += 1
        if str(content.body) != "None":
            temp = str((content.body.text).translate({ord(i): None for i in '\x7f'}))
            #tokens = nltk.word_tokenize((temp).lower().translate({ord(i): None for i in string.punctuation}))
            tokens = nltk.word_tokenize((temp).translate({ord(i): None for i in string.punctuation}))
            length_document = length_document + len(tokens)
            tokens = set(tokens)
            #collect the df in dictionary
            for token in tokens:
                if token in df:
                    df[token] = df[token] + 1
                else:
                    df[token] = 1
average_length_document = length_document / N
'''

#2nd loop
#tokenize and creat
for fileName in sorted(files):
    f = open("reuters21578/"+fileName, "r", encoding="ISO-8859-1")
    data = f.read()
    soup = BeautifulSoup(data)
    contents = soup.findAll("reuters")
    for content in contents:
        newid = (content['newid'])
        '''
        if str(content.title) != "None":
            temp = str((content.title.text).translate({ord(i): None for i in '\x7f'}))
            #tileTokens = nltk.word_tokenize((temp).lower().translate({ord(i): None for i in string.punctuation}))
            tileTokens = nltk.word_tokenize((temp).translate({ord(i): None for i in string.punctuation}))
            #tileTokens = set(tileTokens)-set(stopWordIn30)
            #tileTokens = set(tileTokens) - set(stopWordIn150)
            tileTokens = set(tileTokens)
            for tileToken in tileTokens:
                if not tileToken.isdigit():
                    if tileToken in dictionary:
                        dictionary[tileToken].append(newid)
                    else:
                        dictionary[tileToken] = [newid]
        '''
        if str(content.body) != "None":
            temp = str((content.body.text).translate({ord(i): None for i in '\x7f'}))
            #tokens = nltk.word_tokenize((temp).lower().translate({ord(i): None for i in string.punctuation}))
            tokens = nltk.word_tokenize((temp).translate({ord(i): None for i in string.punctuation}))
            #tokens = set(tokens) - set(stopWordIn30)

            ld = len(tokens)
            ld_dictionary[newid] = ld
            temptoken = tokens
            length_document2 = length_document2 + ld
            #tokens = set(tokens) - set(stopWordIn150)
            tokens = set(tokens)
            for token in tokens:
                tf = temptoken.count(token)
                if not token.isdigit():
                    #n is df
                    #n = df[token]
                    #print(token + str(n))
                    if newid in tf_dictionary:
                        if token in tf_dictionary[newid]:
                            tf_dictionary[newid][token] += tf
                        else:
                            tf_dictionary[newid][token] = tf
                    else:
                        tf_dictionary[newid] = {token: tf}
                    '''
                    # apply the formula by the book 11.32
                    weight = ((k1 + 1) * tf) / (tf + k1 * (((1 - b) + b * (ld / average_length_document))))
                    idf = math.log((N) / (n))
                    resultBM25 = (weight) * idf
                    if newid in Bm25ScoreDictionary:
                        Bm25ScoreDictionary[newid][token] = resultBM25
                    else:
                        Bm25ScoreDictionary[newid] = {token: resultBM25}
                        '''
                    if token in dictionary:

                        #if newid not in dictionary[token]:
                        dictionary[token].append(newid)
                        #dictionary[token].append(newid+":"+str(tf))
                    else:
                        #dictionary[token] = [newid+":"+str(tf)]
                        dictionary[token] = [newid]

        articleCount += 1
        if articleCount % 499 == 0:
            if not os.path.exists("./disk"):
                os.makedirs("./disk")
            dictionary.pop('\u0003', None)
            fileNameCreate = "./disk/block" + str(blockNumber) + ".txt"
            fileLists.append(fileNameCreate)
            fp = open(fileNameCreate, 'a')
            keyArr = sorted(dictionary)
            for key in keyArr:
                fp.write(str(key)+":::"+str(dictionary[key])+"\n")
            fp.write("zzzzzzzzzzzzzz----:::[]")
            print(fileNameCreate)
            dictionary = {}
            blockNumber += 1

# check the last reminding
if(dictionary):
    dictionary.pop('\u0003', None)
    fileNameCreate = "./disk/block"+ str(blockNumber) +".txt"
    fileLists.append(fileNameCreate)
    with open(fileNameCreate, 'a') as fp:
        keyArr = sorted(dictionary)
        for key in keyArr:
            fp.write(str(key) + ":::" + str(dictionary[key])+"\n")
# put "zzzzzzzzzzzzzz----:::[]" in the bottom of the block
        fp.write("zzzzzzzzzzzzzz----:::[]")
    dictionary = {}
    print(fileNameCreate)

average_length_document2 = length_document2 / articleCount

documentLen["N"] = articleCount
documentLen["average_length"] = average_length_document2


for file in fileLists:
    index = 0
    with open(file) as fin:
        for line in fin:
            index += 1
    if max < index:
        max = index
        maxFile = file
    stopArr.append(index)
print(maxFile)
print(max)
print(stopArr)

with open("DocTemp.txt", 'a') as fpp:
    for key in documentLen:
        fpp.write(str(key) + "<:::>" + str(documentLen[key]) + "\n")
'''
with open("BM25Score.txt", 'a') as fpp:
    for key in Bm25ScoreDictionary:
        fpp.write(str(key) + "<:::>" + str(Bm25ScoreDictionary[key]) + "\n")
'''
with open("tf.txt", 'a') as fpp:
    for key in tf_dictionary:
        fpp.write(str(key) + "<:::>" + str(tf_dictionary[key]) + "\n")

with open("ld.txt", 'a') as fpp:
    for key in tf_dictionary:
        fpp.write(str(key) + "<:::>" + str(ld_dictionary[key]) + "\n")
#merge
mg.mergeInit(fileLists, stopArr, max)
mg.run()

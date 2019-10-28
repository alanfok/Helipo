#https://stackoverflow.com/questions/10525867/extracting-tag-attributes-with-beautifulsoup
#https://github.com/igorbrigadir/stopwords/blob/master/en/nltk.txt
from bs4 import BeautifulSoup
from FileRetrival import FileRetrival
from Dictionary import Dictionary
from Merge import Merge



import nltk
import string
import os

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
max =0
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

        if str(content.body) != "None":
            temp = str((content.body.text).translate({ord(i): None for i in '\x7f'}))
            #tokens = nltk.word_tokenize((temp).lower().translate({ord(i): None for i in string.punctuation}))
            tokens = nltk.word_tokenize((temp).translate({ord(i): None for i in string.punctuation}))
            #tokens = set(tokens) - set(stopWordIn30)
            #tokens = set(tokens) - set(stopWordIn150)
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
#merge
mg.mergeInit(fileLists, stopArr, max)
mg.run()

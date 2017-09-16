import nltk
from nltk.corpus import stopwords
p = open("Pos.txt","r")
postext = p.readlines()
n = open("Neg.txt","r")
negtext = n.readlines()
x = ["POSITIVE"] *len(postext)
y = ['NEGATIVE'] *len(negtext)
taggedtweets = zip( postext,x) + zip(negtext,y)
#print taggedtweets
tweetsW = []
for (line,senti) in taggedtweets:
    words = [i.upper() for i in line.split()]
    tweetsW.append((words,senti))
#print tweetsW
def getwordfreq(xyz):
    x=[]
    for (words,senti) in xyz:
        x.extend(words)
    wordFreq = nltk.FreqDist(x)
    #print wordFreq.keys()
    #print wordFreq.values()   
    return wordFreq.keys()
words = getwordfreq(tweetsW)
#print "\n---------\n"
#print (words)
customStopwords = ['HE','SHE','ABSOLUTELY','COMPLETELY','YOU','FEEL','LEAD', 'MAKE','THEY','SEE','MUCH','PRESIDENT','THISYOU','TO','ALBUM','NEW','MAKES', 'THAN','SINGER','GO', 'THE', 'THINK','SHOULD', 'SO','MY', 'EARS','FOR', 'WHAT','BAND','WAS','IS','I','ME','MYSELF','KOREA','NORTH','SOUTH','ARE','THEM','THEIR','THIS','THAT','BEING','PLAY','IN','IS']
allWords = [i for i in words if not i in customStopwords and i not in stopwords.words('english')]
#print '\n---------\n'
#print allWords
def featureExtractor(document):
    document = set(document)
    features = {}
    for i in allWords:
        features['contains(%s)' %i] = (i in document)
    return features
#print "\n--------\n"
trainingSet = nltk.classify.apply_features(featureExtractor,tweetsW)
#print trainingSet
classifier = nltk.NaiveBayesClassifier.train(trainingSet)
print "----------------------------------------------------------------------------------------------------------"
a = raw_input( 'Enter a sentence for Sentiment analysis : ')
a = a.upper()
#print "--------"
sentence = list()
sentence = a.split()
word = [i for i in sentence if not i in allWords and not i in stopwords.words('english')and not i in customStopwords]
#print word
flag = 0
for z in range(0,len(word)):
    if word not in allWords:
        #print "--------"
        print word
        print 'This word is not in our directory.\n'
        ans = raw_input('If it is POSITIVE, press P.\nIf it is NEGATIVE, press N.\nIf it is NOT a SENTIMENTAL word, press G.\n')
        if ans.upper() == 'N':
            r = open('neg.txt','a')
            r.write("\n")
            r.write(a)
            r.close()
            flag = 1
            break
        elif ans.upper() == 'P':
            r = open('pos.txt','a')
            r.write("\n")
            r.write(a)
            r.close()
            flag = 1
            break
        else:
            break

if flag ==1 :
    print "----------------------------------------------------------------------------------------------------------"
else:
    print "----------------------------------------------------------------------------------------------------------"
    print 'The entered sentence is : '
    print classifier.classify(featureExtractor(a.strip().split()))
    print "----------------------------------------------------------------------------------------------------------"
p.close()
n.close()

import cPickle as pickle
LetterDict = {}

y=0
for x in range(ord('a'),ord('z')):
    l=[0]*100
    l[y] = 1
    LetterDict[chr(x)] = l
    y+=1

print LetterDict

pickle.dump( LetterDict, open("letterdict.p", "wb"))

import random, pickle

txt_f='game/words.txt'
pickle_f='game/words.dat'

#production.py에서 실행할 때 새로운 단어 추가할려고 쓰는 함수
def inputWords():
    f1=open(txt_f, 'rt')
    words = f1.readlines()
    for i in range(len(words)):
        words[i] = words[i].replace('\n', '')
    f1.close()
    f2=open(pickle_f, 'wb')
    pickle.dump(words, f2)
    f2.close()

def makeWord():
    f=open(pickle_f, 'rb')
    word_dic= pickle.load(f)
    word = random.choice(word_dic)
    f.close()
    return word

def makeSet(X, Y):

    if random.randint(0,1): #위 또는 아래에서 나올때
        x= random.choice((0, X))    #모서리 중 하나
        y= random.randint(0, Y)
    else:
        x= random.randint(0, X)
        y= random.choice((0, Y))

    return (x, y)

if __name__ == '__main__':
    inputWords()
    f = open(pickle_f, 'rb')
    worddb=[]
    worddb = pickle.load(f)
    maxV=len(worddb[0])
    for w in worddb:
        if maxV<len(w):
            maxV=len(w)
    print(maxV)

    f.close()


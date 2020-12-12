from unittest import TestCase
import pickle, random

txt_f = 'data/words.txt'
pickle_f = 'data/words.dat'

class Test(TestCase):

    def test_inputWords(self):
        f1 = open(txt_f, 'rt')
        words = f1.readlines()
        for i in range(len(words)):
            words[i] = words[i].replace('\n', '')
            self.assertIn(words[i], words)
        f1.close()

    def test_makeWord(self):
        try:
            f = open(pickle_f, 'rb')
            word_dic = pickle.load(f)
            word = random.choice(word_dic)
            f.close()
        except FileNotFoundError as e:
            word = "FileNotFoundError"
        self.assertIsNotNone(word)

    def test_makeSet(self):
        try:
            f = open(pickle_f, 'rb')
            word_dic = pickle.load(f)
            word = random.choice(word_dic)
            f.close()
        except FileNotFoundError as e:
            word = "FileNotFoundError"

        w=15*len(word) # 단어박스의 가로길이 - 개선필요

        X = 1280 - w
        Y=930

        # 난수 나오는 범위 조정
        if random.randint(0, 1):  # 위 또는 아래에서 나올때
            x = random.choice((0, 1280))  # 모서리 중 하나
            y = random.randrange(0, 930, 5)
        else:
            x = random.randrange(0, 1280, 5)
            y = random.choice((0, 930))

        if x==X:
            self.assertTrue(0 <= y <= Y)
        elif y==Y:
            self.assertTrue(0<=x<=X)

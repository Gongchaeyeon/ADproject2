import pygame, math
from game import production
display_size=(1280,960)
X=display_size[0]
Y=display_size[1]
class wordBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.word = production.makeWord()
        self.w=15*len(self.word)
        self.h=30
        self.set = production.makeSet(X - self.w, Y - self.h) # set or list
        self.rect = pygame.Rect(self.set[0], self.set[1], self.w, self.h) #변수, 문자열 길이에 따른 ,20 #상수
        self.word_font = pygame.font.Font(None, 30)
        self.surface = self.word_font.render(self.word, True, (0, 0, 0))
        print(self.word, self.set)


        # 박스 생성되는 delay랑, 게임진행(움직임) delay를 다르게 해야겠네 ->if문을 사용할까? 창연공에서 했던 것 처럼
        #0. 랜덤한 단어
        #1. 랜덤한 위치에서 생성

    def move(self, speed):
        xS = X/2 - (self.set[0]+self.w/2)
        yS = Y/2 - (self.set[1]+self.h/2)
        k = speed / (math.sqrt(xS * xS + yS * yS))
        self.speed = (k * xS, k * yS)  # 식 세워가지고 speed 정해줘야함
        # speed는 속력, self.speed는 속도
        self.rect = self.rect.move(self.speed)

if __name__ == "__main__":
    pygame.font.init()
    w=wordBox()

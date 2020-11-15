import pygame, math
from game import production
display_size=(1280,960)
X=display_size[0]
Y=display_size[1]

class wordBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.word = production.makeWord()
        self.w=15*len(self.word) # 단어박스의 가로길이 - 개선필요
        self.h=30
        self.set = production.makeSet(X - self.w, Y - self.h) # 생성 좌표 설정
        self.rect = pygame.Rect(self.set[0], self.set[1], self.w, self.h) #변수, 문자열 길이에 따른 ,20 #상수
        self.word_font = pygame.font.Font(None, 30)
        self.surface = self.word_font.render(self.word, True, (0, 0, 0))
        self.scalar_speed = 0
        print(self.word, self.set)

    def move(self):
        xS = X/2 - (self.set[0]+self.w/2)
        yS = Y/2 - (self.set[1]+self.h/2)
        k = self.scalar_speed / (math.sqrt(xS * xS + yS * yS))
        self.speed = (k * xS, k * yS)  # 벡터 식
        # scalar_speed는 속력, self.speed는 속도
        self.rect = self.rect.move(self.speed)

    def set_speed(self, level, t):
        #임시로 level*(시간에 대한 무리함수 꼴)
        self.scalar_speed = level*math.sqrt(t)

if __name__ == "__main__":
    pygame.font.init()
    w=wordBox()

import pygame, math
import production
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
        self.surface = self.word_font.render(self.word, True, (255, 255, 255), None)
        self.scalar_speed = 0
        self.set_float = []
        self.set_float.append(self.set[0])
        self.set_float.append(self.set[1])
        xS = X/2 - (self.set[0]+self.w/2)
        yS = Y/2 - (self.set[1]+self.h/2)
        k = 1/ (math.sqrt(xS * xS + yS * yS))   

        print(self.word, xS,yS, (k*xS, k*yS), end= '     ')

    def move(self):
        #xS = X / 2 - (self.set[0] + self.w / 2)
        #yS = Y / 2 - (self.set[1] + self.h / 2)
        xS = X/2 - round(self.set_float[0], 2)
        yS = Y/2 - round(self.set_float[1], 2)
        k = self.scalar_speed / (math.sqrt(xS * xS + yS * yS))
        self.speed = (k * xS, k * yS)  # 벡터 식
        #frame이 integer 단위이기에 move를 override하는건 불가능
        #but, set의 float형을 갖는 list를 두어서,
        # xS, yS를 더 정확한 값에(정보손실이 덜하는)두어 이동 문제를 어느정도 해결
        self.set_float[0] += self.speed[0]
        self.set_float[1] += self.speed[1]
        # scalar_speed는 속력, self.speed는 속도
        self.rect = self.rect.move(round(self.speed[0]), round(self.speed[1]))

    def set_speed(self, level, t):
        #임시로 level*(producedT에 대한 무리함수꼴)
        #self.scalar_speed = level*(-1/(t+0.9)+5/level)
        self.scalar_speed = 5 - level
        #속력은 2*10^0.4 -> 약 5를 마지노선으로 잡고 가자
        print(self.scalar_speed, end = '     ')
if __name__ == "__main__":
    pygame.font.init()
    w=wordBox()

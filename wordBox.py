import pygame, math
import production
display_size=(1280,960)
X=display_size[0]
Y=display_size[1]

class wordBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.word = production.makeWord()
        self.w=15*len(self.word) # 단어박스의 가로길이 -
        self.h=30

        self.set = production.makeSet(X - self.w, Y - self.h) # 생성 좌표 설정
        self.rect = pygame.Rect(self.set[0], self.set[1], self.w, self.h) #변수, 문자열 길이에 따른 ,20 #상수
        self.word_font = pygame.font.Font(None, 30)
        self.surface = self.word_font.render(self.word, True, (255, 255, 255), None)

    def move(self, target_center, center):

        distance = math.sqrt((target_center[0] - center[0])**2+(target_center[1] - center[1])**2)
        #중력 효과를 넣기 위해 속도에 배수를 해주는 변수
        g=2
        if distance>300:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((g*self.speed[0], g*self.speed[1]))

    def set_speed(self, level, t):
        #level*(producedT에 대한 무리함수꼴)
        tmp=level*(t+0.9)**0.1
        self.scalar_speed = tmp if tmp<4 else 4
        self.set_float = [self.set[0] + self.w / 2, self.set[1] + self.h / 2]
        self.initial_xS = X / 2 - self.set_float[0]
        self.initial_yS = Y / 2 - self.set_float[1]
        self.initial_k = 1 / (math.sqrt(self.initial_xS * self.initial_xS + self.initial_yS * self.initial_yS))
        self.unit_speed = (self.initial_k * self.initial_xS, self.initial_k * self.initial_yS)  # cos, sin
        self.speed = (round(self.scalar_speed * self.unit_speed[0]),round(self.scalar_speed * self.unit_speed[1]))  # 벡터 식

        #속력은 2*10^0.4 -> 5를 최대속도로 하여 단어가 안보이는 현상 막음

if __name__ == "__main__":
    pygame.font.init()
    w=wordBox()

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

    def move(self, target_center, center):

        #frame이 integer 단위이기에 move를 override하는건 불가능
        #but, set의 float형을 갖는 list를 두어서,
        # xS, yS를 더 정확한 값에(정보손실이 덜하는)두어 이동 문제를 어느정도 해결
        #--> 하려 했으나 이렇게 하면 운석이 끼는 현상 발생 -> move함수 대신 지구의 크기를 바꿔서 운석이 지구에 빗나가지 않게 함
        # --> 최소 스피드 2는 해야 빗나가지 않음 어쩔 수 없는 pygame 모듈의 문제이기에 (좌표값이 정수임) 이게 최선.

        # scalar_speed는 속력, self.unit_speed는 방향, self.speed는 속도

        distance = math.sqrt((target_center[0] - center[0])**2+(target_center[1] - center[1])**2)
        #중력 효과를 넣기 위해 속도에 배수를 해주는 변수
        g=2
        if distance>300:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((g*self.speed[0], g*self.speed[1]))

    def set_speed(self, level, t):
        #임시로 level*(producedT에 대한 무리함수꼴)
        #
        tmp=level*(t+0.9)**0.1
        print("levlel {}".format(level))
        self.scalar_speed = tmp if tmp<4 else 4
        self.set_float = [self.set[0] + self.w / 2, self.set[1] + self.h / 2]
        self.initial_xS = X / 2 - self.set_float[0]
        self.initial_yS = Y / 2 - self.set_float[1]
        self.initial_k = 1 / (math.sqrt(self.initial_xS * self.initial_xS + self.initial_yS * self.initial_yS))
        self.unit_speed = (self.initial_k * self.initial_xS, self.initial_k * self.initial_yS)  # cos, sin
        self.speed = (round(self.scalar_speed * self.unit_speed[0]),round(self.scalar_speed * self.unit_speed[1]))  # 벡터 식

        #self.scalar_speed = 5 - level
        #속력은 2*10^0.4 -> 약 5를 마지노선으로 잡고 가자
        #확인용 코드
        print(self.word, self.initial_xS, self.initial_yS, (self.initial_k * self.initial_xS, self.initial_k * self.initial_yS), end='     ')
        print(self.scalar_speed, self.speed, end = '     ')
if __name__ == "__main__":
    pygame.font.init()
    w=wordBox()

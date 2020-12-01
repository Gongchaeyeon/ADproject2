import wordBox as WB
import inputBox as IB
from Images import *    #Background, Earth, Meteor class
import pygame, math, sys

import pickle
import tkinter as tk
from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw()

#Sprite Group, enemy를 move 시키기 위해서 필요
group = pygame.sprite.Group()

#size of window
display_size = (1280, 960)
size=display_size

#bakcground
background = Background("data/image/space.png")

#Earth
earth = Earth("data/image/earth.png", 250)
#Meteor
meteor = Meteor("data/image/meteor.png", 50)

#화면, 입력박스, 단어박스들, 라이프, 점수등 초기화
def initialize():
    global screen, textinput, time_term, clock, last_time, enemy, lives, score, producedT, enemy_death, maxScore
    maxScore =0

    screen = pygame.display.set_mode(size)

    # Create TextInput-object
    textinput = IB.TextInput()

    #to set each enemy's speed
    producedT=0+0.1

    #단어 생성 시간 간격 ms
    #1500<time_term<=3000
    time_term = 1500 * (1 / (1 * producedT + 0.9)) + 1500

    #pygame의 clock 객체, 프레임 조정을 담당함
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()

    #단어박스(enemy)를 Sprite의 Group에서 다 없애고, 초기화 시킴
    for w in group:
        group.remove(w)

    #livses and score
    lives = 20
    score=0

    enemy_death = 0 #move함수 실험용 변수: 충돌한 행성 갯수

def set_initial_speed():
    fh = open('data/difficulty.dat', 'rb')
    level = pickle.load(fh)
    fh.close()

    if level == "하":
        return 2
    elif level == "중":
        return 3
    else:#상
        return 4

#게임 오버 후 화면에 글자 숫자 띄워줌
def replay(time,maxScore):

    screen.fill((255, 255, 255))
    replay_font = pygame.font.Font(None, 50)
    replay_string1 = "Game Over!"
    replay_score = "score: " + str(maxScore)
    replay_string2 = "press key R to replay"
    replay_string3 = "{}".format(time)
    replay_surface1 = replay_font.render(replay_string1, 1, (0, 0, 0))
    replay_surface2 = replay_font.render(replay_score, 1, (0, 0, 0))
    replay_surface3 = replay_font.render(replay_string2, 1, (0, 0, 0))
    replay_surface4 = replay_font.render(replay_string3, 1, (0, 0, 0))

    screen.blit(replay_surface1, (550, 300))
    screen.blit(replay_surface2, (563-(((len(replay_score)-7)/10)*2), 360))
    screen.blit(replay_surface3, (470, 420))
    screen.blit(replay_surface4, (630, 480))

    pygame.display.update()

#게임 오버 후 replay 할 것인지, 끝낼 것인지 결정
def isgameover(lives, score, MaxScore):
    if not lives:
        # 가장 큰 점수를 저장함
        maxScore= score if MaxScore<score else MaxScore
        fh= open('data/maxScore.dat', 'wb')
        pickle.dump(maxScore, fh)
        fh.close()
        #showing = 현재시간, waiting = 현재시간 +10초
        waiting = pygame.time.get_ticks() + 10000
        showing = pygame.time.get_ticks()
        t = 10
        R_pressed = False
        #10초안에 R키 누를 시 재시작, 그렇지 않으면 게임 종료
        while (waiting > pygame.time.get_ticks() and not (R_pressed)):
            #1초가 경과할때마다 t가 1씩 줄어들어서 10-9-8...1-0 의 식으로 초를 보여줌
            if showing + 1000 < pygame.time.get_ticks():
                showing += 1000
                t -= 1
            replay(t,maxScore)
            events = pygame.event.get()
            for event in events:
                #종료버튼을 누르면
                if event.type == pygame.QUIT:
                    exit()
                #R key가 눌리면
                elif event.type == pygame.KEYDOWN and event.key == pygame.locals.K_r:
                    initialize()
                    R_pressed = True
                    break
        else:
            #10초동안 가만히 있을시 게임 자동으로 종료
            if not R_pressed: exit()

#최종 점수를 저장하기 위한 변수
MaxScore=0

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    # 배경음악 재생
    backgroundSound = pygame.mixer.Sound('data/sounds/background.wav')
    backgroundSound.set_volume(0.1)
    backgroundSound.play(-1)

    initialize()
    level = set_initial_speed()

    while True:
        # game over
        isgameover(lives, score, MaxScore)

        #배경 이미지 (우주) screen에 붙여넣기
        screen.blit(background.image, background.location)
        #라이프, 점수 표시 draw lives and score
        for i in range(lives):
            pygame.draw.circle(screen, (200, 0, 130), (30+30*i, 900), 10)
        score_font=pygame.font.Font(None, 30)
        score_surface=score_font.render("score: {}".format(score), 1, (255, 255, 255))
        screen.blit(score_surface, (30, 930))

        #지구 screen에 붙이기
        screen.blit(earth.image, (size[0]/2-earth.r, size[1]/2-earth.r))
        # 확인 코드 : 지구 주변에 중력효과가 작용되는 원 그리기
        pygame.draw.circle(screen, (255, 255 , 255), (size[0]/2, size[1]/2), 300, 5)

        #단어박스 생성, produce enemy( = wordBox )
        if pygame.time.get_ticks() > last_time+time_term:

            enemy = WB.wordBox()
            enemy.set_speed(level, producedT)
            group.add(enemy)

            producedT+=0.1
            print(time_term)    #시간 간격 확인용 출력문

            time_term = 1500 * (1 / (1* producedT + 0.9)) + 1500
            last_time+=time_term

            print("생성된 애들: {}".format(int(producedT * 10))) #확인용 코드

        for enemy in group:
            #운석 이미지 생성위치 -> 뺄 숫자 바꿔주면서 글자랑 위치 조정했음
            meteor_location=[enemy.rect.x-15, enemy.rect.y-30]
            # 단어박스 움직임
            enemy.move((size[0]/2-30, size[1]/2), (meteor_location[0]+meteor.r, meteor_location[1]+meteor.r))
            #운석, 단어 screen에 붙여넣기
            screen.blit(meteor.image, meteor_location)
            screen.blit(enemy.surface, (enemy.rect.x+5, enemy.rect.y+5))


            #확인 코드 : 운석 주변 원 표시 -> 중력 효과 적용 보기 위해서
            pygame.draw.circle(screen, (255, 255, 0), (meteor_location[0]+50, meteor_location[1]+50), meteor.r, 2)

            meteor_location[0]+=enemy.speed[0]
            meteor_location[1]+=enemy.speed[1]
            #운석이 지구와 부딪히면
            if meteor.collision((size[0]/2-30, size[1]/2), earth.r - 70, (meteor_location[0]-30, meteor_location[1])):
                #group에서 enemy(단어) 제거 -> 화면에서 사라지는 효과
                group.remove(enemy)
                
                # 부딪히는 효과음
                hit = pygame.mixer.Sound('data/sounds/쿠르를.wav')
                hit.set_volume(1)
                hit.play()
                lives-=1
                
                enemy_death+=1
                print("죽은 애들: {}".format(enemy_death))  #move함수 확인용 코드 -> 360개중 360개 정확히 충돌함

        events = pygame.event.get() #사용자로부터 이벤트 받음
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if (tk.messagebox.askyesno('경고!', '게임을 중단하면 결과가 저장되지 않습니다. \n게임을 종료하시겠습니까?', icon='error') == True):
                    exit()
                else:
                    last_time=pygame.time.get_ticks()

        textinput.update(events)
        # 매 프레임마다 이벤트를 준다,Feed it with events every frame -> 입력 박스에 글자가 써지고 지워지는 것, 엔터누르면 입력되는 것..

        #단어 입력시(엔터) group내에 같은 글자를 가진게 있으면, 해당 단어박스 없앰. kill enemy by entering correspending word
        if textinput.get_search():
            for w in group:
                if textinput.get_text() == w.word:
                    group.remove(w)

                    # 단어 맞췄을 때 효과음
                    s_sound= pygame.mixer.Sound('data/sounds/마리오.wav')
                    s_sound.set_volume(0.3)
                    s_sound.play()

                    score+=100
                    enemy_death += 1
                    
            textinput.search=False

        #텍스트박스 screen에 붙여기 Blit its surface onto the screen
        textinput.draw(screen)

        #screen을 업데이트 시켜서 화면에 보이도록 함
        pygame.display.update()
        clock.tick(30)

#개선해야 할점
# 3. 가운데 정렬
# 5. enemy(wordBox's instance) width 크기 조정

#해결

# 2. collision 처리  Game.py line 11
# 6. 단어 move 의 rect.move 오버라이드 해서 실수형 가능하게 하기 .
# -> 실수로 좌표를 주면 운석이 끼게됨, move함수는 그대로하고 지구 크기를 늘려서 간접적으로 해결함

# 1. enemy(wordBox's instance) remove 하는 방법  Game.py line 87, inputBox.py line 115
# 4. 엔터하면 단어 사라지게 만들기
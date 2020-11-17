import wordBox as WB
import inputBox as IB
import pygame, math, sys
from PyQt5 import QtWidgets as Qt
import pickle

#Sprite Group, enemy를 move 시키기 위해서 필요
group = pygame.sprite.Group()

#https://stackoverflow.com/questions/24727773/detecting-rectangle-collision-with-a-circle
def collision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width/2, rtop + height/2

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected

#size of window
display_size = (1280, 960)
size=display_size

#화면, 입력박스, 단어박스들, 라이프, 점수등 초기화
def initialize():
    global screen, textinput, time_term, clock, last_time, enemy, lives, score, producedT

    screen = pygame.display.set_mode(size)

    # Create TextInput-object
    textinput = IB.TextInput()

    #단어 생성 시간 간격 ms
    time_term = 3000
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()

    for w in group:
        group.remove(w)

    #livses and score
    lives = 5
    score=0

    #to set each enemy's speed
    producedT=0+1

def set_initial_speed(level = "중"):
    fh = open('data/difficulty.dat', 'rb')
    level = pickle.load(fh)
    fh.close()
    print(level)

    if level == "하":
        return 1.2
    elif level == "중":
        return 2
    else:#상
        return 3
#게임 오버 후 화면에 글자 숫자 띄워줌
def replay(time):
    screen.fill((255, 255, 255))
    replay_font = pygame.font.Font(None, 50)
    replay_string1 = "Game Over!"
    replay_string2 = "press key R to replay"
    replay_string3 = "{}".format(time)
    replay_surface1 = replay_font.render(replay_string1, 1, (0, 0, 0))
    replay_surface2 = replay_font.render(replay_string2, 1, (0, 0, 0))
    replay_surface3 = replay_font.render(replay_string3, 1, (0, 0, 0))

    screen.blit(replay_surface1, (400, 300))
    screen.blit(replay_surface2, (400, 400))
    screen.blit(replay_surface3, (400, 500))


    pygame.display.update()

#게임 오버 후 replay 할 것인지, 끝낼 것인지 결정
def isgameover(lives, score, MaxScore):
    if not lives:
        # 가장 큰 점수를 저장함
        maxScore= score if MaxScore<score else MaxScore
        fh= open('data/maxScore.dat', 'wb')
        pickle.dump(maxScore, fh)
        fh.close()

        waiting = pygame.time.get_ticks() + 10000
        showing = pygame.time.get_ticks()
        t = 10
        R_pressed = False
        #10초안에 R키 누를 시 재시작, 그렇지 않으면 게임 종료
        while (waiting > pygame.time.get_ticks() and not (R_pressed)):
            if showing + 1000 < pygame.time.get_ticks():
                showing += 1000
                t -= 1
            replay(t)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                #R key가 눌리면
                elif event.type == pygame.KEYDOWN and event.key == pygame.locals.K_r:
                    initialize()
                    R_pressed = True
                    break
        else:
            if not R_pressed: exit()

#최종 점수를 저장하기 위한 변수
MaxScore=0

if __name__ == "__main__":
    pygame.init()
    initialize()
    level = set_initial_speed()
    while True:
        # game over
        isgameover(lives, score, MaxScore)
        screen.fill((255, 255, 255))  # 뒷 배경색을 하얀색으로 채움

        #라이프, 점수 표시 draw lives and score
        for i in range(lives):
            pygame.draw.circle(screen, (200, 0, 130), (30+30*i, 900), 10)

        score_font=pygame.font.Font(None, 30)
        score_surface=score_font.render("score: {}".format(score), 1, (0, 0, 0))
        screen.blit(score_surface, (30, 930))

        #핵 그리기 draw circle
        pygame.draw.circle(screen, (10, 25, 124),(size[0]/2, size[1]/2) ,170, 5)

        #단어박스 생성, produce enemy( = wordBox )
        if pygame.time.get_ticks() > last_time+time_term:
            enemy = WB.wordBox()
            enemy.set_speed(level, producedT)
            producedT+=1
            group.add(enemy)
            last_time+=time_term

        for enemy in group:
            #단어박스 움직임
            enemy.move()
            enemy.surface = enemy.word_font.render(enemy.word, True, (0, 0, 0))
            screen.blit(enemy.surface, (enemy.rect.x+5, enemy.rect.y+5))
            pygame.draw.rect(screen, [0,0,0], enemy.rect, 1)

            #collision(충돌)시 단어(enemy) 제거 , 라이프 깎임
            if collision(enemy.rect.x, enemy.rect.y, enemy.rect.w, enemy.rect.h,
                         size[0]/2, size[1]/2, 170):
                group.remove(enemy)
                lives-=1

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Feed it with events every frame
        textinput.update(events)

        #단어 입력시, 해당 단어박스 없앰 kill enemy by entering correspending word
        if textinput.get_search():
            for w in group:
                if textinput.get_text() == w.word:
                    group.remove(w)
                    score+=100
            textinput.search=False

        # Blit its surface onto the screen
        textinput.draw(screen)
        pygame.display.update()
        clock.tick(30)


#개선해야 할점
# 1. enemy(wordBox's instance) remove 하는 방법  Game.py line 87, inputBox.py line 115
# 2. collision 처리  Game.py line 11
# 3. 가운데 정렬
# 4. 엔터하면 단어 사라지게 만들기
# 5. enemy(wordBox's instance) width 크기 조정
# 6. 단어 move 의 rect.move 오버라이드 해서 실수형 가능하게 하기 .

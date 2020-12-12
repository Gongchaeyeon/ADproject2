from unittest import TestCase
import random
import math, pygame
from wordBox import wordBox


class TestwordBox(TestCase):

    def setUp(self):
        pygame.font.init()
        self.w = wordBox()
        self.w.set_speed(2, 0.1)

    #word의 move 함수가 중력구현 부분을 잘 했는지 테스트
    def test_move(self):
        #display_size = (1280, 960)
        target_center =  (1280/2-30, 960/2)
        case = int(input("test 시행 횟수 입력 : "))
        print()
        for i in range(case):
            print("test %d" %(i+1))
            # 1. 직접 입력 해서 테스트 할 때
            x, y= map(int, input().strip().split())
            center = (x, y)
            #2. random한 값으로 테스트 할 때
            #center = (random.randint(0, 1280), random.randint(0, 960))
            #좌표평면에서의 점과 점사이의 거리 공식
            distance = math.sqrt((target_center[0] - center[0]) ** 2 + (target_center[1] - center[1]) ** 2)
            rst = 0 if distance>300 else 1
            self.assertEqual(self.w.move(target_center,center), rst)

    def test_set_speed(self):
        pass

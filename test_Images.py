from unittest import TestCase
from Images import Meteor
import random, math, pygame
class TestMeteor(TestCase):

    def setUp(self):
        pygame.init()
        self.meteor =Meteor("data/image/meteor.png", 50)

    #meteor의 collision이 True, False를 잘 반환 하는지 테스트
    def test_collision(self):
        #display_size = (1280, 960)
        #constant
        earth_center = (1280 / 2 - 30, 960 / 2)
        meteor_r = 50
        earth_r = 200
        case = int(input("test 시행 횟수 입력 : "))
        print()
        for i in range(case):
            print("test %d" % (i + 1))
            # 1. 직접 입력 해서 테스트 할 때
            x, y = map(int, input().strip().split())
            location = (x-30, y)
            # 2. random한 값으로 테스트 할 때
            #location = (random.randint(0, 1280)-30, random.randint(0, 960))
            center = (location[0]+meteor_r, location[1]+meteor_r)
            #좌표평면에서의 점과 점사이의 거리 공식
            distance = math.sqrt((earth_center[0] - center[0]) ** 2 + (earth_center[1] - center[1]) ** 2)

            ans = False if distance>earth_r+meteor_r else True

            rst =self.meteor.collision(earth_center, earth_r, location)
            self.assertEqual(rst, ans)
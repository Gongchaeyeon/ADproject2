import pygame
import math

#이미지 클래스
class Image(pygame.sprite.Sprite):
    def __init__(self, image_file, location=(0,0), size=(1280,960)):
        super().__init__() #call Sprite initializer
        #이미지 파일 로드함
        self.image_file = pygame.image.load(image_file)
        self.size=size
        self.location=location
        #이미지의 크기를 원하는 size에 맞게 조정함
        self.image = pygame.transform.scale(self.image_file, self.size)


class Background(Image):
    def __init__(self, image_file):
        super().__init__(image_file)

class Earth(Image):
    def __init__(self, image_file, r):
        #지구의 반지름
        self.r=r
        size=(2*self.r, 2*self.r)
        location = (640 - self.r, 480 - self.r)
        super().__init__(image_file, location, size)

class Meteor(Image):
    def __init__(self, image_file, r):
        #운석의 반지름
        self.r=r
        size=(2*self.r, 2*self.r)
        super().__init__(image_file,(0,0) , size)

    #원(지구)와 원(운석)이 충돌하는 것으로 판단
    def collision(self, target_center, target_r, location):
        self.center = (location[0]+self.r, location[1]+self.r)
        #지구 중심과 운석 중심 사이의 거리
        distance = math.sqrt((target_center[0] - self.center[0])**2+(target_center[1] - self.center[1])**2)
        #거리와 반지름의 합 비교
        if distance>(target_r+self.r):
            return False
        else:
            return True

import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location=(0,0)):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(image, (1280, 960))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        print(self.rect)

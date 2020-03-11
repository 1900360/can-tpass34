import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings
        
        #加载alien图像
        self.image=pygame.image.load('image/alien.bmp')
        self.rect=self.image.get_rect()
        #初始位置在左上角
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #存储alien的准确位置
        self.x=float(self.rect.x)
    def blitme(self):
        """绘制alien"""
        self.screen.blit(self.image,self.rect)
    def check_edgs(self):
        """若alien位于屏幕边缘，就返回ture"""
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True
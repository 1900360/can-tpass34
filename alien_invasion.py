import pygame
import game_fuctions as gf
from settings import Settings
from game_stats import GameStats
from ship import Ship
from button import Button
from scoreboard import Scoreboard
from bullet import Bullet
from pygame.sprite import Group
def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("CXK VS Ball")
    #创建飞船
    ship=Ship(ai_settings,screen)
    #创建存储子弹的群
    bullet_always=Bullet(ai_settings,screen,ship)
    bullets=Group()
    #创建alien群
    aliens=Group()
    gf.create_aliens(ai_settings,screen,ship,aliens)
    #创建存储游戏统计信息的实例,并创建记分牌
    stats=GameStats(ai_settings)
    sb=Scoreboard(ai_settings,screen,stats)
    #创建Play按钮
    play_button=Button(ai_settings,screen,"Fighting")
    
    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullet_always)
        if stats.game_active:     
            Ship.update(ship)
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bullet_always)
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
run_game()
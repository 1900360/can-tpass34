import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullet_always):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        #在玩家单击play时开始新游戏
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
                check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                #向右移动飞船
                ship.moving_right=True
            elif event.key==pygame.K_LEFT:
                #向左移动飞船
                ship.moving_left=True
            elif event.key==pygame.K_UP:
                #向上移动飞船
                ship.moving_up=True
            elif event.key==pygame.K_DOWN:
                #向下移动飞船
                ship.moving_down=True
            elif event.key==pygame.K_SPACE:
                #发射子弹
                bullet_always.fire=True
            elif event.key==pygame.K_r:
                #重启游戏
                stats.game_active=False
                pygame.mouse.set_visible(True)
            elif event.key==pygame.K_s:
                #暂停10S
                sleep(10)
            elif event.key==pygame.K_p:
                #使用p开始游戏
                check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        elif event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT:
                ship.moving_right=False
            elif event.key==pygame.K_LEFT:
                ship.moving_left=False
            elif event.key==pygame.K_UP:
                ship.moving_up=False
            elif event.key==pygame.K_DOWN:
                ship.moving_down=False
            elif event.key==pygame.K_SPACE:
                bullet_always.fire=False
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """在玩家单击play或p时开始游戏"""
    #重置游戏设置
    ai_settings.initializee_dynamic_settings()
    #隐藏光标
    pygame.mouse.set_visible(False)
    #重置游戏统计信息
    stats.reset_stats()
    stats.game_active=True
    #重置记分牌图像
    sb.prep_level()
    sb.prep_high_score()
    sb.prep_score()
    sb.prep_ships()
    #使游戏初始化
    aliens.empty()
    bullets.empty()
    create_aliens(ai_settings,screen,ship,aliens)
    ship.center_ship()
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bullet_always):
    """更新子弹的位置，删除已消失的子弹"""
    if bullet_always.fire:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
    bullets.update()   
    #删除已消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
    #检查是否有子弹击中了alien，若是，则删除该alien
    collisions=pygame.sprite.groupcollide(bullets,aliens,False,True)
    """击落飞船就计分，确保被消灭的aliens都能计分"""
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
            """检查是否诞生了新的最高分"""
        if stats.score>=stats.high_score:
            stats.high_score=stats.score
            sb.prep_high_score()
    #删除现有的子弹并新建一群aliens
    if len(aliens)==0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()
        create_aliens(ai_settings,screen,ship,aliens)
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.draw_score()
    #如果游戏处于非活跃状态
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()
def create_aliens(ai_settings,screen,ship,aliens):
    """创建alien群"""
    #创建一个alien，并计算一行可容纳多少alien,alien间距为alien宽度
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    available_space_x=ai_settings.screen_width-alien_width
    number_aliens_x=int(available_space_x/(2*alien_width))
    #计算屏幕可容纳多少行alien
    ship_height=ship.rect.height
    alien_height=alien.rect.height
    available_space_y=ai_settings.screen_height-3*alien_height-ship_height
    number_rows=int(available_space_y/(2*alien_height))
    
    #创建duo行alien
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien=Alien(ai_settings,screen)
            alien.x=alien_width+2*alien_width*alien_number
            alien.rect.x=alien.x
            alien.rect.y=alien_height+2*alien_height*row_number
            aliens.add(alien)
def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """更新alien位置"""
    #向左或向右移动alien
    for alien in aliens.sprites():
        alien.x+=alien.ai_settings.alien_speed_factor*alien.ai_settings.fleet_direction
        alien.rect.x=alien.x
    #alien碰到边缘
    for alien in aliens.sprites():
        if alien.check_edgs():
            #将整群alien下移，并改变他们的方向
            for alien in aliens.sprites():
                alien.rect.y+=ai_settings.fleet_drop_speed
            ai_settings.fleet_direction*=-1
            break
    
    #检测飞船和alien的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
    
    #检查alien是否到底部
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
            break
def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    """响应被alien撞到的飞船"""
    if stats.ships_left>0:
        #将飞船数减一
        stats.ships_left-=1
        #更新剩余飞船
        sb.prep_ships()
        #清空alien列表和子弹列表
        aliens.empty()
        bullets.empty()
        #将alien和飞船归位
        create_aliens(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停一会
        sleep(0.55)
    else:
        stats.game_active=False
        #显示光标
        pygame.mouse.set_visible(True)
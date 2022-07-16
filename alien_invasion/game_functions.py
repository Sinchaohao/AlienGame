# @Author:sch
# @Time:2022/07/13
# @File:game_functions.py
# @software: PyCharm

import sys
import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.K_q:
            sys.exit()

def update_screen(ai_settings, screen, ship, bullets, aliens):
    """更新屏幕上的图像，并切换到新屏幕"""

    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove( bullet )
    # for bullet in bullets.copy():
    #     if bullet.rect.buttom <= 0:
    #         bullets.remove(bullet)

def update_aliens(aliens):
    aliens.update()

def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, alien_width, alien_number, number_rows):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + (2 * alien.rect.height) * number_rows
    alien.rect.x = alien.x
    return alien


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)

    # 创建多行外星人
    for row in range(number_rows):
        for i in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            aliens.add(create_alien(ai_settings, screen, alien_width, i, row))


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""

    available_space_y = ai_settings.screen_height - (5 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows



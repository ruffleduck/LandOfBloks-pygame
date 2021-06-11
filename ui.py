import math

import pygame

from text import Text
from blocks import *
from tools import *

scale_size = 50
tree = pygame.transform.scale(tree, [scale_size, scale_size])
fruit_tree = pygame.transform.scale(fruit_tree, [scale_size, scale_size])
mine = pygame.transform.scale(mine, [scale_size, scale_size])

apple = pygame.image.load('img/ui/apple.gif')
coin = pygame.image.load('img/ui/coin.gif')

pygame.init()


def health_to_hearts(health, max_health):
    i = math.ceil(health / 5)
    length = math.ceil(max_health / 10)
    hearts = []
    for _ in range(length):
        if i > 1:
            hearts.append('full')
            i -= 2
        elif i == 1:
            hearts.append('half')
            i -= 1
        else:
            hearts.append('empty')
    return hearts


def draw_hearts(player_hearts, screen, Y, X=10):
    x = X
    y = Y
    for i in player_hearts:
        screen.blit(img[i], [x, y])
        x += 40
        newlineX = 230 if X == 10 else 1730
        if x > newlineX:
            x = X
            y += 40


def draw_inventory(inventory, index, screen, Y, X=10):
    y = Y
    x = X
    for z, i in enumerate(inventory):
        size = [45, 45]
        if i == 'food':
            image = pygame.transform.scale(apple, size)
        elif isinstance(i, Tool):
            image = pygame.transform.scale(i.image, size)
        elif i in [WoodWall, StoneWall, Windmill, SpikyWall, FasterWindmill, \
                   BoosterPad, FastestWindmill, VerySpikyWall]:
            image = pygame.transform.scale(i.image, size)
        else:
            raise ValueError("Unknown item in inventory: %s" % i)
        if z == index:
            pygame.draw.rect(screen, [255, 255, 255], [x, y, 50, 50], 4)
        else:
            pygame.draw.rect(screen, [255, 255, 255], [x, y, 50, 50], 2)
        screen.blit(image, [x + 3, y + 3])
        x += 65
        newlineX = 230 if X == 10 else 1780
        if x > newlineX:
            x = X
            y += 65


def draw_resource(img, quantity, screen, pos, small=False):
    img_pos = pos
    if small:
        img_pos = [pos[0], pos[1] + 15]
    screen.blit(img, img_pos)
    Text(large_font if not small else font, [pos[0] + (60 if not small else 35), pos[1] + 18], "x %s" % quantity).render(screen)


def render_ui(player1, player2, screen):
    p1_hearts = health_to_hearts(player1.health, player1.max_health)
    p2_hearts = health_to_hearts(player2.health, player2.max_health)
    
    pygame.draw.rect(screen, [0, 0, 0], [0, 0, 300, 925])
    pygame.draw.rect(screen, [0, 0, 0], [1521, 0, 300, 925])

    inventory1 = player1.tools + ['food'] + player1.inventory
    inventory2 = player2.tools + ['food'] + player2.inventory

    # Player 2

    Text(large_font, [150, 40], "Player 2", center=True).render(screen)

    Text(font, [10, 100], "Level %s" % (player2.level+1)).render(screen)
    Text(font, [10, 133], "XP").render(screen)
    pygame.draw.rect(screen, [255, 255, 255], [80, 130, 200, 20], 2)
    if player2.xp > 0:
        pygame.draw.rect(screen, [0, 147, 255], [82, 132, player2.xp * 2, 17])

    draw_hearts(p2_hearts, screen, 175)

    draw_resource(tree, player2.resources['wood'], screen, [10, 266])
    draw_resource(mine, player2.resources['stone'], screen, [10, 326])
    draw_resource(fruit_tree, player2.resources['food'], screen, [10, 386])

    draw_inventory(inventory2, player2.index, screen, 500)

    Text(large_font, [10, 700], "Cost:").render(screen)
    try:
        Text(font, [10, 740], "Wood: %s" % inventory2[player2.index].cost['wood']).render(screen)
        Text(font, [10, 770], "Stone: %s" % inventory2[player2.index].cost['stone']).render(screen)
    except AttributeError:
        Text(font, [10, 740], "Wood: 0").render(screen)
        Text(font, [10, 770], "Stone: 0").render(screen)

    draw_resource(coin, player2.coins, screen, [10, 820], small=True)

    # Player 1

    Text(large_font, [1680, 40], "Player 1", center=True).render(screen)

    Text(font, [1530, 100], "Level %s" % (player1.level+1)).render(screen)
    Text(font, [1530, 133], "XP").render(screen)
    pygame.draw.rect(screen, [255, 255, 255], [1590, 130, 200, 20], 2)
    if player1.xp > 0:
        pygame.draw.rect(screen, [0, 147, 255], [1592, 132, player1.xp * 2, 17])

    draw_hearts(p1_hearts, screen, 175, X=1530)

    draw_resource(tree, player1.resources['wood'], screen, [1530, 266])
    draw_resource(mine, player1.resources['stone'], screen, [1530, 326])
    draw_resource(fruit_tree, player1.resources['food'], screen, [1530, 386])

    draw_inventory(inventory1, player1.index, screen, 500, X=1535)

    Text(large_font, [1530, 700], "Cost:").render(screen)
    try:
        Text(font, [1530, 740], "Wood: %s" % inventory1[player1.index].cost['wood']).render(screen)
        Text(font, [1530, 770], "Stone: %s" % inventory1[player1.index].cost['stone']).render(screen)
    except AttributeError:
        Text(font, [1530, 740], "Wood: 0").render(screen)
        Text(font, [1530, 770], "Stone: 0").render(screen)

    draw_resource(coin, player1.coins, screen, [1530, 820], small=True)


img = {
    'full': pygame.image.load('img/ui/full_heart.gif'),
    'half': pygame.image.load('img/ui/half_heart.gif'),
    'empty': pygame.image.load('img/ui/empty_heart.gif')
}

large_font = pygame.font.Font("8bitFontBold.ttf", 30)
font = pygame.font.Font("8bitFontBold.ttf", 24)



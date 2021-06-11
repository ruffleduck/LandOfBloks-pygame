import math

import pygame

pygame.init()

screen = pygame.display.set_mode([500, 500])


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
    #print(len(hearts))
    return hearts


health = 25
max_health = 30

img = {
    'full': pygame.image.load('full_heart.gif'),
    'half': pygame.image.load('half_heart.gif'),
    'empty': pygame.image.load('empty_heart.gif')
}

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                health += 1
            else:
                health -= 1

    screen.fill([255, 255, 255])

    x = 10
    y = 100
    for i in health_to_hearts(health, max_health):
        if x > 330:
            x = 10
            y += 30
        screen.blit(img[i], [x, y])
        x += 50
    
    pygame.display.update()

pygame.quit()

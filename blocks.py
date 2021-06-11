import time

import pygame

pygame.init()

tree = pygame.image.load('img/tree.gif')
mine = pygame.image.load('img/mine.gif')
fruit_tree = pygame.image.load('img/fruit_tree.gif')
gold_mine = pygame.image.load('img/gold_mine.gif')

wood_wall = pygame.image.load('img/wood_wall.gif')
stone_wall = pygame.image.load('img/stone_wall.gif')
spiky_wall = pygame.image.load('img/spiky_wall.gif')
very_spiky_wall = pygame.image.load('img/very_spiky_wall.gif')
windmill = pygame.image.load('img/windmill_1.gif')


class NaturalBlock:
    image = None
    
    def __init__(self, position, block_size):
        self.position = (position[0] * block_size + 15, position[1] * block_size + 15)
    
    def render(self, screen):
        screen.blit(self.__class__.image, self.position)


class Tree(NaturalBlock):
    image = tree


class Mine(NaturalBlock):
    image = mine


class FruitTree(NaturalBlock):
    image = fruit_tree


class GoldMine(NaturalBlock):
    image = gold_mine


class Block:
    def render(self, screen, position):
        screen.blit(self.__class__.image, position)


class WoodWall(Block):
    image = wood_wall
    start_health = 35
    cost = {'stone': 10, 'wood': 10}
    name = "Wood wall"

    def __init__(self):
        self.last_player = None
        self.health = self.__class__.start_health


class Windmill(Block):
    start_health = 35
    cost = {'stone': 10, 'wood': 30}
    coins_per_second = 1
    name = "Windmill"
    image = windmill

    def __init__(self, player):
        self.owner = player
        self.last_turned = 0
        self.last_gave = 0
        self.last_player = None
        self.health = self.__class__.start_health
        self.frame = 1

    def turn(self):
        return time.time() - self.last_turned > 0.4

    def render(self, screen, position):
        if self.turn():
            self.frame = 1 if self.frame == 2 else 2
            self.last_turned = time.time()
        if self.frame == 2:
            position[0] -= 13
            position[1] -= 11
        screen.blit(pygame.image.load('img/windmill_%s.gif' % self.frame), position)

    def give_coins(self):
        if time.time() - self.last_gave > 1:
            self.owner.coins += Windmill.coins_per_second
            self.last_gave = time.time()


class StoneWall(Block):
    image = stone_wall
    start_health = 60
    cost = {'stone': 20, 'wood': 20}
    name = "Stone wall"

    def __init__(self):
        self.last_player = None
        self.health = self.__class__.start_health


class SpikyWall(Block):
    image = spiky_wall
    start_health = 50
    cost = {'stone': 30, 'wood': 20}
    damage_per_hit = 5
    name = "Spiky wall"

    def __init__(self):
        self.last_player = None
        self.health = self.__class__.start_health


class VerySpikyWall(Block):
    image = very_spiky_wall
    start_health = 50
    cost = {'stone': 40, 'wood': 20}
    damage_per_hit = 10
    name = "Very spiky wall"

    def __init__(self):
        self.last_player = None
        self.health = self.__class__.start_health


class BoosterPad(Block):
    start_health = 45
    cost = {'stone': 40, 'wood': 15}
    name = "Booster pad"
    image = pygame.image.load('img/booster_pad_right.gif')

    def __init__(self, direction):
        self.last_player = None
        self.health = self.__class__.start_health
        self.direction = direction

    def render(self, screen, position):
        screen.blit(pygame.image.load('img/booster_pad_%s.gif' % self.direction), position)


class FasterWindmill(Block):
    image = windmill
    start_health = 40
    cost = {'stone': 15, 'wood': 45}
    coins_per_second = 3
    name = "Faster windmill"

    def __init__(self, player):
        self.owner = player
        self.last_turned = 0
        self.last_gave = 0
        self.last_player = None
        self.health = self.__class__.start_health
        self.frame = 1

    def turn(self):
        return time.time() - self.last_turned > 0.3

    def render(self, screen, position):
        if self.turn():
            self.frame = 1 if self.frame == 2 else 2
            self.last_turned = time.time()
        if self.frame == 2:
            position[0] -= 13
            position[1] -= 11
        screen.blit(pygame.image.load('img/windmill_%s.gif' % self.frame), position)

    def give_coins(self):
        if time.time() - self.last_gave > 1:
            self.owner.coins += FasterWindmill.coins_per_second
            self.last_gave = time.time()


class FastestWindmill(Block):
    image = windmill
    start_health = 45
    cost = {'stone': 20, 'wood': 85}
    coins_per_second = 6
    name = "Fastest windmill"

    def __init__(self, player):
        self.owner = player
        self.last_turned = 0
        self.last_gave = 0
        self.last_player = None
        self.health = self.__class__.start_health
        self.frame = 1

    def turn(self):
        return time.time() - self.last_turned > 0.2

    def render(self, screen, position):
        if self.turn():
            self.frame = 1 if self.frame == 2 else 2
            self.last_turned = time.time()
        if self.frame == 2:
            position[0] -= 13
            position[1] -= 11
        screen.blit(pygame.image.load('img/windmill_%s.gif' % self.frame), position)

    def give_coins(self):
        if time.time() - self.last_gave > 1:
            self.owner.coins += FastestWindmill.coins_per_second
            self.last_gave = time.time()



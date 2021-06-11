import random
import time
import math
import copy
import os

import pygame

from tools import *
from blocks import *

pygame.init()

player1_img = {
    'down': pygame.image.load('img/characters/P1/down.gif'),
    'right': pygame.image.load('img/characters/P1/right.gif'),
    'left': pygame.image.load('img/characters/P1/left.gif'),
    'up': pygame.image.load('img/characters/P1/up.gif'),
    'down_hurt': pygame.image.load('img/characters/P1/down_hurt.gif'),
    'right_hurt': pygame.image.load('img/characters/P1/right_hurt.gif'),
    'left_hurt': pygame.image.load('img/characters/P1/left_hurt.gif'),
    'up_hurt': pygame.image.load('img/characters/P1/up_hurt.gif')
}


player2_img = {
    'down': pygame.image.load('img/characters/P2/down.gif'),
    'right': pygame.image.load('img/characters/P2/right.gif'),
    'left': pygame.image.load('img/characters/P2/left.gif'),
    'up': pygame.image.load('img/characters/P2/up.gif'),
    'down_hurt': pygame.image.load('img/characters/P2/down_hurt.gif'),
    'right_hurt': pygame.image.load('img/characters/P2/right_hurt.gif'),
    'left_hurt': pygame.image.load('img/characters/P2/left_hurt.gif'),
    'up_hurt': pygame.image.load('img/characters/P2/up_hurt.gif')
}


def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


class Player:
    speed = 0.15
    hit_speed = 0.5
    flash_time = 0.15
    
    @classmethod
    def find_spot(cls, map, block_size, other_pos):
        spot = [0, 0]
        spot[0] = random.randint(5, len(map[0]) - 7)
        spot[1] = random.randint(0, len(map) - 2)
        
        while map[spot[1]][spot[0]] != None and distance(spot, other_pos) > 5:
            spot[0] = random.randint(5, len(map[0]) - 7)
            spot[1] = random.randint(0, len(map) - 2)

        spot[0] *= block_size
        spot[1] *= block_size
        spot = [spot[0] + 15, spot[1] + 15]
        return spot

    def __init__(self, map, controls, use_key, other_pos, player_img, turn_key):
        self.position = Player.find_spot(map, 56, other_pos)
        self.player_img = player_img
        self.other_pos = other_pos
        self.controls = controls
        self.move_time = Player.speed
        self.hit_time = Player.hit_speed
        self.direction = 'down'
        self.use_key = use_key
        self.being_hurt = False
        self.last_flashed = 0
        self.last_added = 0
        self.level = 0
        self.index = 0
        self.turn_key = turn_key

        self.inventory = [WoodWall, Windmill]#, StoneWall, SpikyWall,
                          #FasterWindmill, BoosterPad, FastestWindmill, VerySpikyWall]
        self.tools = [Standard()]
        self.resources = {
            'wood': 0,
            'stone': 0,
            'food': 0
        }
        
        self.max_health = 60
        self.health = self.max_health
        self.coins = 0
        self.xp = 0

    def render(self, screen):
        image = self.player_img[self.direction + ('' if not self.being_hurt else '_hurt')]
        screen.blit(image, [self.position[0], self.position[1]])

    def flash(self):
        self.being_hurt = True
        self.last_flashed = time.time()

    def stop_flash(self):
        if time.time() - self.last_flashed > Player.flash_time:
            self.being_hurt = False

    def moveable(self):
        return time.time() - self.move_time > Player.speed

    def hitable(self):
        return time.time() - self.hit_time > Player.hit_speed
        

    def move(self, direction, map, other_player, players, turning=False):
        self.direction = direction
        self.move_time = time.time()

        if turning: return

        inventory = self.tools + ['food'] + self.inventory
        
        old_pos = copy.deepcopy(self.position)
        
        if direction == 'up':
            self.position[1] -= 56
        elif direction == 'down':
            self.position[1] += 56
        elif direction == 'left':
            self.position[0] -= 56
        elif direction == 'right':
            self.position[0] += 56

        try:
            block = map[self.position[1] // 56][self.position[0] // 56]
        except IndexError:
            pass
        
        if self.position[1] // 56 > len(map) - 1 or \
           self.position[0] // 56 > len(map[0]) - 6 or \
           self.position[0] < 300 or \
           self.position[1] < 0:
            # Undo the move
            self.position = old_pos
        elif block != None:
            if not isinstance(block, BoosterPad):
                self.position = old_pos

            # Give resources
            if self.hitable() and isinstance(inventory[self.index], Tool):
                if isinstance(block, Tree):
                    self.resources['wood'] += inventory[self.index].resources
                elif isinstance(block, Mine):
                    self.resources['stone'] += inventory[self.index].resources
                elif isinstance(block, FruitTree):
                    self.resources['food'] += inventory[self.index].resources
                elif isinstance(block, GoldMine):
                    self.coins += inventory[self.index].resources
                elif isinstance(block, SpikyWall) or isinstance(block, VerySpikyWall):
                    block.health -= inventory[self.index].wall_damage // 2
                    block.last_player = self
                    self.health -= block.damage_per_hit
                    self.flash()
                elif isinstance(block, BoosterPad):
                    pass
                else:
                    block.health -= inventory[self.index].wall_damage // 2
                    block.last_player = self

                self.xp += 1

                self.hit_time = time.time()

        if self.position == other_player.position:
            self.position = old_pos
            
            other_player.health -= 5
            other_player.flash()
            
            self.health -= 5
            self.flash()
        


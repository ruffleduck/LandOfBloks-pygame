import random
import time
import math
import sys
import os

import pygame

from player import Player, distance, player1_img, player2_img
from ui import render_ui
from blocks import *
from tools import *

# Setup
pygame.init()

width = 1821
height = 896

screen = pygame.display.set_mode([width, 925])
clock = pygame.time.Clock()

pygame.display.set_caption("Land of Bloks")

block_size = 56

# Colors
WHITE = (255, 255, 255)

# Images
tiles = [
    pygame.image.load('img/tiles/tile1.gif'),
    pygame.image.load('img/tiles/tile2.gif'),
    pygame.image.load('img/tiles/tile3.gif')
]


def make_background():
    background = []
    for _ in range(height // block_size + 1):
        row = []
        for _ in range(width // block_size):
            row.append(random.randint(0, len(tiles) - 1))
        background.append(row)
    return background


def render_background(background):
    x = 0
    y = 0
    for row in background:
        for col in row:
            screen.blit(tiles[col], [x + 30, y])
            x += block_size
        y += block_size
        x = 0


def create_map():
    map = []
    for row in range(height // block_size):
        map_row = []
        for col in range(width // block_size):
            if col > 4 and col < width // block_size - 4:
                num = random.randint(1, 160)
                if num < 135:
                    map_row.append(None)
                elif num < 150:
                    if random.randint(1, 2) == 1:
                        map_row.append(Tree([col, row], block_size))
                    else:
                        map_row.append(Mine([col, row], block_size))
                else:
                    if random.randint(1, 2) == 1:
                        map_row.append(FruitTree([col, row], block_size))
                    else:
                        map_row.append(GoldMine([col, row], block_size))
            else:
                map_row.append(None)
        map.append(map_row)
    return map


def render_map(map):
    x = 0
    y = 0
    for row in map:
        for col in row:
            if col != None:
                try:
                    col.render(screen)
                except TypeError:
                    col.render(screen, [x+15, y+25])
            x += block_size
        y += block_size
        x = 0


def place_block(player):
    inventory = player.tools + ['food'] + player.inventory

    if not (player.resources['wood'] >= inventory[player.index].cost['wood'] and \
       player.resources['stone'] >= inventory[player.index].cost['stone']):
        # If the player doesn't have enough resources, decline and tell user
        more_wood = inventory[player.index].cost['wood'] - player.resources['wood']
        more_stone = inventory[player.index].cost['stone'] - player.resources['stone']
        return
        
    try:
        block_to_place = inventory[player.index]()
    except TypeError:
        try:
            block_to_place = inventory[player.index](direction=player.direction)
        except TypeError:
            block_to_place = inventory[player.index](player)
    
    accept = True
    x = player.position[0] // block_size
    y = player.position[1] // block_size

    if player.direction == 'up':
        block_pos = (x, y - 1)
    elif player.direction == 'down':
        block_pos = (x, y + 1)
    elif player.direction == 'left':
        block_pos = (x - 1, y)
    elif player.direction == 'right':
        block_pos = (x + 1, y)
    
    try:
        accept = map[block_pos[1]][block_pos[0]] == None
    except IndexError:
        accept = False

    if accept:
        map[block_pos[1]][block_pos[0]] = block_to_place

        # Take the resources from the player
        player.resources['wood'] -= inventory[player.index].cost['wood']
        player.resources['stone'] -= inventory[player.index].cost['stone']


background = make_background()
map = create_map()

# Players
player1 = Player(map, {pygame.K_DOWN: 'down', pygame.K_UP: 'up',
                       pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'},
                 pygame.K_SPACE, (-5, -5), player1_img, pygame.K_RSHIFT)
player2 = Player(map, {pygame.K_s: 'down', pygame.K_w: 'up',
                       pygame.K_a: 'left', pygame.K_d: 'right'},
                 pygame.K_q, player1.position, player2_img, pygame.K_TAB)

players = (player1, player2)

keys = []

# Play music
pygame.mixer.music.load('sounds/land_of_bloks.wav')
pygame.mixer.music.play(-1)

# Load SFX
axe = pygame.mixer.Sound('sounds/axe.wav')
pickaxe = pygame.mixer.Sound('sounds/pickaxe.wav')
death = pygame.mixer.Sound('sounds/game_over.wav')

# Game loop
done = False
while not done:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            keys.append(event.key)

            inventory1 = player1.tools + ['food'] + player1.inventory
            inventory2 = player2.tools + ['food'] + player2.inventory

            if event.key == pygame.K_n:
                player1.index -= 1
                if player1.index < 0:
                    player1.index = 0

            if event.key == pygame.K_m:
                player1.index += 1
                if player1.index > len(inventory1) - 1:
                    player1.index = len(inventory1) - 1

            if event.key == pygame.K_1:
                player2.index -= 1
                if player2.index < 0:
                    player2.index = 0

            if event.key == pygame.K_2:
                player2.index += 1
                if player2.index > len(inventory2) - 1:
                    player2.index = len(inventory2) - 1
                
        if event.type == pygame.KEYUP:
            try:
                keys.remove(event.key)
            except ValueError:
                pass

    for player in players:
        player.stop_flash()
        
        for key in keys:
            if key == player.use_key and player.hitable():
                x = player.position[0] // block_size
                y = player.position[1] // block_size

                inventory = player.tools + ['food'] + player.inventory
                use_tool = False
                
                if inventory[player.index] == 'food' and \
                   player.resources['food'] > 0 and \
                   player.health < player.max_health:
                    # Regenerate some health
                    player.health += 5
                    player.resources['food'] -= 1
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif isinstance(inventory[player.index], Tool):
                    use_tool = True
                elif inventory[player.index] in [WoodWall, StoneWall, Windmill, SpikyWall, FasterWindmill, \
                   BoosterPad, FastestWindmill, VerySpikyWall]:
                    # Place a block
                    place_block(player)

                # Contains all of the blocks around the player
                blocks = [
                    (x, y - 1),
                    (x - 1, y - 1),
                    (x + 1, y - 1),
                    (x - 1, y),
                    (x + 1, y),
                    (x, y + 1),
                    (x - 1, y + 1),
                    (x + 1, y + 1)
                ]

                if use_tool:
                    # Collect resources and break walls
                    axe_num = 0
                    pickaxe_num = 0
                    for pos in blocks:
                        if pos[1] < len(map) and pos[1] >= 0 and \
                           pos[0] < len(map[0]) and pos[0] >= 0:
                            # Give resource
                            block = map[pos[1]][pos[0]]
                            player.xp += 1
                            if isinstance(block, Tree):
                                player.resources['wood'] += inventory[player.index].resources
                                axe_num += 1
                            elif isinstance(block, Mine):
                                player.resources['stone'] += inventory[player.index].resources
                                pickaxe_num += 1
                            elif isinstance(block, FruitTree):
                                player.resources['food'] += inventory[player.index].resources
                                axe_num += 1
                            elif isinstance(block, GoldMine):
                                player.coins += inventory[player.index].resources
                                pickaxe_num += 1
                            elif block == None:
                                player.xp -= 1
                            else:
                                block.last_player = player
                                block.health -= inventory[player.index].wall_damage
                                if isinstance(block, SpikyWall) or isinstance(block, VerySpikyWall):
                                   player.health -= block.damage_per_hit
                                   player.flash()
                    if axe_num > 0 and pickaxe_num > 0:
                        (pickaxe if pickaxe_num > axe_num else axe).play()
                    elif axe_num > 0:
                        axe.play()
                    elif pickaxe_num > 0:
                        pickaxe.play()

                    # Damage opponents
                    other_players = list(players[:])
                    other_players.remove(player)
                    for x in other_players:
                        tool_range = inventory[player.index].damage_range
                        tool_damage = inventory[player.index].damage
                        lucky = random.randint(1, 100) < inventory[player.index].hit_chance * 100
                        if distance(x.position, player.position) // 56 <= tool_range and lucky:
                            if isinstance(inventory[player.index], Bow) and player.resources['wood'] > 0:
                                player.resources['wood'] -= 1
                                x.health -= tool_damage
                                x.flash()
                            else:
                                x.health -= tool_damage
                                x.flash()
                
                player.hit_time = time.time()
            
            if key in player.controls.keys() and player.moveable():
                player_list = list(players)
                player_list.remove(player)
                other_player = player_list[0]

                turning = player.turn_key in keys
                player.move(player.controls[key], map, other_player, players, turning=turning)

    # Destroys any blocks that were destroyed
    for i, row in enumerate(map):
        for j, x in enumerate(row):
            if isinstance(x, Tree) or \
               isinstance(x, Mine) or \
               isinstance(x, FruitTree) or \
               isinstance(x, GoldMine) or \
               x == None:
                pass
            else:
                if x.health <= 0:
                    x.last_player.resources['wood'] += x.cost['wood']
                    x.last_player.resources['stone'] += x.cost['stone']
                    map[i][j] = None

    # Checks to see if somebody won
    for player in players:
        refill = True
        if player.coins >= 3000:
            os.system('clear')
            print("CONGRATULATIONS! Player %s won!" % (players.index(player) + 1))
            sys.exit(0)
        elif player.coins >= 500 and player.max_health < 120:
            player.max_health = 120
        elif player.coins >= 400 and player.max_health < 110:
            player.max_health = 110
        elif player.coins >= 300 and player.max_health < 100:
            player.max_health = 100
        elif player.coins >= 200 and player.max_health < 90:
            player.max_health = 90
        elif player.coins >= 100 and player.max_health < 80:
            player.max_health = 80
        elif player.coins >= 50 and player.max_health < 70:
            player.max_health = 70
        else:
            refill = False

        if refill:
            player.health = player.max_health

    # Checks to see if anybody died
    for i, player in enumerate(players):
        if player.health <= 0:
            coins = player.coins
            player.__init__(map, player.controls,
                            player.use_key, player.other_pos,
                            player.player_img, player.turn_key)
            player.coins = coins // 2
            players[i - 1].coins += math.ceil(coins / 2)

            players[i - 1].xp += 50

            death.play()

    # Gives coins to players with windmills
    for row in map:
        for x in row:
            if isinstance(x, Windmill) or \
               isinstance(x, FasterWindmill) or \
               isinstance(x, FastestWindmill):
                # Give coins
                x.give_coins()

    # Updates people's inventory and tools when they got 100 XP
    for player in players:
        if player.xp >= 100:
            player.xp = 0
            player.level += 1

            if player.level == 1:
                player.inventory.append(StoneWall)
                player.tools.append(Axe())
                player.inventory.remove(WoodWall)
                del player.tools[0]  # Removes the standard tool
            elif player.level == 2:
                player.inventory.append(SpikyWall)
                player.inventory.append(FasterWindmill)
                player.tools.append(Bow())
                player.inventory.remove(Windmill)
            elif player.level == 3:
                player.inventory.append(BoosterPad)
                player.tools.append(Sword())
            elif player.level == 4:
                player.inventory.append(FastestWindmill)
                player.inventory.append(VerySpikyWall)
                player.tools.append(Pickaxe())
                player.inventory.remove(FasterWindmill)
                player.inventory.remove(SpikyWall)
                del player.tools[0]  # Removes the axe

    # Moves players if they are on a booster pad
    for player in players:
        pos = player.position[0] // block_size, player.position[1] // block_size
        block = map[pos[1]][pos[0]]
        if isinstance(block, BoosterPad):
            if block.direction == 'up':
                player.position[1] -= 56
            elif block.direction == 'down':
                player.position[1] += 56
            elif block.direction == 'left':
                player.position[0] -= 56
            elif block.direction == 'right':
                player.position[0] += 56
            player.direction = block.direction

    # Fill screen
    screen.fill(WHITE)

    # Display graphics
    render_background(background)
    render_map(map)
    
    for player in players:
        player.render(screen)

    render_ui(player1, player2, screen)
    
    # Update screen
    pygame.display.update()

    # Tick
    clock.tick(20)

os.system('clear')

# Quit
pygame.quit()

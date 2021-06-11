import pygame

pygame.init()

standard_tool = pygame.image.load('img/tools/standard_tool.gif')
pickaxe = pygame.image.load('img/tools/pickaxe.gif')
axe = pygame.image.load('img/tools/axe.gif')
sword = pygame.image.load('img/tools/sword.gif')
bow = pygame.image.load('img/tools/bow.gif')


class Tool:
    resources = 0
    damage = 0
    wall_damage = 0
    damage_range = 0
    hit_chance = 0.85


class Standard(Tool):
    image = standard_tool
    resources = 1
    damage = 5
    damage_range = 1
    wall_damage = 5

    def __init__(self):
        self.name = "Standard"


class Axe(Tool):
    image = axe
    resources = 2
    damage = 8
    damage_range = 2
    wall_damage = 7

    def __init__(self):
        self.name = "Axe"


class Sword(Tool):
    image = sword
    resources = 1
    damage = 15
    damage_range = 2
    wall_damage = 7

    def __init__(self):
        self.name = "Sword"


class Bow(Tool):
    image = bow
    damage = 10
    damage_range = 6
    hit_chance = 0.75

    def __init__(self):
        self.name = "Bow"


class Pickaxe(Tool):
    image = pickaxe
    resources = 3
    damage = 8
    damage_range = 3
    wall_damage = 12

    def __init__(self):
        self.name = "Pickaxe"

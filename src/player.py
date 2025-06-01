# player.py
import pygame
from settings import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

    def move(self, dx, dy, game_map):
        if game_map.is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
            
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

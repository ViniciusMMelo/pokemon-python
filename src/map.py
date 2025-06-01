# map.py
import pygame
from settings import *

class Map:
    def __init__(self):
        self.name = "map"
        self.tiles = []
        self.pokemon_spots = []
        self.exit = []
        self.load_new_map(self.name)
        

    def load_map(self, filename):
        with open(f"data/{filename}.txt") as f:
            lines = f.readlines()
        map_data = []
        spots = []
        exit = []

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                if char == 'P':
                    spots.append((x, y))
                    row.append('.')  # substitui P por chão
                elif char == 'E':
                    
                    exit.append((x, y))
                    
                    row.append('.')  # substitui P por chão
                else:
                    row.append(char)
            map_data.append(row)

        self.pokemon_spots = spots
        
        self.exit = exit

        return map_data

    def load_new_map(self, filename):
        self.tiles = self.load_map(filename)

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                color = GRASS
                if tile == 'W':
                    color = WALL
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    def is_walkable(self, x, y):
        try:
            return self.tiles[y][x] != 'W'
        except IndexError:
            return False
        
    def load_from_file(self, filename):
        with open(filename, "r") as f:
            self.data = [line.strip() for line in f.readlines()]


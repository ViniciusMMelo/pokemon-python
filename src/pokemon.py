import pygame
from settings import *
import os

class Pokemon:
    def __init__(self, x, y, atributos, name="???"):
        self.x = x
        self.y = y
        self.atributos = atributos
        self.name = name

        # Caminho da imagem baseado no nome do Pokémon
        img_path = os.path.join("assets", "imagens", "pokemons", f"{name.lower()}.png")
        # img_path = os.path.join("assets", "imagens", "pokemons", f"pokemon1.png")
        
        try:
            image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        except FileNotFoundError:
            # Se a imagem não for encontrada, usa uma cor de fallback
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(GRASS)

    def draw(self, screen):
        screen.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))

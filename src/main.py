import pygame
from game import Game
from start_screen import get_player_name

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokemon Game")

player_name = get_player_name(screen)

game = Game(screen, player_name)
clock = pygame.time.Clock()
game.run(clock)

pygame.quit()
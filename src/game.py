# game.py
import pygame
import os
import json
import random
from settings import *
from player import Player
from map import Map
from pokemon import Pokemon

class Game:
    def __init__(self, screen, player_name):
        self.screen = screen
        self.player_name = player_name
        self.map = Map()
        self.pokemons = self.load_pokemons()
        self.player = Player(2, 2, (255, 0, 0))
        self.all_sprites = pygame.sprite.Group(self.player)
        self.exit = self.map.exit
        self.captured_count = 0
        self.last_captured = []
        self.next_map_ready = False

    def load_pokemons(self):
        with open(POKEMON_FILE) as f:
            data = json.load(f)

        # Copia os locais possíveis do mapa
        available_spots = self.map.pokemon_spots[:]
        random.shuffle(available_spots)
        random.shuffle(data)
        pokemons = []
        for i, p in enumerate(data):
            if i < len(available_spots):
                x, y = available_spots[i]
                
                pokemons.append(Pokemon(x, y, p["atributos"], p["name"]))
        return pokemons

    def run(self, clock):
        running = True
        message = ""
        pokemon_encontrado = None

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move(-1, 0, self.map)
                    elif event.key == pygame.K_RIGHT:
                        self.player.move(1, 0, self.map)
                    elif event.key == pygame.K_UP:
                        self.player.move(0, -1, self.map)
                    elif event.key == pygame.K_DOWN:
                        self.player.move(0, 1, self.map)
                    
                    pokemon_encontrado = self.check_pokemon_collision()
                    if pokemon_encontrado:
                        message = f"{pokemon_encontrado.name} apareceu! Pressione [C] para capturar."
                    else:
                        message = "Procure os pokémons..."

                    if event.key == pygame.K_c and pokemon_encontrado:
                        message = f"{pokemon_encontrado.name} capturado!"
                        self.save_captured(pokemon_encontrado)
                        self.pokemons.remove(pokemon_encontrado)
                        self.captured_count += 1
                        self.last_captured.insert(0, pokemon_encontrado.name)
                        self.last_captured = self.last_captured[:3]
                        pokemon_encontrado = None

                        if self.captured_count >= 3:
                            message = "Você capturou 3 pokémons! Pressione [M] para ir para outro mapa."
                            self.next_map_ready = True

                    elif event.key == pygame.K_m and self.next_map_ready:
                        self.change_map()
                        message = "Novo mapa carregado!"
                        self.next_map_ready = False
                    
                    exit = self.check_exit_collision()
                    if exit:
                        message = f"Você encontrou uma saida! Pressione [S] para trocar de mapa."

                    if event.key == pygame.K_s and exit:
                        self.change_map()
                        message = "Novo mapa carregado!"
                        self.next_map_ready = False

            # Desenha tudo
            self.screen.fill(WHITE)
            self.map.draw(self.screen)

            for p in self.pokemons:
                p.draw(self.screen)

            self.all_sprites.draw(self.screen)

            # Mostrar mensagens e UI
            self.draw_ui(message, pokemon_encontrado)

            pygame.display.flip()

    def check_pokemon_collision(self):
        for pokemon in self.pokemons:
            if pokemon.x == self.player.x and pokemon.y == self.player.y:
                return pokemon
        return None
    def check_exit_collision(self):
        print(self.exit)
        for exit in self.exit:
            if exit[0] == self.player.x and exit[1] == self.player.y:
                return exit
        return None
    def save_captured(self, pokemon):
        save_file = "data/capturados.json"

        if os.path.exists(save_file):
            with open(save_file, "r") as f:
                data = json.load(f)
        else:
            data = {}

        if self.player_name not in data:
            data[self.player_name] = []

        data[self.player_name].append({
            "name": pokemon.name,
            "atributos": pokemon.atributos
        })

        with open(save_file, "w") as f:
            json.dump(data, f, indent=4)

    def draw_ui(self, message, pokemon):
        font = pygame.font.SysFont(None, 24)

        # Mensagem inferior
        if message:
            text = font.render(message, True, (0, 0, 0))
            self.screen.blit(text, (10, HEIGHT - 30))

        # Exibir atributos do Pokémon encontrado
        if pokemon:
            attr_y = HEIGHT - 100
            for attr, val in pokemon.atributos.items():
                attr_text = font.render(f"{attr}: {val}", True, (0, 0, 0))
                self.screen.blit(attr_text, (10, attr_y))
                attr_y += 20

        # Contador de capturas
        count_text = font.render(f"Capturados: {self.captured_count}", True, (0, 0, 0))
        self.screen.blit(count_text, (WIDTH - 180, 10))

        # Lista dos últimos capturados
        y_offset = 35
        for i, name in enumerate(self.last_captured):
            captured_text = font.render(f"- {name}", True, (0, 0, 0))
            self.screen.blit(captured_text, (WIDTH - 180, y_offset + i * 20))

    def change_map(self):
        if self.map.name == "map":
            self.map.load_new_map("map2")
            self.map.name = "map2"
        elif self.map.name == "map2":
            self.map.load_new_map("map")
            self.map.name = "map"
        self.player.set_position(2, 2)
        self.pokemons = self.load_pokemons()
        self.exit = self.map.exit

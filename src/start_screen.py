import pygame

def get_player_name(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    input_box = pygame.Rect(200, 200, 240, 36)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Ativa o input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Desenho da caixa de input
        txt_surface = font.render(text, True, (0, 0, 0))
        width = max(240, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Título
        title = font.render("Digite seu nome e pressione Enter:", True, (0, 0, 0))
        screen.blit(title, (200, 150))

        pygame.display.flip()
        clock.tick(30)

    return text

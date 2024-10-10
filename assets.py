import pygame

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_start_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    draw_text(screen, "Pressione qualquer tecla para começar", font, (255, 255, 255), width // 2, height // 2)
    pygame.display.flip()

def draw_pause_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    draw_text(screen, "Jogo Pausado", font, (255, 255, 255), width // 2, height // 2)
    draw_text(screen, "Pressione P para continuar", font, (255, 255, 255), width // 2, height // 2 + 100)
    pygame.display.flip()

def draw_menu_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    draw_text(screen, "Menu", font, (255, 255, 255), width // 2, height // 2 - 100)
    draw_text(screen, "1. Iniciar Jogo", font, (255, 255, 255), width // 2, height // 2)
    draw_text(screen, "2. Sair", font, (255, 255, 255), width // 2, height // 2 + 100)
    pygame.display.flip()

def draw_victory_screen(screen, width, height):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    draw_text(screen, "Você Venceu!", font, (255, 255, 255), width // 2, height // 2)
    pygame.display.flip()
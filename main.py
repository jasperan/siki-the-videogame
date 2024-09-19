import pygame
import sys
from game_state import GameState
from player import Player
from target import Target

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Siki's Smoking Adventure")

clock = pygame.time.Clock()
game_state = GameState(WIDTH, HEIGHT)

# Load assets
background_img = pygame.image.load("assets/background.jpg").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.set_volume(game_state.volume)
pygame.mixer.music.play(-1)

collect_sound = pygame.mixer.Sound("assets/collect.mp3")
game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state.game_over:
                    game_state.update_high_scores()
                    game_state.reset()
                elif game_state.start_screen:
                    game_state.start_game()
            elif event.key == pygame.K_h and game_state.start_screen:
                game_state.high_score_screen = True
            elif event.key == pygame.K_b and game_state.high_score_screen:
                game_state.high_score_screen = False
            elif event.key == pygame.K_UP and game_state.start_screen:
                game_state.handle_volume(0.1)
            elif event.key == pygame.K_DOWN and game_state.start_screen:
                game_state.handle_volume(-0.1)
            elif game_state.game_over:
                if event.key == pygame.K_BACKSPACE:
                    game_state.player_name = game_state.player_name[:-1]
                elif event.key != pygame.K_RETURN:
                    game_state.player_name += event.unicode

    screen.blit(background_img, (0, 0))

    if game_state.start_screen:
        if game_state.high_score_screen:
            game_state.draw_high_score_screen(screen)
        else:
            game_state.draw_start_screen(screen)
    elif game_state.game_over:
        game_state.draw_game_over(screen)
    else:
        game_state.update()
        if game_state.check_collect():
            collect_sound.play()
        if game_state.check_game_over():
            game_over_sound.play()
        game_state.draw(screen)

    pygame.display.flip()
    clock.tick(60)
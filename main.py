# Example file showing a basic pygame "game loop"
import pygame
import time

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
title = pygame.display.set_caption(title="Des Valamons", icontitle="None")
clock = pygame.time.Clock()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.play()
pygame.font.init()
running = True

screen_type = "home"
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    def is_text_clicked(x, y, text_rect):
        return text_rect.collidepoint(x, y)

    def home_screen() :
        title = pygame.font.SysFont('Arial', 120)
        title_surface = title.render("Des Valamons", False, (128,0,0))
        text = pygame.font.SysFont('Arial', 50)
        text_surface = text.render("-> Jouer Solo", False, (128,0,0))
        text_surface1 = text.render("-> Jouer en Multijoueur", False, (128,0,0))
        text_surface2 = text.render("-> Quitter", False, (128,0,0))
        text_rect = text_surface.get_rect(topleft=(350,325))
        text_rect1 = text_surface1.get_rect(topleft=(350,425))
        text_rect2 = text_surface2.get_rect(topleft=(350,525))
        screen.blit(title_surface, (350, 25))
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if is_text_clicked(mouse_x, mouse_y, text_rect2):
                global running
                running = False
            if is_text_clicked(mouse_x, mouse_y, text_rect):
                print("Passage en mode Solo")
                global screen_type
                screen_type = "solo"
                return

    def solo() :
        pygame.font.init()
        title = pygame.font.SysFont('Arial', 120)
        title_surface = title.render("Pas Dispo", False, (128, 0, 0))
        title_rect = title_surface.get_rect(center=(640,360))
        screen.blit(title_surface, title_rect)
        global screen_type
        screen_type = 'home'
        print("Retour au menu d'acceuil")
        return

    if screen_type == "home" :
        home_screen()
    elif screen_type == 'solo' :
        solo()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

print("Merci d'avoir joué")
pygame.quit()
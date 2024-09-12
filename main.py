# Example file showing a basic pygame "game loop"
import pygame
import time

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
title = pygame.display.set_caption(title="Valamons", icontitle="None")
clock = pygame.time.Clock()
pygame.mixer.music.load('assets/music.mp3')
pygame.mixer.music.play()
pygame.font.init()
running = True
princip_color = (128,0,0)

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
        title_surface = title.render("Valamons", False, princip_color)
        text = pygame.font.SysFont('Arial', 50)
        text_surface = text.render("-> Jouer Solo", False, princip_color)
        text_surface1 = text.render("-> Jouer en Multijoueur", False, princip_color)
        text_surface2 = text.render("-> Crédits", False, princip_color)
        text_surface3 = text.render("-> Quitter", False, princip_color)
        title_rect = title_surface.get_rect(center=(640, 100))
        text_rect = text_surface.get_rect(topleft=(350,325))
        text_rect1 = text_surface1.get_rect(topleft=(350,425))
        text_rect2 = text_surface2.get_rect(topleft=(350,525))
        text_rect3 = text_surface3.get_rect(topleft=(350,625))
        screen.blit(title_surface, title_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if is_text_clicked(mouse_x, mouse_y, text_rect3):
                global running
                running = False
            if is_text_clicked(mouse_x, mouse_y, text_rect):
                print("Passage en mode Solo")
                global screen_type
                screen_type = "solo"
                return
            if is_text_clicked(mouse_x, mouse_y, text_rect2):
                print("Passage sur les crédits")
                screen_type = "credit"
                return

    def solo() :
        pygame.font.init()
        title = pygame.font.SysFont('Arial', 120)
        title_surface = title.render("Pas Dispo", False, princip_color)
        title_rect = title_surface.get_rect(center=(640,360))
        screen.blit(title_surface, title_rect)
        global screen_type
        screen_type = 'home'
        print("Retour au menu d'acceuil")
        return

    def credit() :
        pygame.font.init()
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (50, 50))
        title = pygame.font.SysFont('Arial', 120)
        text = pygame.font.SysFont('Arial', 50)
        copyright = pygame.font.SysFont('Arial', 25)
        title_surface = title.render("Valamons", False, princip_color)
        text_surface = text.render("Designer Graphique : Raphael Robin", False, princip_color)
        text_surface1 = text.render("Développeurs : Lucas De Araujo, Robin Calcar,", False, princip_color)
        text_surface3 = text.render("Raphael Robin et Emma Joulin", False, princip_color)
        text_surface2 = text.render("Directrice de projet : Emma Joulin", False, princip_color)
        copyright_surface = copyright.render("Tous droits réservés © 2024", False, princip_color)
        title_rect = title_surface.get_rect(center=(640, 100))
        text_rect = text_surface.get_rect(center=(640,325))
        text_rect1 = text_surface1.get_rect(center=(640, 425))
        text_rect2 = text_surface2.get_rect(center=(640, 600))
        text_rect3 = text_surface3.get_rect(center=(640, 500))
        home_rect = scaled_image.get_rect(topleft=(12, 12))
        copyright_rect = copyright_surface.get_rect(center=(640, 700))
        screen.blit(title_surface, title_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)
        screen.blit(copyright_surface, copyright_rect)
        screen.blit(scaled_image, home_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if is_text_clicked(mouse_x, mouse_y, home_rect):
                print("Retour à l'écran d'acceuil")
                global screen_type
                screen_type = "home"
                return


    if screen_type == "home" :
        home_screen()
    elif screen_type == 'solo' :
        solo()
    elif screen_type == 'credit' :
        credit()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

print("Merci d'avoir joué")
pygame.quit()
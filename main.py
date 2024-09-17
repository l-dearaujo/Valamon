import pygame
import time
import csv

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN)
title = pygame.display.set_caption(title="Valamons", icontitle="None")
clock = pygame.time.Clock()
pygame.font.init()
running = True
princip_color = (128,0,0)
startscreen = True

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


    def read_csv_to_list(filename):
        data_list = []
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for lines in reader:
                data_list.append(lines)
        return data_list

    def home_screen() :
        title = pygame.font.SysFont('Arial', 240)
        title_surface = title.render("Valamons", False, princip_color)
        text = pygame.font.SysFont('Arial', 100)
        text_surface = text.render("-> Jouer Solo", False, princip_color)
        text_surface1 = text.render("-> Jouer en Multijoueur", False, princip_color)
        text_surface2 = text.render("-> Crédits", False, princip_color)
        text_surface3 = text.render("-> Quitter", False, princip_color)
        title_rect = title_surface.get_rect(center=(960, 100))
        text_rect = text_surface.get_rect(topleft=(670,435))
        text_rect1 = text_surface1.get_rect(topleft=(670,585))
        text_rect2 = text_surface2.get_rect(topleft=(670,735))
        text_rect3 = text_surface3.get_rect(topleft=(670,885))
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
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (50, 50))
        home_rect = scaled_image.get_rect(topleft=(12, 12))
        fond = pygame.image.load('assets/fond.png')
        fond = pygame.transform.scale(fond, (1920, 1080))
        screen.blit(fond, (0, 0))
        screen.blit(scaled_image, home_rect)
        global startscreen
        if startscreen == True :
            pygame.font.init()
            start=pygame.font.SysFont('Arial',240)
            start_surface=start.render("Start !", False, (255,255,255))
            start_rect=start_surface.get_rect(center=(960,885))
            screen.blit(start_surface, start_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if is_text_clicked(mouse_x, mouse_y, start_rect):
                    startscreen = False
        if startscreen == False :
            data_list = read_csv_to_list('assets/valamons.csv')
            print(data_list)
            class Valamons :
                def __init__(self,nom,pv,atk1,titreatk1,atk2,titreatk2,elt,soin1,soin2):
                    self.nom = nom
                    self.pv = pv
                    self.atk1 = atk1
                    self.titre1 = titreatk1
                    self.atk2 = atk2
                    self.titre2 = titreatk2
                    self.elt = elt
                    self.__soin1 = soin1
                    self.__soin2 = soin2

                def attaque(self,nom1, nom2, atk):
                    if atk == self.titre1 :
                        nom2.pv -= self.atk1
                        nom1.pv += self.__soin1
                    else:
                        nom2.pv -= self.atk2
                        nom1.pv += self.__soin2
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if is_text_clicked(mouse_x, mouse_y, home_rect):
                global screen_type
                screen_type = 'home'
                startscreen = True

    def credit() :
        pygame.font.init()
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (50, 50))
        title = pygame.font.SysFont('Arial', 240)
        text = pygame.font.SysFont('Arial', 100)
        copyright = pygame.font.SysFont('Arial', 50)
        title_surface = title.render("Valamons", False, princip_color)
        text_surface = text.render("Designer Graphique : Raphael Robin", False, princip_color)
        text_surface1 = text.render("Développeurs : Lucas De Araujo, Robin Calcar,", False, princip_color)
        text_surface3 = text.render("Raphael Robin et Emma Joulin", False, princip_color)
        text_surface2 = text.render("Directrice de projet : Emma Joulin", False, princip_color)
        copyright_surface = copyright.render("Tous droits réservés © 2024", False, princip_color)
        title_rect = title_surface.get_rect(center=(960, 100))
        text_rect = text_surface.get_rect(center=(960,435))
        text_rect1 = text_surface1.get_rect(center=(960, 585))
        text_rect2 = text_surface2.get_rect(center=(960, 885))
        text_rect3 = text_surface3.get_rect(center=(960, 735))
        home_rect = scaled_image.get_rect(topleft=(12, 12))
        copyright_rect = copyright_surface.get_rect(center=(960, 1000))
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
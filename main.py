import pygame
import csv
import random
import webbrowser

from pygame.display import toggle_fullscreen

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1728, 972), pygame.SCALED)
title = pygame.display.set_caption(title="Valamons", icontitle="None")
clock = pygame.time.Clock()
pygame.font.init()
running = True
princip_color = (255,255,255)
startscreen = True
screen_type = "home"
pos_emplacement1 = [[[602,506],[732,506],[862,506],[992,506],[1122,506]],[[602,672],[732,672],[862,672],[992,672],[1122,672]]]
pos_emplacement2 = [[[602,130],[732,130],[862,130],[992,130],[1122,130]],[[602,296],[732,296],[862,296],[992,296],[1122,296]]]
carte_rects_j1 = []
carte_rects_j2 = []
ordre_elt1 = ["Plante","Eau","Feu"]
ordre_elt2 = ["Bonbons","Robots","Lumière"]
pos_carte_selec = None
prop_screen = False
quit = False

def is_text_clicked(x, y, text_rect):
    return text_rect.collidepoint(x, y)


def read_csv_to_list(filename):
    liste = []
    with open(filename, mode='r', newline='', encoding='ansi') as file:
        reader = csv.reader(file, delimiter=';')
        for lines in reader:
            liste.append(lines)
    return liste

def pos_cartes():
    m = [["","","","","",""],["","","","","",""]]
    compteur_x = 0
    while compteur_x<7:
        lig = random.randint(0,1)
        col = random.randint(0,4)
        if m[lig][col]!= "X":
            m[lig][col] = "X"
            compteur_x+=1
    return m

class Valamons:
    def __init__(self, nom, pv, pvmax, atk1, atk2, soin1, soin2, soincol1, soincol2, elt1, elt2, titreatk1, titreatk2):
        self.nom = nom
        self.pv = pv
        self.__pvmax = pvmax
        self.atk1 = atk1
        self.titre1 = titreatk1
        self.atk2 = atk2
        self.titre2 = titreatk2
        self.elt1 = elt1
        self.elt2 = elt2
        self.soin1 = soin1
        self.soin2 = soin2
        self.__soincol1 = soincol1
        self.__soincol2 = soincol2

    def __sub__(self, valeur):
        self.pv -= valeur

    def get_pvmax(self):
        return self.__pvmax

    def attaque1(self, vala, player):
        vala - self.atk1
        if self.__soincol1 == 0:
            if not self.pv + self.soin1 > self.__pvmax:
                self.pv += self.soin1
        else:
            for i in range(len(player.liste)):
                if player.liste[i].pv + self.soin1 <= player.liste[i].get_pvmax():
                    player.liste[i].pv += self.soin1

    def attaque2(self, vala, player):
        vala - self.atk2
        if self.__soincol2 == 0:
            if not self.pv + self.soin2 > self.__pvmax:
                self.pv += self.soin2
        else:
            for i in range(len(player.liste)):
                if player.liste[i].pv + self.soin2 <= player.liste[i].get_pvmax():
                    player.liste[i].pv += self.soin2

    """def elt_check(self,vala):
        global ordre_elt1
        for i in range(2):
            if """


class Joueur :
    def __init__(self):
        self.liste = []
        for i in range(8):
            ran = random.randint(0, 20)
            self.liste.append(valamonslist[ran])
    def possecarte(self, vala, position):
        valaimage = pygame.image.load(f'assets/{vala}.png')
        screen.blit(valaimage, position)


valamons = read_csv_to_list('assets/valamons.csv')
valamonsl = [element for element in valamons]
valamonslist = []

for i in range(len(valamonsl)):
    valamonsl[i][0] = valamonsl[i][0].strip('"')
    valamonsl[i][0] = Valamons(valamonsl[i][0], int(valamonsl[i][1]), int(valamonsl[i][2]), int(valamonsl[i][3]),
                               int(valamonsl[i][4]), int(valamonsl[i][5]), int(valamonsl[i][6]), int(valamonsl[i][7]),
                               int(valamonsl[i][8]), valamonsl[i][9], valamonsl[i][10], valamonsl[i][11], valamonsl[i][12])
    valamonslist.append(valamonsl[i][0])

J1 = Joueur()
BOT = Joueur()
plateauJ1 = pos_cartes()
plateauBOT = pos_cartes()

def init_pos():
    global carte_rects_j1
    global carte_rects_j2
    for i in range(len(J1.liste)):
        placed = False
        for a in range(2):
            if placed :
                break
            for b in range(5):
                if plateauJ1[a][b] == "X" and not placed:
                    carte = pygame.image.load(f'assets/carte_{J1.liste[i].nom}.png')
                    pos_a = pos_emplacement1[a][b][0]
                    pos_b = pos_emplacement1[a][b][1]
                    carte_rect = carte.get_rect(center=(pos_a, pos_b))
                    carte_rects_j1.append([carte_rect, pos_a, pos_b, i, a, b])
                    plateauJ1[a][b]="Y"
                    placed = True
    for i in range(len(BOT.liste)):
        placed = False
        for a in range(2):
            if placed :
                break
            for b in range(5):
                if plateauBOT[a][b] == "X" and not placed:
                    carte = pygame.image.load(f'assets/carte_{BOT.liste[i].nom}.png')
                    pos_a = pos_emplacement2[a][b][0]
                    pos_b = pos_emplacement2[a][b][1]
                    carte_rect = carte.get_rect(center=(pos_a, pos_b))
                    carte_rects_j2.append([carte_rect, pos_a, pos_b, i, a, b])
                    plateauBOT[a][b]="Y"
                    placed = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    def home_screen() :
        global pos_carte_selec
        global quit
        titre = pygame.font.SysFont('Arial', 150)
        titre_surface = titre.render("Valamons", False, princip_color)
        text = pygame.font.SysFont('Arial', 75)
        text_surface = text.render("-> Jouer Solo", False, princip_color)
        text_surface1 = text.render("-> Règles du jeu", False, princip_color)
        text_surface2 = text.render("-> Crédits", False, princip_color)
        text_surface3 = text.render("-> Quitter", False, princip_color)
        fond = pygame.image.load('assets/home_screen.png')
        fond_scaled = pygame.transform.scale(fond, (1728, 972))
        screen.blit(fond_scaled, (0, 0))
        voile = pygame.Surface((1728, 972))
        voile.set_alpha(70)
        voile.fill((0, 0, 0))
        screen.blit(voile, (0, 0))
        titre_rect = titre_surface.get_rect(center=(860, 100))
        text_rect = text_surface.get_rect(topleft=(570,325))
        text_rect1 = text_surface1.get_rect(topleft=(570,450))
        text_rect2 = text_surface2.get_rect(topleft=(570,575))
        text_rect3 = text_surface3.get_rect(topleft=(570,700))
        screen.blit(titre_surface, titre_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)
        if quit :
            voile = pygame.Surface((600, 300))
            voile.set_alpha(200)
            voile.fill((0, 0, 0))
            voile_rect = voile.get_rect(center=(864, 450))
            screen.blit(voile, voile_rect.topleft)
            quit_surface = pygame.image.load('assets/bob.png')
            quit_scaled = pygame.transform.scale(quit_surface, (304, 179))
            quit_rect = quit_scaled.get_rect(center=(864,386))
            screen.blit(quit_scaled,quit_rect)
            titre = pygame.font.SysFont('Arial', 50)
            titre_surface = titre.render("Es-tu sûr de vouloir quitter ?", False, princip_color)
            text = pygame.font.SysFont('Arial', 25)
            text_surface = text.render("Oui", False, princip_color)
            text_surface1 = text.render("Non", False, princip_color)
            titre_rect = titre_surface.get_rect(center=(860, 525))
            text_rect = text_surface.get_rect(topleft=(770,555))
            text_rect1 = text_surface1.get_rect(topleft=(870,555))
            screen.blit(titre_surface, titre_rect)
            screen.blit(text_surface, text_rect)
            screen.blit(text_surface1, text_rect1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if is_text_clicked(mouse_x, mouse_y, text_rect1):
                        quit = False
                    if is_text_clicked(mouse_x, mouse_y, text_rect):
                        global running
                        running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not quit:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if is_text_clicked(mouse_x, mouse_y, text_rect3):
                    quit = True
                if is_text_clicked(mouse_x, mouse_y, text_rect):
                    print("Passage en mode Solo")
                    global screen_type
                    screen_type = "solo"
                    init_pos()
                    return
                if is_text_clicked(mouse_x, mouse_y, text_rect2):
                    print("Passage sur les crédits")
                    screen_type = "credit"
                    return
                if is_text_clicked(mouse_x,mouse_y,text_rect1):
                    webbrowser.open('https://github.com/Energielulu83852/Valamons/wiki/Rules')

    def solo() :
        global carte_rects_j1
        global carte_rects_j2
        global pos_carte_selec
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (35, 35))
        home_rect = scaled_image.get_rect(topleft=(10, 10))
        fond = pygame.image.load('assets/plateau.png')
        screen.blit(fond, (0, 0))
        screen.blit(scaled_image, home_rect)
        global startscreen
        global prop_screen
        if startscreen == True :
            voile = pygame.Surface((1728, 972))
            voile.set_alpha(128)
            voile.fill((0, 0, 0))
            screen.blit(voile, (0, 0))
            pygame.font.init()
            start=pygame.font.SysFont('Arial',125)
            start_surface=start.render("Start !", False, (255,255,255))
            start_rect=start_surface.get_rect(center=(860,872))
            screen.blit(start_surface, start_rect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if is_text_clicked(mouse_x, mouse_y, start_rect):
                    startscreen = False
        elif startscreen == False :
            for carte_rect, pos_a, pos_b, i, a, b in carte_rects_j1:
                carte = pygame.image.load(f'assets/carte_{J1.liste[i].nom}.png')
                pv = J1.liste[i].pv
                img_pv = pygame.image.load(f'assets/chiffre_{pv}.png')
                img_pv_rect = img_pv.get_rect(center=(pos_a+20, pos_b+55))
                screen.blit(carte, carte_rect)
                screen.blit(img_pv, img_pv_rect)
            for carte_rect, pos_a, pos_b, i, a, b in carte_rects_j2:
                carte = pygame.image.load(f'assets/carte_{BOT.liste[i].nom}.png')
                pv = BOT.liste[i].pv
                img_pv = pygame.image.load(f'assets/chiffre_{pv}.png')
                img_pv_rect = img_pv.get_rect(center=(pos_a+20, pos_b+55))
                screen.blit(carte, carte_rect)
                screen.blit(img_pv, img_pv_rect)

            if pos_carte_selec != None:
                pygame.font.init()
                text = pygame.font.SysFont('Arial', 30)
                text_surface = text.render("Propriété de la carte", False, princip_color)
                text_surface2 = text.render("Attaque 1", False, princip_color)
                text_surface3 = text.render("Attaque 2", False, princip_color)
                posi_a = pos_carte_selec[0]
                posi_b = pos_carte_selec[1]
                text_rect = text_surface.get_rect(center=(401, 525))
                text_rect2 = text_surface2.get_rect(center=(401, 570))
                text_rect3 = text_surface3.get_rect(center=(401, 620))
                background_color = (128, 128, 128)
                voile = pygame.Surface((125, 165))
                voile.set_alpha(64)
                voile.fill((255, 255, 153))
                screen.blit(voile, (posi_a-65, posi_b-80))
                pygame.draw.rect(screen, background_color, text_rect)
                pygame.draw.rect(screen, background_color, text_rect2)
                pygame.draw.rect(screen, background_color, text_rect3)
                screen.blit(text_surface, text_rect)
                screen.blit(text_surface2, text_rect2)
                screen.blit(text_surface3, text_rect3)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if is_text_clicked(mouse_x, mouse_y, text_rect):
                            prop_screen = True
                        if is_text_clicked(mouse_x, mouse_y, text_rect2):
                            if plateauBOT[0][pos_carte_selec[4]] == 'Y':
                                for el in carte_rects_j2:
                                    if el[4] == 0 and el[5] == pos_carte_selec[4]:
                                        cartead = el[3]
                                        J1.liste[i].attaque1(BOT.liste[cartead], J1)
                            elif plateauBOT[1][pos_carte_selec[4]] == 'Y':
                                for el in carte_rects_j2:
                                    if el[4] == 1 and el[5] == pos_carte_selec[4]:
                                        cartead = el[3]
                                        J1.liste[i].attaque1(BOT.liste[cartead], J1)
                        if is_text_clicked(mouse_x, mouse_y, text_rect3):
                            if plateauBOT[0][pos_carte_selec[4]] == 'Y':
                                for el in carte_rects_j2:
                                    if el[4] == 0 and el[5] == pos_carte_selec[4]:
                                        cartead = el[3]
                                        J1.liste[i].attaque2(BOT.liste[cartead], J1)
                            elif plateauBOT[1][pos_carte_selec[4]] == 'Y':
                                for el in carte_rects_j2:
                                    if el[4] == 1 and el[5] == pos_carte_selec[4]:
                                        cartead = el[3]
                                        J1.liste[i].attaque2(BOT.liste[cartead], J1)
            if prop_screen == True:
                voile = pygame.Surface((1728, 972))
                voile.set_alpha(128)
                voile.fill((0, 0, 0))
                screen.blit(voile, (0, 0))
                xmark = pygame.image.load('assets/xmark-solid.svg')
                scaled_image = pygame.transform.scale(xmark, (35, 45))
                xmark_rect = scaled_image.get_rect(topleft=(1680, 10))
                screen.blit(scaled_image, xmark_rect)
                text = pygame.font.SysFont('Arial', 90)
                titre = pygame.font.SysFont('Arial', 125)
                titre_surface = titre.render(f"{J1.liste[pos_carte_selec[2]].nom}", False, (255, 255, 255))
                text_surface5 = text.render(f"Élément 1 : {J1.liste[pos_carte_selec[2]].elt1}", False, (255, 255, 255))
                elt2 = J1.liste[pos_carte_selec[2]].elt2
                if elt2 == 'None':
                    text_surface6 = text.render(f"Élément 2 : Aucun", False, (255, 255, 255))
                else:
                    text_surface6 = text.render(f"Élément 2 : {J1.liste[pos_carte_selec[2]].elt2}", False,(255, 255, 255))
                text_surface = text.render(f"Attaque 1 : {J1.liste[pos_carte_selec[2]].titre1}", False, (255, 255, 255))
                text_surface2 = text.render(f"PV d'attaque 1 : {J1.liste[pos_carte_selec[2]].atk1} (Soin : {J1.liste[pos_carte_selec[2]].soin1})", False, (255, 255, 255))
                text_surface3 = text.render(f"Attaque 2 : {J1.liste[pos_carte_selec[2]].titre2}", False, (255, 255, 255))
                text_surface4 = text.render(f"PV d'attaque 2 : {J1.liste[pos_carte_selec[2]].atk2} (Soin : {J1.liste[pos_carte_selec[2]].soin2})", False, (255, 255, 255))
                titre_rect=titre_surface.get_rect(center=(860,100))
                screen.blit(titre_surface, titre_rect)
                text_rect2=text_surface2.get_rect(center=(860,565))
                screen.blit(text_surface2, text_rect2)
                text_rect=text_surface.get_rect(center=(860,445))
                screen.blit(text_surface, text_rect)
                text_rect3=text_surface3.get_rect(center=(860,685))
                screen.blit(text_surface3, text_rect3)
                text_rect4=text_surface4.get_rect(center=(860,805))
                screen.blit(text_surface4, text_rect4)
                text_rect6=text_surface6.get_rect(center=(860,325))
                screen.blit(text_surface6, text_rect6)
                text_rect5=text_surface5.get_rect(center=(860,225))
                screen.blit(text_surface5, text_rect5)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if is_text_clicked(mouse_x, mouse_y, xmark_rect):
                            prop_screen = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for carte_rect, posa, posb, i, a, b in carte_rects_j1:
                        if carte_rect.collidepoint(mouse_x, mouse_y):
                            pos_carte_selec = [posa,posb,i, a, b]
                            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if is_text_clicked(mouse_x, mouse_y, home_rect):
                    global screen_type
                    screen_type = 'home'
                    startscreen = True

    def credit() :
        pygame.font.init()
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (25, 25))
        titre = pygame.font.SysFont('Arial', 150)
        text = pygame.font.SysFont('Arial', 75)
        copyrights = pygame.font.SysFont('Arial', 50)
        titre_surface = titre.render("Valamons", False, princip_color)
        text_surface = text.render("Designer Graphique : Raphael Robin", False, princip_color)
        text_surface1 = text.render("Développeurs : Lucas De Araujo, Robin Calcar,", False, princip_color)
        text_surface3 = text.render("Raphael Robin et Emma Joulin", False, princip_color)
        text_surface2 = text.render("Directrice de projet : Emma Joulin", False, princip_color)
        copyrights_surface = copyrights.render("Tous droits réservés © 2024", False, princip_color)
        titre_rect = titre_surface.get_rect(center=(860, 100))
        text_rect = text_surface.get_rect(center=(860,325))
        text_rect1 = text_surface1.get_rect(center=(860, 450))
        text_rect2 = text_surface2.get_rect(center=(860, 700))
        text_rect3 = text_surface3.get_rect(center=(860, 575))
        home_rect = scaled_image.get_rect(topleft=(10, 10))
        copyrights_rect = copyrights_surface.get_rect(center=(860, 900))
        fond = pygame.image.load('assets/credit_screen.png')
        fond_scaled = pygame.transform.scale(fond, (1728, 972))
        screen.blit(fond_scaled, (0, 0))
        voile = pygame.Surface((1728, 972))
        voile.set_alpha(70)
        voile.fill((0, 0, 0))
        screen.blit(voile, (0, 0))
        screen.blit(titre_surface, titre_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface3, text_rect3)
        screen.blit(copyrights_surface, copyrights_rect)
        screen.blit(scaled_image, home_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
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

    #clock.tick(60)  # limits FPS to 60

print("Merci d'avoir joué")
pygame.quit()
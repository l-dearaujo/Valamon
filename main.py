import pygame
import csv
import random
import webbrowser

from pygame.display import toggle_fullscreen

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1728, 972), pygame.SCALED)
title = pygame.display.set_caption(title="Valamon", icontitle="None")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.font.init()
running = True
princip_color = (255,255,255)
startscreen = True
screen_type = "home"
pos_emplacement1 = [[[602,506],[732,506],[862,506],[992,506],[1122,506]],[[602,672],[732,672],[862,672],[992,672],[1122,672]]]
pos_emplacement2 = [[[602,130],[732,130],[862,130],[992,130],[1122,130]],[[602,296],[732,296],[862,296],[992,296],[1122,296]]]
carte_rects_j1, carte_rects_j2, cartes_joues = [],[],[]
ordre_elt = {"Plante":"Eau","Eau":"Feu","Feu":"Plante","Bonbons":"Robot","Robot":"Lumiere","Lumiere":"Bonbons",'Vide':'Vide'}
pos_carte_selec = None
prop_screen, quit, tour_end, over_screen, win_screen, diag,atk_selec = False, False, False, False, False,False,None
attaquebot, bot_atk = 0,0


pygame.mixer.init()
musique_par_page = {
    "home": "assets/acceuil.mp3",
    "solo": "assets/combat.mp3"
}

def jouer_musique(page, musique_actuelle):
    if page in musique_par_page:
        if musique_par_page[page] != musique_actuelle:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(musique_par_page[page])
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
            return musique_par_page[page]
    else:
        pygame.mixer.music.stop()
        return None
    return musique_actuelle

musique_actuelle = None

def init_pos():
    global carte_rects_j2, carte_rects_j1, plateauBOT, pos_emplacement2, carte_rect_liste
    cont = False
    for i in range(len(carte_rect_liste)):
        if J1.liste[carte_rect_liste[i][1]].plc <= J1.plc:
            cont = True
    if cont == True:
        for i in range(len(BOT.liste_pasplac)):
            placed = False
            if len(carte_rects_j2) > len(carte_rects_j1) :
                return
            for a in range(2):
                if placed :
                    break
                for b in range(5):
                    if plateauBOT[a][b] == "X" and not placed:
                        carte = pygame.image.load(f'assets/carte_{BOT.liste_pasplac[0].nom}.png')
                        pos_a = pos_emplacement2[a][b][0]
                        pos_b = pos_emplacement2[a][b][1]
                        carte_rect = carte.get_rect(center=(pos_a, pos_b))
                        for c in range(len(BOT.liste)):
                            if BOT.liste[c] == BOT.liste_pasplac[0]:
                                carte_rects_j2.append([carte_rect, pos_a, pos_b, c, a, b])
                        plateauBOT[a][b]="Y"
                        BOT.liste_pasplac.pop(0)
                        placed = True
                    else :
                        a = random.randint(0,1)
                        b = random.randint(0,4)
                        if plateauBOT[a][b] == "" and not placed:
                            carte = pygame.image.load(f'assets/carte_{BOT.liste_pasplac[0].nom}.png')
                            pos_a = pos_emplacement2[a][b][0]
                            pos_b = pos_emplacement2[a][b][1]
                            carte_rect = carte.get_rect(center=(pos_a, pos_b))
                            for c in range(len(BOT.liste)):
                                if BOT.liste[c] == BOT.liste_pasplac[0]:
                                    carte_rects_j2.append([carte_rect, pos_a, pos_b, c, a, b])
                            plateauBOT[a][b] = "Y"
                            BOT.liste_pasplac.pop(0)
                            placed = True


#--------------------------------
# Partie de Raphaël
#--------------------------------

white = (255, 255, 255)
SCREEN_WIDTH = 1728
SCREEN_HEIGHT = 972
card_image = pygame.image.load("assets/carte_Bob.png")
card_width, card_height = card_image.get_size()
carte_rect_liste = []
cases_rect_liste = []
cartes_differences_liste = []

button_clicked = False
num_cards = 4
selection_carte = "pas_de_selection"

width, height = 1728, 972
carte_rect = card_image.get_rect()

def display_cards(surface, num_cards):
    if num_cards > 0 :
        x_offset = 200/(2.5*num_cards)
        y_pos = SCREEN_HEIGHT - card_height - 20
        total_cards_width = num_cards * card_width + (num_cards - 1) * x_offset
        x_start = (SCREEN_WIDTH - total_cards_width) // 2

    for i in range(num_cards):
        x_pos = x_start + i * (card_width + x_offset)
        valaimage = pygame.image.load(f'assets/carte_{J1.liste[carte_rect_liste[i][1]].nom}.png')
        surface.blit(valaimage, (x_pos, y_pos))
        carte_rect_liste[i][0].x = x_pos
        carte_rect_liste[i][0].y = y_pos
        plc = J1.liste[carte_rect_liste[i][1]].plc
        img_plc = pygame.image.load(f'assets/chiffre_{plc}.png')
        img_plc_rect = img_plc.get_rect(center=(x_pos+102.5, y_pos+23))
        screen.blit(img_plc, img_plc_rect)
        pv = J1.liste[carte_rect_liste[i][1]].pv
        img_pv = pygame.image.load(f'assets/chiffre_{pv}.png')
        img_pv_rect = img_pv.get_rect(center=(x_pos+80, y_pos+135))
        screen.blit(img_pv, img_pv_rect)
        if J1.liste[carte_rect_liste[i][1]].plc > J1.plc:
            voile = pygame.Surface((125, 165))
            voile.set_alpha(128)
            voile.fill((255, 0, 0))
            screen.blit(voile, (x_pos-5, y_pos))

def poser_carte(selection_carteeee, num_emplacement_case) :
    a = num_emplacement_case // 5
    b = num_emplacement_case % 5
    if selection_carte is not None:
        for i in range(len(cases_rect_liste)) :
            if cases_rect_liste[i].collidepoint(event.pos) and plateauJ1[a][b] == "":
                carte = pygame.image.load(f'assets/carte_{J1.liste[selection_carteeee].nom}.png') #
                pos_a = pos_emplacement1[a][b][0]
                pos_b = pos_emplacement1[a][b][1]
                carte_rect = carte.get_rect(center=(pos_a, pos_b))
                carte_rects_j1.append([carte_rect, pos_a, pos_b, selection_carteeee,a,b])
                plateauJ1[a][b] = "Y"
                J1.plc-=J1.liste[selection_carteeee].plc

#--------------------------------
# Fin de la partie
#--------------------------------

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
    while compteur_x<4:
        lig = random.randint(0,1)
        col = random.randint(0,4)
        if m[lig][col]!= "X":
            m[lig][col] = "X"
            compteur_x+=1
    return m

class Valamon:
    def __init__(self, nom, pv, pvmax, atk1, atk2, soin1, soin2, soincol1, soincol2, elt1, elt2, titreatk1, titreatk2,plc,diag):
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
        self.soincol1 = soincol1
        self.soincol2 = soincol2
        self.plc = plc
        self.diag = diag

    def __sub__(self, valeur):
        self.pv = max(0, self.pv - valeur)

    def get_pvmax(self):
        return self.__pvmax
    def get_pv(self):
        return self.pv

    def elt_check(self,vala,atk):
        global ordre_elt
        if atk == 1 :
            if ordre_elt[self.elt1] == vala.elt1:
                return 2
            else:
                return 0
        else:
            if self.elt2 != 'Vide' and vala.elt2 != 'Vide':
                if ordre_elt[self.elt2] == vala.elt2:
                    return 2
                else:
                    return 0
            else:
                return 0

    def attaque1(self, vala, player, player2, pos, pos_a, pos_b,pos_carte):
        global pos_emplacement1, pos_emplacement2
        ran = random.randint(1,4)
        pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(1.0)
        sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
        sound.play()
        if player2 == BOT:
            effet_attaque = pygame.image.load(f'assets/degat_{self.elt1}.png')
            effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement2[pos_a][pos_b][0]-85, pos_emplacement2[pos_a][pos_b][1]-110))
            screen.blit(effet_attaque, effet_attaque_rect.topleft)
        else:
            effet_attaque = pygame.image.load(f'assets/degat_{self.elt1}.png')
            effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement1[pos_a][pos_b][0]-85, pos_emplacement1[pos_a][pos_b][1]-110))
            screen.blit(effet_attaque, effet_attaque_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(1000)
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.unpause()
        a = self.elt_check(vala,1)
        vala - (self.atk1 + a)
        if self.soincol1 == 0:
            if not self.pv + self.soin1 > self.__pvmax:
                self.pv += self.soin1
                if self.soin1 != 0:
                    pygame.mixer.music.pause()
                    pygame.mixer.music.set_volume(1.0)
                    sound = pygame.mixer.Sound(f'assets/heal_effect.mp3')
                    sound.play()
                    if player == BOT:
                        effet_attaque = pygame.image.load(f'assets/heal.png')
                        effet_attaque_rect = effet_attaque.get_rect(
                            topleft=(
                            pos_emplacement2[pos_a][pos_b][0] - 85, pos_emplacement2[pos_a][pos_b][1] - 110))
                        screen.blit(effet_attaque, effet_attaque_rect.topleft)
                    else:
                        effet_attaque = pygame.image.load(f'assets/heal.png')
                        effet_attaque_rect = effet_attaque.get_rect(
                            topleft=(
                            pos_emplacement1[pos_a][pos_b][0] - 85, pos_emplacement1[pos_a][pos_b][1] - 110))
                        screen.blit(effet_attaque, effet_attaque_rect.topleft)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.unpause()
        else:
            for i in range(len(player.liste)):
                if player.liste[i].pv + self.soincol1 <= player.liste[i].get_pvmax():
                    player.liste[i].pv += self.soincol1
                    if self.soincol1 != 0:
                        pygame.mixer.music.pause()
                        pygame.mixer.music.set_volume(1.0)
                        sound = pygame.mixer.Sound(f'assets/heal_effect.mp3')
                        sound.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.unpause()
        if vala.get_pv() <= 0:
            if player2.nom == "BOT":
                carte_rects_j2.pop(pos_carte)
                plateauBOT[pos_a][pos_b] = ''
            else :
                carte_rects_j1.pop(pos_carte)
                plateauJ1[pos_a][pos_b] = ''
        global pos_carte_selec,prop_screen,diag
        pos_carte_selec=None
        prop_screen = False
        diag = False


    def attaque2(self, vala, player, player2, pos, pos_a, pos_b,pos_carte):
        ran = random.randint(1,4)
        pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(1.0)
        sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
        sound.play()
        if not self.elt2 == 'Vide':
            if player2 == BOT:
                effet_attaque = pygame.image.load(f'assets/degat_{self.elt2}.png')
                effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement2[pos_a][pos_b][0]-85, pos_emplacement2[pos_a][pos_b][1]-110))
                screen.blit(effet_attaque, effet_attaque_rect.topleft)
            else:
                effet_attaque = pygame.image.load(f'assets/degat_{self.elt2}.png')
                effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement1[pos_a][pos_b][0]-85, pos_emplacement1[pos_a][pos_b][1]-110))
                screen.blit(effet_attaque, effet_attaque_rect.topleft)
        else:
            if player2 == BOT:
                effet_attaque = pygame.image.load(f'assets/degat_{self.elt1}.png')
                effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement2[pos_a][pos_b][0]-85, pos_emplacement2[pos_a][pos_b][1]-110))
                screen.blit(effet_attaque, effet_attaque_rect.topleft)
            else:
                effet_attaque = pygame.image.load(f'assets/degat_{self.elt1}.png')
                effet_attaque_rect = effet_attaque.get_rect(topleft=(pos_emplacement1[pos_a][pos_b][0]-85, pos_emplacement1[pos_a][pos_b][1]-110))
                screen.blit(effet_attaque, effet_attaque_rect.topleft)
        pygame.display.flip()
        pygame.time.wait(1000)
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.set_volume(0.3)
        pygame.time.wait(500)
        pygame.mixer.music.unpause()
        a = self.elt_check(vala,2)
        vala - (self.atk2 + a)
        if self.soincol2 == 0:
            if not self.pv + self.soin2 > self.__pvmax:
                self.pv += self.soin2
                if self.soin2 != 0:
                    pygame.mixer.music.pause()
                    pygame.mixer.music.set_volume(1.0)
                    sound = pygame.mixer.Sound(f'assets/heal_effect.mp3')
                    sound.play()
                    if player == BOT:
                        effet_attaque = pygame.image.load(f'assets/heal.png')
                        effet_attaque_rect = effet_attaque.get_rect(
                            topleft=(pos_emplacement2[pos_a][pos_b][0] - 85, pos_emplacement2[pos_a][pos_b][1] - 110))
                        screen.blit(effet_attaque, effet_attaque_rect.topleft)
                    else:
                        effet_attaque = pygame.image.load(f'assets/heal.png')
                        effet_attaque_rect = effet_attaque.get_rect(
                            topleft=(pos_emplacement1[pos_a][pos_b][0] - 85, pos_emplacement1[pos_a][pos_b][1] - 110))
                        screen.blit(effet_attaque, effet_attaque_rect.topleft)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.unpause()
        else:
            for i in range(len(player.liste)):
                if player.liste[i].pv + self.soincol2 <= player.liste[i].get_pvmax():
                    player.liste[i].pv += self.soincol2
                    if self.soincol2 != 0:
                        pygame.mixer.music.pause()
                        pygame.mixer.music.set_volume(1.0)
                        sound = pygame.mixer.Sound(f'assets/heal_effect.mp3')
                        sound.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.wait(100)
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.unpause()
        if vala.get_pv() <= 0:
            if player2.nom == "BOT":
                carte_rects_j2.pop(pos_carte)
                plateauBOT[pos_a][pos_b] = ''
            else:
                carte_rects_j1.pop(pos_carte)
                plateauJ1[pos_a][pos_b] = ''
        global pos_carte_selec,prop_screen,diag
        pos_carte_selec=None
        prop_screen = False
        diag = False



class Joueur :
    def __init__(self,nom):
        self.liste = []
        self.nom = nom
        self.pv = 30
        self.plc = 4
        while len(self.liste) != 4:
            ran = random.randint(0, len(valamonl)-1)
            nouveau_valamon = Valamon(valamonl[ran][0], int(valamonl[ran][1]), int(valamonl[ran][2]), int(valamonl[ran][3]),
                                     int(valamonl[ran][4]), int(valamonl[ran][5]), int(valamonl[ran][6]), int(valamonl[ran][7]),
                                     int(valamonl[ran][8]), valamonl[ran][9], valamonl[ran][10], valamonl[ran][11],
                                     valamonl[ran][12], int(valamonl[ran][13]), int(valamonl[ran][14]))
            self.liste.append(nouveau_valamon)


class Bot:
    def __init__(self,nom):
        self.liste = []
        self.nom = nom
        self.pv = 30
        self.liste_pasplac = []
        while len(self.liste) != 4:
            ran = random.randint(0, len(valamonl)-1)
            nouveau_valamon = Valamon(valamonl[ran][0], int(valamonl[ran][1]), int(valamonl[ran][2]),
                                       int(valamonl[ran][3]),
                                       int(valamonl[ran][4]), int(valamonl[ran][5]), int(valamonl[ran][6]),
                                       int(valamonl[ran][7]),
                                       int(valamonl[ran][8]), valamonl[ran][9], valamonl[ran][10], valamonl[ran][11],
                                       valamonl[ran][12], int(valamonl[ran][13]), int(valamonl[ran][14]))
            self.liste.append(nouveau_valamon)
            self.liste_pasplac.append(nouveau_valamon)

valamon = read_csv_to_list('assets/valamon.csv')
valamonl = [element for element in valamon]


J1 = Joueur("J1")
BOT = Bot("BOT")
plateauJ1 = [["", "", "", "", ""], ["", "", "", "", ""]]
plateauBOT = pos_cartes()

def lancement_partie():
    global diag,num_cards,J1, BOT, plateauJ1, plateauBOT, carte_rects_j1, carte_rects_j2, carte_rect_liste, cases_rect_liste, cartes_differences_liste, pos_carte_selec, prop_screen, quit, tour_end, over_screen, win_screen, attaquebot
    J1 = Joueur("J1")
    BOT = Bot("BOT")
    plateauJ1 = [["", "", "", "", ""], ["", "", "", "", ""]]
    plateauBOT = pos_cartes()
    carte_rect_liste = []
    cases_rect_liste = []
    cartes_differences_liste = []
    pos_carte_selec = None
    prop_screen, quit, tour_end, over_screen, win_screen,diag = False, False, False, False, False, False
    attaquebot = 0
    last_carte: int = -1
    num_cards = 4
    for a in range(2):
        for b in range(5):
            last_carte += 1
            cases_rect_liste.append(pygame.Rect(carte_rect))
            cases_rect_liste[last_carte].x = pos_emplacement1[a][b][0] - 60
            cases_rect_liste[last_carte].y = pos_emplacement1[a][b][1] - 70
    for i in range(num_cards):
        carte_rect_liste.append([pygame.Rect(carte_rect), i, J1.liste[i]])
        cartes_differences_liste.append(i)
    init_pos()

#--------------------------------
# Partie de Raphaël
#--------------------------------

last_carte : int = -1
for a in range(2) :
    for b in range(5) :
        last_carte += 1
        cases_rect_liste.append(pygame.Rect(carte_rect))
        cases_rect_liste[last_carte].x = pos_emplacement1[a][b][0] - 60
        cases_rect_liste[last_carte].y = pos_emplacement1[a][b][1] - 70
for i in range(num_cards) :
    carte_rect_liste.append([pygame.Rect(carte_rect),i,J1.liste[i]])
    cartes_differences_liste.append(i)

#--------------------------------
# Fin de la partie
#--------------------------------

def attaque_bot():
    global tour_end, attaquebot, pioche, bot_atk,num_cards, carte_rect_liste, cartes_differences_liste
    if attaquebot == len(carte_rects_j2):
        J1.plc += 2
        tour_end = False
        attaquebot = 0
        pioche = 0
        bot_atk = 0
        ran = random.randint(0, len(valamonl)-1)
        nouveau_valamon = Valamon(valamonl[ran][0], int(valamonl[ran][1]), int(valamonl[ran][2]),
                                   int(valamonl[ran][3]),
                                   int(valamonl[ran][4]), int(valamonl[ran][5]), int(valamonl[ran][6]),
                                   int(valamonl[ran][7]),
                                   int(valamonl[ran][8]), valamonl[ran][9], valamonl[ran][10], valamonl[ran][11],
                                   valamonl[ran][12], int(valamonl[ran][13]), int(valamonl[ran][14]))
        J1.liste.append(nouveau_valamon)
        ran = random.randint(0, len(valamonl)-1)
        nouveau_valamon = Valamon(valamonl[ran][0], int(valamonl[ran][1]), int(valamonl[ran][2]),
                                   int(valamonl[ran][3]),
                                   int(valamonl[ran][4]), int(valamonl[ran][5]), int(valamonl[ran][6]),
                                   int(valamonl[ran][7]),
                                   int(valamonl[ran][8]), valamonl[ran][9], valamonl[ran][10], valamonl[ran][11],
                                   valamonl[ran][12], int(valamonl[ran][13]), int(valamonl[ran][14]))
        BOT.liste.append(nouveau_valamon)
        BOT.liste_pasplac.append(nouveau_valamon)
        new_index = len(J1.liste) - 1
        carte_rect_liste.append([pygame.Rect(carte_rect), new_index, J1.liste[new_index]])
        cartes_differences_liste.append(new_index)
        num_cards += 1
        return
    attaquebot += 1
    ran = bot_atk
    ran1 = random.randint(0,1)
    pos_b = carte_rects_j2[ran][5]
    if plateauJ1[0][pos_b] == 'Y':
        for e in range(len(carte_rects_j1)):
            if e < len(carte_rects_j1):
                if carte_rects_j1[e][4] == 0 and carte_rects_j1[e][5] == pos_b:
                        if ran1 == 0:
                            BOT.liste[ran].attaque1(J1.liste[carte_rects_j1[e][3]], BOT, J1, carte_rects_j1[e][3], 0, pos_b,e)
                            print(BOT.liste[ran].nom)
                        else:
                            BOT.liste[ran].attaque2(J1.liste[carte_rects_j1[e][3]], BOT, J1, carte_rects_j1[e][3], 0, pos_b,e)
                            print(BOT.liste[ran].nom)
                        break
    elif plateauJ1[1][pos_b] == 'Y':
        for e in range(len(carte_rects_j1)):
            if e < len(carte_rects_j1):
                if carte_rects_j1[e][4] == 1 and carte_rects_j1[e][5] == pos_b:
                        if ran1 == 0:
                            BOT.liste[ran].attaque1(J1.liste[carte_rects_j1[e][3]], BOT, J1, carte_rects_j1[e][3], 1, pos_b,e)
                            print(BOT.liste[ran].nom)
                        else:
                            BOT.liste[ran].attaque2(J1.liste[carte_rects_j1[e][3]], BOT, J1, carte_rects_j1[e][3], 1, pos_b,e)
                            print(BOT.liste[ran].nom)
                        break
    else:
        if ran1 == 0:
            J1.pv -= BOT.liste[ran].atk1
            ran2 = random.randint(1,4)
            pygame.mixer.music.pause()
            pygame.mixer.music.set_volume(1.0)
            sound = pygame.mixer.Sound(f'assets/attaque{ran2}.mp3')
            sound.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            pygame.mixer.music.set_volume(0.3)
            pygame.time.wait(500)
            pygame.mixer.music.unpause()
            print(BOT.liste[ran].nom)
        else:
            J1.pv -= BOT.liste[ran].atk2
            ran2 = random.randint(1,4)
            pygame.mixer.music.pause()
            pygame.mixer.music.set_volume(1.0)
            sound = pygame.mixer.Sound(f'assets/attaque{ran2}.mp3')
            sound.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            pygame.mixer.music.set_volume(0.3)
            pygame.time.wait(500)
            pygame.mixer.music.unpause()
            print(BOT.liste[ran].nom)
    pygame.time.wait(500)
    bot_atk += 1
    return



while running:
    click_sound = pygame.mixer.Sound('assets/clic.mp3')
    click_sound.set_volume(1.0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                toggle_fullscreen()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    def home_screen() :
        global pos_carte_selec
        global quit
        titre = pygame.font.SysFont('Arial', 200)
        titre_surface = titre.render("Valamon", False, princip_color)
        text = pygame.font.SysFont('Arial', 70)
        bouton = pygame.image.load(f'assets/button_blue.png')
        scaled_bouton = pygame.transform.scale(bouton, (350, 100))
        text_surface = text.render("Jouer", False, (0,0,0))
        text_surface1 = text.render("Règles", False, (0,0,0))
        text_surface2 = text.render("Crédits", False, (0,0,0))
        text_surface3 = text.render("Quitter", False, (0,0,0))
        fond = pygame.image.load('assets/home_screen.png')
        fond_scaled = pygame.transform.scale(fond, (1728, 972))
        screen.blit(fond_scaled, (0, 0))
        voile = pygame.Surface((1728, 972))
        voile.set_alpha(70)
        voile.fill((0, 0, 0))
        screen.blit(voile, (0, 0))
        bouton_rect1= scaled_bouton.get_rect(center=(864, 525))
        bouton_rect2= scaled_bouton.get_rect(center=(864, 650))
        bouton_rect3= scaled_bouton.get_rect(center=(864, 775))
        bouton_rect4= scaled_bouton.get_rect(center=(864, 900))
        titre_rect = titre_surface.get_rect(center=(860, 250))
        text_rect = text_surface.get_rect(center=(864,520))
        text_rect1 = text_surface1.get_rect(center=(864,645))
        text_rect2 = text_surface2.get_rect(center=(864,770))
        text_rect3 = text_surface3.get_rect(center=(864,895))
        screen.blit(scaled_bouton, bouton_rect1)
        screen.blit(scaled_bouton, bouton_rect2)
        screen.blit(scaled_bouton, bouton_rect3)
        screen.blit(scaled_bouton, bouton_rect4)
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
                    return
                if is_text_clicked(mouse_x, mouse_y, text_rect2):
                    print("Passage sur les crédits")
                    screen_type = "credit"
                    return
                if is_text_clicked(mouse_x,mouse_y,text_rect1):
                    webbrowser.open('https://github.com/Energielulu83852/Valamon/wiki/Rules')

    def solo() :
        global atk_selec, diag, carte_rects_j1, carte_rects_j2, pos_carte_selec, over_screen, win_screen, tour_end, cartes_joues, attaquebot, valamonlist, carte_rect, startscreen, prop_screen
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (35, 35))
        home_rect = scaled_image.get_rect(topleft=(10, 10))
        fond = pygame.image.load('assets/plateau.png')
        screen.blit(fond, (0, 0))
        screen.blit(scaled_image, home_rect)
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
        elif startscreen == False:
            if J1.pv <= 0:
                go = pygame.image.load('assets/GO.png')
                voile = pygame.Surface((1728, 972))
                voile.set_alpha(128)
                voile.fill((0, 0, 0))
                screen.blit(voile, (0, 0))
                go_rect = go.get_rect(center=(864, 486))
                screen.blit(go, go_rect)
                over_screen = True
            if BOT.pv <= 0:
                win = pygame.image.load('assets/WIN.png')
                voile = pygame.Surface((1728, 972))
                voile.set_alpha(128)
                voile.fill((0, 0, 0))
                screen.blit(voile, (0, 0))
                win_rect = win.get_rect(center=(864, 486))
                screen.blit(win, win_rect)
                win_screen = True
            if over_screen == False and win_screen == False:
                init_pos()
                pygame.font.init()
                text_end = pygame.font.SysFont('Arial', 30)
                bouton = pygame.image.load(f'assets/button_blue.png')
                bouton_rect= bouton.get_rect(center=(1321, 590))
                screen.blit(bouton, bouton_rect)
                text_surface_end = text_end.render("Fin de tour", False, (0,0,0))
                text_rect_end = text_surface_end.get_rect(center=(1321, 590))
                screen.blit(text_surface_end, text_rect_end)
                coeur = pygame.image.load(f'assets/coeur.png')
                coeur_rect= coeur.get_rect(center=(1281, 690))
                screen.blit(coeur, coeur_rect)
                coeur_bot = pygame.image.load(f'assets/coeur.png')
                coeur_bot_rect= coeur_bot.get_rect(center=(440, 130))
                screen.blit(coeur_bot, coeur_bot_rect)
                plc = pygame.image.load(f'assets/mana.png')
                plc_rect= plc.get_rect(center=(1401, 690))
                screen.blit(plc, plc_rect)
                pv_j = J1.pv
                plc_j = J1.plc
                pv_bot = BOT.pv
                img_pv = pygame.image.load(f'assets/chiffre_{pv_j}.png')
                img_h, img_l = img_pv.get_size()
                img_pv = pygame.transform.scale(img_pv, (img_h*2, img_l*2))
                img_pv_rect = img_pv.get_rect(center=(1281, 690))
                screen.blit(img_pv, img_pv_rect)
                img_pv_bot = pygame.image.load(f'assets/chiffre_{pv_bot}.png')
                img_bot_h, img_bot_l = img_pv_bot.get_size()
                img_pv_bot = pygame.transform.scale(img_pv_bot, (img_bot_h*2, img_bot_l*2))
                img_pv_bot_rect = img_pv_bot.get_rect(center=(440, 130))
                screen.blit(img_pv_bot, img_pv_bot_rect)
                img_plc = pygame.image.load(f'assets/chiffre_{plc_j}.png')
                img_plc_h, img_plc_l = img_plc.get_size()
                img_plc = pygame.transform.scale(img_plc, (img_plc_h*2, img_plc_l*2))
                img_plc_rect = img_plc.get_rect(center=(1401, 690))
                screen.blit(img_plc, img_plc_rect)
                for carte_rect, pos_a, pos_b, i, a, b in carte_rects_j1:
                    if plateauJ1[a][b] == 'Y':
                        carte = pygame.image.load(f'assets/carte_{J1.liste[i].nom}.png')
                        pv = J1.liste[i].pv
                        img_pv = pygame.image.load(f'assets/chiffre_{pv}.png')
                        img_pv_rect = img_pv.get_rect(center=(pos_a+20, pos_b+55))
                        screen.blit(carte, carte_rect)
                        screen.blit(img_pv, img_pv_rect)
                for i in range(len(carte_rects_j2)):
                    carte = pygame.image.load(f'assets/carte_{BOT.liste[carte_rects_j2[i][3]].nom}.png')
                    pv = BOT.liste[carte_rects_j2[i][3]].pv
                    img_pv = pygame.image.load(f'assets/chiffre_{pv}.png')
                    img_pv_rect = img_pv.get_rect(center=(carte_rects_j2[i][1]+20, carte_rects_j2[i][2]+55))
                    screen.blit(carte, carte_rects_j2[i][0])
                    screen.blit(img_pv, img_pv_rect)

#--------------------------------------------------------------
# Partie de Raphaël
#--------------------------------------------------------------
                global num_cards
                global button_clicked
                global selection_carte
                global cartes_differences_liste
                global carte_rect_liste
                global pos_emplacement1

                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()

                rect_surface = pygame.Surface((2000, 2000), pygame.SRCALPHA)

                for i in range(len(carte_rect_liste)):
                    pygame.draw.rect(rect_surface, (255, 0, 0, 0), carte_rect_liste[i][0])
                for i in range(len(cases_rect_liste)):
                    pygame.draw.rect(rect_surface, (0, 0, 0, 0), cases_rect_liste[i])
                screen.blit(rect_surface, (0, 0))

                # Afficher 5 cartes sur une ligne
                display_cards(screen, num_cards)

                # Handle mouse button down event ------- ACTION LORSQUE CLIQUE SUR CARTE----
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(carte_rect_liste)):
                        if carte_rect_liste[i][0].collidepoint(event.pos) and not button_clicked:
                            if not J1.liste[carte_rect_liste[i][1]].plc > J1.plc :
                                selection_carte = carte_rect_liste[i][1]
                                pos_carte_selec = [carte_rect_liste[i][0].x+60, carte_rect_liste[i][0].y+80, selection_carte, 0, 0]
                                button_clicked = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pop = False
                    for j in range(len(cases_rect_liste)):  # Parcours toutes les cases du plateau
                        if cases_rect_liste[j].collidepoint(event.pos):
                            if selection_carte != None:
                                a = j //5
                                b = j%5
                                if not plateauJ1[a][b] == 'Y':
                                    poser_carte(selection_carte, j)

                                    num_cards -= 1
                                    pop = True
                                    cartes_differences_liste.pop()
                                    button_clicked = True
                                    break  # Sort de la boucle après avoir placé la carte pour éviter plusieurs placements

                    if pop:
                        for i in range(len(carte_rect_liste)):
                            if carte_rect_liste[i][2] == J1.liste[selection_carte]:
                                del_carte = i
                        carte_rect_liste.pop(del_carte)

                        selection_carte = None

                # Handle mouse button up event
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(len(carte_rect_liste)):
                        if not carte_rect_liste[i][0].collidepoint(event.pos):
                            button_clicked = False

                # Handle mouse button up event
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in range(len(carte_rect_liste)):
                        if carte_rect_liste[i][0].collidepoint(event.pos):
                            button_clicked = False

                # Check if mouse is over the text
                for i in range(len(carte_rect_liste)):
                    if carte_rect_liste[i][0].collidepoint(mouse_pos):
                        carte_rect_liste[i][0].y = carte_rect_liste[i][0].y - 10
                    else:
                        carte_rect_liste[i][0].y = carte_rect_liste[i][0].y

# --------------------------------------------------------------
# Fin de la partie
# --------------------------------------------------------------

                if pos_carte_selec != None and not tour_end == True:
                    pygame.font.init()
                    text = pygame.font.SysFont('Arial', 30)
                    text_surface = text.render("Propriétés", False, (0,0,0))
                    text_surface2 = text.render("Attaque 1", False, (0,0,0))
                    text_surface3 = text.render("Attaque 2", False, (0,0,0))
                    posi_a = pos_carte_selec[0]
                    posi_b = pos_carte_selec[1]
                    text_rect = text_surface.get_rect(center=(381, 525))
                    text_rect2 = text_surface2.get_rect(center=(381, 580))
                    text_rect3 = text_surface3.get_rect(center=(381, 640))
                    bouton_rect1= bouton.get_rect(center=(381, 525))
                    bouton_rect2= bouton.get_rect(center=(381, 580))
                    bouton_rect3= bouton.get_rect(center=(381, 640))
                    voile = pygame.Surface((125, 165))
                    voile.set_alpha(64)
                    voile.fill((255, 255, 153))
                    screen.blit(voile, (posi_a-65, posi_b-80))
                    screen.blit(bouton, bouton_rect1)
                    screen.blit(bouton, bouton_rect2)
                    screen.blit(bouton, bouton_rect3)
                    screen.blit(text_surface, text_rect)
                    screen.blit(text_surface2, text_rect2)
                    screen.blit(text_surface3, text_rect3)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if is_text_clicked(mouse_x, mouse_y, text_rect):
                            prop_screen = True
                        if is_text_clicked(mouse_x, mouse_y, text_rect2):
                            if J1.liste[pos_carte_selec[2]].diag == 0:
                                if plateauBOT[1][pos_carte_selec[4]] == 'Y':
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == 1 and carte_rects_j2[e][5] == pos_carte_selec[4]:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque1(BOT.liste[cartead], J1, BOT, carte_rects_j2[e][3], 1, pos_carte_selec[4],e)
                                                break
                                elif plateauBOT[0][pos_carte_selec[4]] == 'Y':
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == 0 and carte_rects_j2[e][5] == pos_carte_selec[4]:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque1(BOT.liste[cartead], J1, BOT, carte_rects_j2[e][3], 0, pos_carte_selec[4],e)
                                                break
                                else:
                                    BOT.pv -= J1.liste[pos_carte_selec[2]].atk1
                                    ran = random.randint(1,4)
                                    pygame.mixer.music.pause()
                                    pygame.mixer.music.set_volume(1.0)
                                    sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
                                    sound.play()
                                    while pygame.mixer.music.get_busy():
                                        pygame.time.wait(100)
                                    pygame.mixer.music.set_volume(0.3)
                                    pygame.time.wait(500)
                                    pygame.mixer.music.unpause()
                                    cartes_joues.append(pos_carte_selec[2])
                                    pos_carte_selec=None
                            else:
                                diag = True
                                atk_selec = 1
                        if is_text_clicked(mouse_x, mouse_y, text_rect3):
                            if J1.liste[pos_carte_selec[2]].diag == 0 :
                                if plateauBOT[1][pos_carte_selec[4]] == 'Y':
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == 1 and carte_rects_j2[e][5] == pos_carte_selec[4]:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque2(BOT.liste[cartead], J1, BOT,carte_rects_j2[e][3], 1, pos_carte_selec[4],e)
                                                break
                                elif plateauBOT[0][pos_carte_selec[4]] == 'Y':
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == 0 and carte_rects_j2[e][5] == pos_carte_selec[4]:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque2(BOT.liste[cartead], J1, BOT,carte_rects_j2[e][3], 0, pos_carte_selec[4],e)
                                                break
                                else:
                                    BOT.pv -= J1.liste[pos_carte_selec[2]].atk2
                                    ran = random.randint(1,4)
                                    pygame.mixer.music.pause()
                                    pygame.mixer.music.set_volume(1.0)
                                    sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
                                    sound.play()
                                    while pygame.mixer.music.get_busy():
                                        pygame.time.wait(100)
                                    pygame.mixer.music.set_volume(0.3)
                                    pygame.time.wait(500)
                                    pygame.mixer.music.unpause()
                                    cartes_joues.append(pos_carte_selec[2])
                                    pos_carte_selec=None
                            else:
                                diag = True
                                atk_selec = 2
                if diag == True:
                    voile = pygame.Surface((125, 165))
                    voile.set_alpha(64)
                    voile.fill((255, 255, 0))
                    highlighted_rects = []
                    if pos_carte_selec[3] == 0:
                        if pos_carte_selec[4] > 0 and plateauBOT[1][pos_carte_selec[4] - 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[1][pos_carte_selec[4] - 1][0] - 65, pos_emplacement2[1][pos_carte_selec[4] - 1][1] - 80,125,165)
                            highlighted_rects.append([rect,1,pos_carte_selec[4] - 1])
                            screen.blit(voile, rect.topleft)
                        elif pos_carte_selec[4] > 0 and plateauBOT[0][pos_carte_selec[4] - 1] == 'Y':
                            rect=pygame.Rect(pos_emplacement2[0][pos_carte_selec[4] - 1][0] - 65, pos_emplacement2[0][pos_carte_selec[4] - 1][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4] - 1])
                            screen.blit(voile, rect.topleft)
                        if pos_carte_selec[4] < 4 and plateauBOT[1][pos_carte_selec[4] + 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[1][pos_carte_selec[4] + 1][0] - 65, pos_emplacement2[1][pos_carte_selec[4] + 1][1] - 80,125,165)
                            highlighted_rects.append([rect,1,pos_carte_selec[4] + 1])
                            screen.blit(voile, rect.topleft)
                        elif pos_carte_selec[4] < 4 and plateauBOT[0][pos_carte_selec[4] + 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[0][pos_carte_selec[4] + 1][0] - 65, pos_emplacement2[0][pos_carte_selec[4] + 1][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4] + 1])
                            screen.blit(voile, rect.topleft)
                        if plateauBOT[1][pos_carte_selec[4]] == 'Y':
                            rect = pygame.Rect(pos_emplacement2[1][pos_carte_selec[4]][0] - 65,pos_emplacement2[1][pos_carte_selec[4]][1] - 80, 125, 165)
                            highlighted_rects.append([rect, 1, pos_carte_selec[4]])
                            screen.blit(voile, rect.topleft)
                        elif plateauBOT[0][pos_carte_selec[4]] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[0][pos_carte_selec[4]][0] - 65, pos_emplacement2[0][pos_carte_selec[4]][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4]])
                            screen.blit(voile, rect.topleft)

                    else:
                        if pos_carte_selec[4] > 0 and plateauBOT[1][pos_carte_selec[4] - 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[1][pos_carte_selec[4] - 1][0] - 65, pos_emplacement2[1][pos_carte_selec[4] - 1][1] - 80,125,165)
                            highlighted_rects.append([rect,1,pos_carte_selec[4] - 1])
                            screen.blit(voile, rect.topleft)
                        elif pos_carte_selec[4] > 0 and plateauBOT[0][pos_carte_selec[4] - 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[0][pos_carte_selec[4] - 1][0] - 65, pos_emplacement2[0][pos_carte_selec[4] - 1][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4] - 1])
                            screen.blit(voile, rect.topleft)
                        if pos_carte_selec[4] < 4 and plateauBOT[1][pos_carte_selec[4] + 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[1][pos_carte_selec[4] + 1][0] - 65, pos_emplacement2[1][pos_carte_selec[4] + 1][1] - 80,125,165)
                            highlighted_rects.append([rect,1,pos_carte_selec[4] + 1])
                            screen.blit(voile, rect.topleft)
                        elif pos_carte_selec[4] < 4 and plateauBOT[0][pos_carte_selec[4] + 1] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[0][pos_carte_selec[4] + 1][0] - 65, pos_emplacement2[0][pos_carte_selec[4] + 1][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4] + 1])
                            screen.blit(voile, rect.topleft)
                        if plateauBOT[1][pos_carte_selec[4]] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[1][pos_carte_selec[4]][0] - 65, pos_emplacement2[1][pos_carte_selec[4]][1] - 80,125,165)
                            highlighted_rects.append([rect,1,pos_carte_selec[4]])
                        elif plateauBOT[0][pos_carte_selec[4]] == 'Y':
                            rect= pygame.Rect(pos_emplacement2[0][pos_carte_selec[4]][0] - 65, pos_emplacement2[0][pos_carte_selec[4]][1] - 80,125,165)
                            highlighted_rects.append([rect,0,pos_carte_selec[4]])
                            screen.blit(voile, rect.topleft)
                    if highlighted_rects == []:
                        if atk_selec == 1:
                            BOT.pv -= J1.liste[pos_carte_selec[2]].atk1
                            ran = random.randint(1, 4)
                            pygame.mixer.music.pause()
                            pygame.mixer.music.set_volume(1.0)
                            sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
                            sound.play()
                            while pygame.mixer.music.get_busy():
                                pygame.time.wait(100)
                            pygame.mixer.music.set_volume(0.3)
                            pygame.time.wait(500)
                            pygame.mixer.music.unpause()
                            cartes_joues.append(pos_carte_selec[2])
                            pos_carte_selec = None
                            diag = False
                        elif atk_selec == 2:
                            BOT.pv -= J1.liste[pos_carte_selec[2]].atk2
                            ran = random.randint(1, 4)
                            pygame.mixer.music.pause()
                            pygame.mixer.music.set_volume(1.0)
                            sound = pygame.mixer.Sound(f'assets/attaque{ran}.mp3')
                            sound.play()
                            while pygame.mixer.music.get_busy():
                                pygame.time.wait(100)
                            pygame.mixer.music.set_volume(0.3)
                            pygame.time.wait(500)
                            pygame.mixer.music.unpause()
                            cartes_joues.append(pos_carte_selec[2])
                            pos_carte_selec = None
                            diag = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        for rect,a,b in highlighted_rects:
                            if rect.collidepoint(mouse_x, mouse_y):
                                if atk_selec == 1 :
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == a and carte_rects_j2[e][5] == b:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque1(BOT.liste[cartead], J1, BOT,carte_rects_j2[e][3], a, b,e)
                                else:
                                    for e in range(len(carte_rects_j2)):
                                        if e < len(carte_rects_j2):
                                            if carte_rects_j2[e][4] == a and carte_rects_j2[e][5] == b:
                                                cartead = carte_rects_j2[e][3]
                                                cartes_joues.append(pos_carte_selec[2])
                                                J1.liste[pos_carte_selec[2]].attaque2(BOT.liste[cartead], J1, BOT,carte_rects_j2[e][3], a, b,e)
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
                                if i not in cartes_joues :
                                    diag = False
                                    pos_carte_selec = [posa, posb, i, a, b]
                                    break
                        if is_text_clicked(mouse_x, mouse_y, text_rect_end):
                            tour_end = True
                            pos_carte_selec = None
                            cartes_joues = []
                            diag = False
                            attaque_bot()
                if attaquebot != 0:
                    attaque_bot()
                elif len(cartes_joues) == len(carte_rects_j1) :
                    if len(cartes_joues) != 0:
                        tour_end = True
                        cartes_joues = []
                        attaque_bot()


        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if is_text_clicked(mouse_x, mouse_y, home_rect):
                    if J1.pv <= 0 or BOT.pv <= 0 :
                        global running
                        running = False
                    else:
                        global screen_type
                        screen_type = 'home'

    def credit() :
        pygame.font.init()
        home = pygame.image.load('assets/house-solid.svg')
        scaled_image = pygame.transform.scale(home, (25, 25))
        titre = pygame.font.SysFont('Arial', 150)
        text = pygame.font.SysFont('Arial', 75)
        copyrights = pygame.font.SysFont('Arial', 50)
        titre_surface = titre.render("Valamon", False, princip_color)
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
        pygame.mixer.music.stop()
        credit()

    # flip() the display to put your work on screen
    pygame.display.flip()
    musique_actuelle = jouer_musique(screen_type, musique_actuelle)

    #clock.tick(60)  # limits FPS to 60

print("Merci d'avoir joué")
pygame.quit()
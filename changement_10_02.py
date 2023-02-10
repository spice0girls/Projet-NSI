import pyxel

pyxel.init(256, 256, title="Tiny Adventurer")
pyxel.load("art1_.pyxres")

# personage
perso_x = 128
perso_y = 182
taille_perso_x = 8
taille_perso_y = 13

# saut
jump = False
taille_saut = 56
space_appuie = 0

# mouvement perso
pvitesse_mouv_dg = 3
pvitesse_mouv_haut = 7
pvitesse_mouv_bas = 8
monte = False
descente = False

# general
playing = 0
scroll = 0
continuous_scroll = 0
ecran_bord=256 # scroll qui peut que monté pour ne pas avoir de respawn des ennemis après avoir reculé
scroll_limitd = 150
scroll_limitg = 80
floor = 190
last_floor = floor
last_scroll = scroll
vie = 3

# plateforme
hauteur_1=140
hauteur_2=90
plateforme_liste = [[ecran_bord, hauteur_1,1],[ecran_bord, hauteur_1,3],[ecran_bord, hauteur_1,5],[ecran_bord, hauteur_1,16],[ecran_bord,hauteur_1,18],[ecran_bord, hauteur_1,20],[ecran_bord, hauteur_2,25],[ecran_bord,hauteur_2,27],[ecran_bord,hauteur_2,29],[ecran_bord,hauteur_1,35], [ecran_bord,hauteur_1,37],[ecran_bord,hauteur_1,39]]
#dans platefrome liste [x,y,scroll d'apparition] qui utilise deux hauteurs différentes
taille_plateforme = 8
plvitesse_mouv = 3

# ennemi
ennemi_liste = []
taille_ennemi_y = 8
taille_ennemi_x = 8
ennemi_vitesse_mouv = 1
ennemi_floor_base = floor
ennemi_vitesse_mouv_bas = 8

pyxel.playm(0, loop=True)


def perso_deplacement(x, y, jump, scroll, last_scroll, last_floor, monte, descente, continuous_scroll, vie,
                      ennemi_liste):
    """déplacement du personnage"""
    last_scroll = scroll
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < scroll_limitd):
            x = x + pvitesse_mouv_dg
        else:
            scroll += 1
            continuous_scroll += 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > scroll_limitg):
            x = x - pvitesse_mouv_dg
        elif scroll > 0:
            scroll -= 1

    if pyxel.btn(pyxel.KEY_SPACE):
        if jump == False:
            last_floor = y + taille_perso_y
            jump = True

    if jump == True:
        if last_floor - taille_saut - taille_perso_y <= y and descente == False:
            monte = True
        else:
            monte = False
            descente = True
            if y + taille_perso_y + pvitesse_mouv_bas >= floor:
                descente = False
                y = floor - taille_perso_y
                jump = False
    else:
        if y + taille_perso_y != floor:
            if y + taille_perso_y + pvitesse_mouv_bas < floor:
                descente = True
            else:
                y = floor - taille_perso_y
                descente = False
                monte = False
    if monte == True:
        y = y - pvitesse_mouv_haut
    if descente == True:
        y = y + pvitesse_mouv_bas
    if len(ennemi_liste) != 0:
        vie, ennemi_liste = contact_ennemi(vie, ennemi_liste)
    return x, y, jump, scroll, last_scroll, last_floor, monte, descente, continuous_scroll, vie, ennemi_liste


def contact_ennemi(vie, ennemi_liste):
    """savoir si il y a contact entre l'ennemi et le personnage"""
    for ennemi in ennemi_liste:
        if perso_y < ennemi[1] + taille_ennemi_y and perso_y + taille_perso_y > ennemi[1] and perso_x + taille_perso_x > \
                ennemi[0] and perso_x < ennemi[0] + taille_ennemi_x:
            vie -= 1
            ennemi_liste.remove(ennemi)
    return vie, ennemi_liste


def plateforme_creation(plateforme_liste, x, y):
    """création d'une plateforme"""
    plateforme_liste.append([x, y])


def plateforme_deplacement(plaforme_liste):
    """déplacement des plateformes"""
    if last_scroll > scroll:
        for plateforme in plateforme_liste:
            if plateforme[2]<scroll:
                plateforme[0] += plvitesse_mouv
        return plateforme_liste
    if last_scroll < scroll:
        for plateforme in plateforme_liste:
            if plateforme[2] < scroll:
                plateforme[0] -= plvitesse_mouv
        return plateforme_liste
    return plateforme_liste


def ennemi_creation(ennemi_liste, x, y, ennemi_floor):
    """creation d'ennemi dependant un niveau"""
    ennemi_liste.append([x, y, ennemi_floor])


def ennemi_deplacement(ennemi_liste):
    """tout les déplacements de tout les ennemis"""
    for ennemi in ennemi_liste:
        if ennemi[0] < 0:
            ennemi_liste.remove(ennemi)
    if last_scroll > scroll:
        for ennemi in ennemi_liste:
            ennemi[0] += (ennemi_vitesse_mouv - plvitesse_mouv)
    elif last_scroll < scroll:
        for ennemi in ennemi_liste:
            ennemi[0] -= (ennemi_vitesse_mouv + plvitesse_mouv)
    else:
        for ennemi in ennemi_liste:
            ennemi[0] -= ennemi_vitesse_mouv
    for ennemi in ennemi_liste:
        ennemi = ennemi_movement_y(ennemi)
    return ennemi_liste


def ennemi_movement_y(ennemi):
    """pour savoir si un ennemi doit descendre"""
    for plateforme in plateforme_liste:
        if ennemi[1] + taille_ennemi_y <= plateforme[1] and ennemi[0] + taille_ennemi_x > plateforme[0] and ennemi[0] < \
                plateforme[0] + taille_plateforme:
            ennemi[2] = plateforme[1]
            ennemi = ennemi_fall(ennemi)
            return ennemi
        else:
            ennemi[2] = ennemi_floor_base
    if ennemi[1] + taille_ennemi_y != ennemi[2]:
        ennemi = ennemi_fall(ennemi)
    return ennemi


def ennemi_fall(ennemi):
    """pour faire descendre un ennemi"""
    if ennemi[1] + taille_ennemi_y + ennemi_vitesse_mouv_bas < ennemi[2]:
        ennemi[1] += ennemi_vitesse_mouv_bas
    else:
        ennemi[1] = ennemi[2] - taille_ennemi_y
    return ennemi


def floor_is(floor):
    """définit le sol du perso à un moment donné, pour savoir si celui ci doit decsendre ou rester"""
    for plateforme in plateforme_liste:
        if perso_y + taille_perso_y <= plateforme[1] and perso_x + taille_perso_x > plateforme[0] and perso_x < \
                plateforme[0] + taille_plateforme:
            floor = plateforme[1]
            return floor
    floor = 190
    return floor


def update():
    """mise à jour des variables (30 fois par seconde)"""

    global perso_x, perso_y, jump, scroll, last_scroll, plateforme_liste, floor, pvitesse_mouv_dg, last_floor, monte, descente, playing, ennemi_liste, ennemi_floor_base, \
        continuous_scroll, taille_perso_x, taille_perso_y, taille_plateforme, taille_ennemi_y, taille_ennemi_x, vie
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if playing == 0:
        if pyxel.btn(pyxel.KEY_S):
            playing = 1
    if scroll >= 120:
        playing = 2
    if playing == 1:
        perso_x, perso_y, jump, scroll, last_scroll, last_floor, monte, descente, continuous_scroll, vie, ennemi_liste = perso_deplacement(
            perso_x, perso_y, jump, scroll, last_scroll, last_floor, monte, descente, continuous_scroll, vie,
            ennemi_liste)
        if (continuous_scroll == 14 or continuous_scroll == 50 )and last_scroll != scroll:
            ennemi_creation(ennemi_liste, ecran_bord, floor - taille_ennemi_y, floor)
        if continuous_scroll==39 and last_scroll!=scroll:
            ennemi_creation(ennemi_liste,ecran_bord,hauteur_1-taille_ennemi_y, hauteur_1)
        if last_scroll != scroll:
            plateforme_liste = plateforme_deplacement(plateforme_liste)
        ennemi_liste = ennemi_deplacement(ennemi_liste)
        floor = floor_is(floor)
    if vie <= 0:
        playing = 3


def draw():
    """création des objets (30 fois par seconde)"""
    print(playing, vie)
    pyxel.cls(0)
    if playing == 0:
        pyxel.text(95, 20, "press s to start", 7)
        pyxel.text(96, 230, "press q to quit", 7)
        pyxel.blt(85, 100, 0, 0, 48, 80, 32)
    if playing == 1:
        pyxel.blt(perso_x, perso_y, 0, 4, 25, taille_perso_x, taille_perso_y, 6)
        for plateforme in plateforme_liste:
            if plateforme[2]<scroll:
                pyxel.blt(plateforme[0], plateforme[1], 0, 16, 8, taille_plateforme, taille_plateforme)
        for ennemi in ennemi_liste:
            pyxel.rect(ennemi[0], ennemi[1], taille_ennemi_x, taille_ennemi_y, 3)
        if vie == 3:
            pyxel.blt(15, 20, 0, 29, 6, 6, 5, 0)
            pyxel.blt(25, 20, 0, 29, 6, 6, 5, 0)
            pyxel.blt(35, 20, 0, 29, 6, 6, 5, 0)
        if vie == 2:
            pyxel.blt(15, 20, 0, 29, 6, 6, 5, 0)
            pyxel.blt(25, 20, 0, 29, 6, 6, 5, 0)
            pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)
        if vie == 1:
            pyxel.blt(15, 20, 0, 29, 6, 6, 5, 0)
            pyxel.blt(25, 20, 0, 45, 6, 6, 5, 0)
            pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)
    if playing == 2:
        pyxel.blt(90, 100, 0, 16, 96, 80, 32, 0)
    if playing == 3:
        pyxel.blt(90, 100, 0, 0, 136, 80, 32, 0)


pyxel.run(update, draw)

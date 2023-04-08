import pyxel

pyxel.init(256, 256, title="Tiny Adventurer")
pyxel.load("art1_3.pyxres")

# personage
perso_x = 128
perso_y = 182
taille_perso_x = 8
taille_perso_y = 13
compteur_animation_1 = True
compteur_animation_2 = True
touche = False

# saut
jump = False
taille_saut = 56

# mouvement perso
pvitesse_mouv_dg = 2.5  # vitesse de mouvement du personnage vers la gauche ou la droite (mouvement horizontal)
pvitesse_mouv_haut = 7  # vitesse de mouvement du personnage en montée (vers le haut)
pvitesse_mouv_bas = 8  # vitesse de mouvement du personnage en descente (vers le haut)
monte = False
descente = False

# general
playing = 0  # variable pour changer entre les différent(e)s vues/écrans du jeu
scroll = 0  # variable pour compter l'avancement en termes de position dans un niveau, peut monter et descendre,
# sert à faire bouger correctement les plateformes, les ennemies et le personnage
continuous_scroll = 0  # variable pour compter l'avancement en termes de position dans un niveau, peut seulement
# monter, sert à ce que les ennemies ne spawn/apparaissent qu'une seule fois (même après avoir reculé)
ecran_bord = 256  # bord de l'écran de jeu, toujours fixe
scroll_limitd = 150  # limite le mouvement du personnage vers la droite de l'écran(pour qu'il ne sorte pas de l'écran)
scroll_limitg = 80  # limite le mouvement du personnage vers la gauche de l'écran
floor = 192  # le "sol" du personnage sur lequel il est ou atterrit toujours,
# change si le personnage est au-dessus d'une plateforme
last_floor = floor  # permet de savoir si le "sol" du personnage change au cours de l'action
floor_base = floor  # "sol" toujours égal à la même valeur (pas comme floor qui dépend du personnage)
last_scroll = scroll  # permet de savoir si et comment le scroll (avancement dans le niveau) change au cours de l'action
vie = 3
niveau = 0
compteur = 0  # pour initialiser une seule fois les variables au début du niveau
points = 0
star1 = 25  # à enlever quand niveau 3 fini
star2 = 25  # à enlever quand niveau 3 fini
star3 = 25  # à enlever quand niveau 3 fini

# plateforme
hauteur_1 = 140
hauteur_2 = 90
hauteur_3 = 115
# 2 hauteurs fixent pour les plateformes
plateforme_liste = []
taille_plateforme = 8
plvitesse_mouv = pvitesse_mouv_dg  # vitesse de mouvement des plateformes

# ennemi
ennemi_liste = []
taille_ennemi_y = 10
taille_ennemi_x = 11
ennemi_vitesse_mouv = 1
ennemi_vitesse_mouv_initial = ennemi_vitesse_mouv  # pour pouvoir facilement réinitialisé la vitesse de mouvement
# en début de niveau
ennemi_vitesse_mouv_bas = 8

# projectile ennemi
projectile_liste = []
taille_projectile_x = 5
taille_projectile_y = 2
projectile_vitesse = ennemi_vitesse_mouv + 1

# fleur
fleur_liste = []
taille_fleur_x = 5
taille_fleur_y = 10
hauteur_0_fleur = floor - taille_fleur_y
hauteur_1_fleur = hauteur_1 - taille_fleur_y
hauteur_2_fleur = hauteur_2 - taille_fleur_y
hauteur_3_fleur = hauteur_3 - taille_fleur_y
regular_points=25

# background et déco
background = 0
arbre_liste = [[ecran_bord, 20], [ecran_bord, 100], [ecran_bord, 200], [ecran_bord, 260], [ecran_bord, 280], [ecran_bord, 340],[ecran_bord, 380], [ecran_bord, 450], [ecran_bord, 490]]
buisson_liste = [[ecran_bord, 40], [ecran_bord, 135], [ecran_bord, 145], [ecran_bord, 240], [ecran_bord, 300], [ecran_bord, 410], [ecran_bord, 470]]
# dans arbre_liste et buisson_liste [x, scroll d'apparition]
tuto=False

pyxel.playm(0,loop=True)
pyxel.play(1,63)


def perso_deplacement():
    """Déplacement du personnage"""
    global perso_x, perso_y, jump, scroll, last_scroll, last_floor, monte, descente, \
        continuous_scroll, vie, ennemi_liste, last_perso_x, tuto
    last_scroll = scroll
    last_perso_x = perso_x
    if pyxel.btn(pyxel.KEY_RIGHT):
        if perso_x < scroll_limitd:
            perso_x = perso_x + pvitesse_mouv_dg
        else:
            scroll += 1
            continuous_scroll += 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if perso_x > scroll_limitg:
            perso_x = perso_x - pvitesse_mouv_dg
        elif scroll > 0:
            scroll -= 1

    if pyxel.btn(pyxel.KEY_SPACE):
        tuto=False
        if not jump:
            last_floor = perso_y + taille_perso_y
            jump = True

    if jump:
        # si la hauteur n'est pas encore atteinte : commencer ou continuer à monter
        if last_floor - taille_saut - taille_perso_y <= perso_y and not descente:
            monte = True
        else:  # si la hauteur du saut est atteinte : commencer à descendre
            monte = False
            descente = True
            # si le personage est atterri sur le sol (qui peut être une plateforme) : fin du saut et
            # réinitialisé emplacement (perso_y) pour être bien aligné
            if perso_y + taille_perso_y + pvitesse_mouv_bas >= floor:
                descente = False
                perso_y = floor - taille_perso_y
                jump = False
    else:
        # teste si le personnage n'est pas sur le sol
        if perso_y + taille_perso_y != floor:
            if perso_y + taille_perso_y + pvitesse_mouv_bas < floor:
                descente = True
            else:
                # réinitialiser perso_y pour qu'il ne se retrouve pas dans une plateforme ou dans le sol
                perso_y = floor - taille_perso_y
                descente = False
                monte = False
    if monte:
        perso_y = perso_y - pvitesse_mouv_haut
    if descente:
        perso_y = perso_y + pvitesse_mouv_bas
    if len(ennemi_liste) != 0:  # vérifier s'il y a un contact entre le personnage et les ennemies
        contact()
    contact_fleur()
    return


def contact():
    """Savoir s'il y a contact entre l'ennemi et le personnage"""
    global vie, touche
    for ennemi in ennemi_liste:
        if perso_y < ennemi[1] + taille_ennemi_y and perso_y + taille_perso_y > ennemi[1] \
                and perso_x + taille_perso_x > ennemi[0] and perso_x < ennemi[0] + taille_ennemi_x:
            vie -= 1
            touche = True
            ennemi_liste.remove(ennemi)
            pyxel.play(2, 1)
    for projectile in projectile_liste:
        if perso_y < projectile[1] + taille_projectile_y and perso_y + taille_perso_y > projectile[1] \
                and perso_x + taille_perso_x > projectile[0] and perso_x < projectile[0] + taille_projectile_x:
            vie -= 1
            touche = True
            projectile_liste.remove(projectile)
            pyxel.play(2,1)
    return

def contact_fleur():
    global points, regular_points
    for fleur in fleur_liste:
        if perso_y < fleur[1] + taille_fleur_y and perso_y + taille_perso_y > fleur[1] \
                and perso_x + taille_perso_x > fleur[0] and perso_x < fleur[0] + taille_fleur_x:
            points += regular_points
            fleur_liste.remove(fleur)
            pyxel.play(2,2)
            return

def plateforme_deplacement():
    """Déplacement des plateformes"""
    if last_scroll > scroll:
        for plateforme in plateforme_liste:
            if plateforme[2] < scroll:
                plateforme[0] += plvitesse_mouv
        return
    if last_scroll < scroll:
        for plateforme in plateforme_liste:
            if plateforme[2] < scroll:
                plateforme[0] -= plvitesse_mouv
        return
    return

def deplacement_avec_plateforme_deco(liste):
    """Déplacement des fleurs"""
    if last_scroll > scroll:
        for element in liste:
            if element[1] < scroll:
                element[0] += plvitesse_mouv
        return
    if last_scroll < scroll:
        for element in liste:
            if element[1] < scroll:
                element[0] -= plvitesse_mouv
        return
    return

def deplacement_avec_plateforme(liste):
    """Déplacement des fleurs"""
    if last_scroll > scroll:
        for element in liste:
            if element[2] < scroll:
                element[0] += plvitesse_mouv
        return
    if last_scroll < scroll:
        for element in liste:
            if element[2] < scroll:
                element[0] -= plvitesse_mouv
        return
    return

def ennemi_creation(y, ennemi_floor, projectile, reste_sur_plateforme):
    """Création d'ennemi dependant un niveau"""
    global ecran_bord
    # dans ennemi_liste: x l'ennemi, y l'ennemi, le sol de l'ennemi, projectile ou non?, reste sur plateforme ou non?,
    # sens inverse (Faux au début)
    ennemi = [ecran_bord, y, ennemi_floor]
    if not projectile:
        ennemi.append(False)
    else:
        ennemi.append(True)

    if reste_sur_plateforme:
        ennemi.append(True)
    else:
        ennemi.append(False)
    ennemi.append(False)  # pour aller vers la gauche (sense normal)
    ennemi_liste.append(ennemi)


def ennemi_deplacement():
    """Tous les déplacements de tous les ennemis"""
    for ennemi in ennemi_liste:
        if not ennemi[5]:  # sens de mouvement normal
            if ennemi[0] > ecran_bord:
                if last_scroll < scroll:
                    ennemi[0] -= plvitesse_mouv
                if last_scroll > scroll:
                    ennemi[0] += plvitesse_mouv
            elif last_scroll > scroll:
                ennemi[0] -= (ennemi_vitesse_mouv - plvitesse_mouv)
            elif last_scroll < scroll:
                ennemi[0] -= (ennemi_vitesse_mouv + plvitesse_mouv)
            else:
                ennemi[0] -= ennemi_vitesse_mouv
        else:
            if last_scroll > scroll:
                ennemi[0] += (ennemi_vitesse_mouv + plvitesse_mouv)
            elif last_scroll < scroll:
                ennemi[0] += (ennemi_vitesse_mouv - plvitesse_mouv)
            else:
                ennemi[0] += ennemi_vitesse_mouv

        if not ennemi[4]:  # reste pas sur plateforme
            ennemi_movement_y(ennemi)
        else:
            check_mouv_dg_ennemi(ennemi)


def ennemi_movement_y(ennemi):
    """Pour savoir si un ennemi doit descendre"""
    global floor_base
    for plateforme in plateforme_liste:
        if ennemi[1] + taille_ennemi_y <= plateforme[1] and ennemi[0] + taille_ennemi_x > plateforme[0] and \
                ennemi[0] < plateforme[0] + taille_plateforme:
            ennemi[2] = plateforme[1]
            ennemi_fall(ennemi)
            return
        else:
            ennemi[2] = floor_base
    if (ennemi[1] + taille_ennemi_y) != ennemi[2]:
        ennemi_fall(ennemi)
    return


def ennemi_fall(ennemi):
    """Pour faire descendre un ennemi"""
    if ennemi[1] + taille_ennemi_y + ennemi_vitesse_mouv_bas < ennemi[2]:
        ennemi[1] += ennemi_vitesse_mouv_bas
    else:
        ennemi[1] = ennemi[2] - taille_ennemi_y


def check_mouv_dg_ennemi(ennemi):
    global taille_ennemi_x, taille_ennemi_y, taille_plateforme
    if not ennemi[5]:
        for plateforme in plateforme_liste:
            if ennemi[1] + taille_ennemi_y == plateforme[1] and \
                    ennemi[0] < plateforme[0] < ennemi[0] + taille_ennemi_x:
                for plateforme2 in plateforme_liste:
                    if ennemi[1] + taille_ennemi_y == plateforme2[1] and \
                            ennemi[0] < plateforme2[0] + taille_plateforme < ennemi[0] + taille_ennemi_x:
                        return
                ennemi[5] = True
                return
    else:
        for plateforme in plateforme_liste:
            if ennemi[1] + taille_ennemi_y == plateforme[1] and ennemi[0] < plateforme[0] + taille_plateforme < \
                        ennemi[0] + taille_ennemi_x:
                for plateforme2 in plateforme_liste:
                    if ennemi[1] + taille_ennemi_y == plateforme2[1] and \
                            ennemi[0] < plateforme2[0] < ennemi[0] + taille_ennemi_x:
                        return
                ennemi[5] = False
                return
    return


def floor_is():
    """Définit le sol du perso à un moment donné, pour savoir si celui-ci doit descendre ou rester à la même hauteur"""
    global floor
    for plateforme in plateforme_liste:
        if perso_y + taille_perso_y <= plateforme[1] and perso_x + taille_perso_x > plateforme[0] and perso_x < \
                plateforme[0] + taille_plateforme:
            floor = plateforme[1]
            return
    floor = 192
    return


def ennemi_projectile():
    """Création de projectile """
    global projectile_liste
    if (pyxel.frame_count % 25) == 0:
        for ennemi in ennemi_liste:
            if ennemi[3] == 1:
                milieu_ennemi = taille_ennemi_y // 2
                milieu_projectile = taille_projectile_y // 2
                projectile_liste.append(
                    [ennemi[0] - taille_projectile_x, ennemi[1] + milieu_ennemi - milieu_projectile])


def projectile_deplacement():
    """Update le déplacement des projectiles"""
    global projectile_liste
    for projectile in projectile_liste:
        if projectile[0] < 0:
            projectile_liste.remove(projectile)
        if last_scroll > scroll:
            projectile[0] += (projectile_vitesse - plvitesse_mouv)
        elif last_scroll < scroll:
            projectile[0] -= (projectile_vitesse + plvitesse_mouv)
        else:
            projectile[0] -= projectile_vitesse


def reset():
    """Remettre les variables à leur valeur de base"""
    global perso_x, perso_y, jump, monte, descente, scroll, continuous_scroll, floor, last_floor, \
        last_scroll, vie, ennemi_liste, ennemi_vitesse_mouv, projectile_vitesse, projectile_liste, background, points,\
        fleur_liste, last_perso_x, arbre_liste, buisson_liste
    perso_x = 128
    perso_y = 182
    jump = False
    monte = False
    descente = False
    scroll = 0
    continuous_scroll = 0
    floor = 190
    last_floor = floor
    last_scroll = scroll
    vie = 3
    ennemi_liste = []
    ennemi_vitesse_mouv = 1
    projectile_vitesse = ennemi_vitesse_mouv_initial
    projectile_liste = []
    background = 0
    points = 0
    fleur_liste = [] # à enlever quand les fleurs seront presente dans tous les niveaux
    last_perso_x = perso_x
    arbre_liste = [[ecran_bord, 20], [ecran_bord, 100], [ecran_bord, 200], [ecran_bord, 260], [ecran_bord, 280],
                   [ecran_bord, 340], [ecran_bord, 380], [ecran_bord, 450], [ecran_bord, 490]]
    buisson_liste = [[ecran_bord, 40], [ecran_bord, 135], [ecran_bord, 145], [ecran_bord, 240], [ecran_bord, 300],
                     [ecran_bord, 410], [ecran_bord, 470]]


def update():
    """Mise à jour des variables (30 fois par seconde)"""

    global scroll, last_scroll, plateforme_liste, floor, playing, continuous_scroll, taille_ennemi_y, vie, \
        niveau, compteur, ennemi_vitesse_mouv, projectile_vitesse, fleur_liste, arbre_liste, buisson_liste, star1, \
        star2, star3, regular_points, tuto
        
    # boutons toujours utilisable
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_N):
        playing = 4
        pyxel.play(1, 63)

    if pyxel.btnp(pyxel.KEY_F):
        print("here",pyxel.play_pos(0))

    if playing == 0:
        if pyxel.btn(pyxel.KEY_S):
            playing = 1
            niveau = 1
            tuto = True 

    if playing == 3:
        compteur = 0
        vie = 3
        if pyxel.btnp(pyxel.KEY_R):
            playing = 1

    if playing == 1:
        if niveau == 1:
            if compteur == 0:
                song = pyxel.play_pos(0)
                pos_tic = round(((song[0] * 48 + song[1])/4)*120)
                pyxel.playm(0, tick=pos_tic, loop=True)
                reset()
                plateforme_liste = [[ecran_bord, hauteur_1, 1], [ecran_bord, hauteur_1, 3], [ecran_bord, hauteur_1, 5],
                                    [ecran_bord, hauteur_1, 16], [ecran_bord, hauteur_1, 18],
                                    [ecran_bord, hauteur_1, 20],
                                    [ecran_bord, hauteur_2, 25], [ecran_bord, hauteur_2, 27],
                                    [ecran_bord, hauteur_2, 29],
                                    [ecran_bord, hauteur_1, 29], [ecran_bord, hauteur_1, 31],
                                    [ecran_bord, hauteur_1, 33],
                                    [ecran_bord, hauteur_1, 35], [ecran_bord, hauteur_1, 37],
                                    [ecran_bord, hauteur_1, 39],
                                    [ecran_bord, hauteur_3, 45], [ecran_bord, hauteur_3, 47],
                                    [ecran_bord, hauteur_3, 49],
                                    [ecran_bord, hauteur_2, 60], [ecran_bord, hauteur_2, 62],
                                    [ecran_bord, hauteur_2, 64],
                                    [ecran_bord, hauteur_1, 80], [ecran_bord, hauteur_1, 82],
                                    [ecran_bord, hauteur_1, 84],
                                    [ecran_bord, hauteur_1, 86], [ecran_bord, hauteur_1, 88],
                                    [ecran_bord, hauteur_1, 90],
                                    [ecran_bord, hauteur_2, 98], [ecran_bord, hauteur_2, 100],
                                    [ecran_bord, hauteur_2, 102],
                                    [ecran_bord, hauteur_2, 104], [ecran_bord, hauteur_2, 118],
                                    [ecran_bord, hauteur_2, 120],
                                    [ecran_bord, hauteur_1, 128], [ecran_bord, hauteur_1, 130],
                                    [ecran_bord, hauteur_1, 132],
                                    [ecran_bord, hauteur_1, 134], [ecran_bord, hauteur_1, 136],
                                    [ecran_bord, hauteur_1, 138],
                                    [ecran_bord, hauteur_1, 146], [ecran_bord, hauteur_1, 148],
                                    [ecran_bord, hauteur_1, 150],
                                    [ecran_bord, hauteur_3, 156], [ecran_bord, hauteur_3, 158],
                                    [ecran_bord, hauteur_3, 160],
                                    [ecran_bord, hauteur_2, 170], [ecran_bord, hauteur_2, 172],
                                    [ecran_bord, hauteur_2, 174],
                                    [ecran_bord, hauteur_1, 178], [ecran_bord, hauteur_1, 180],
                                    [ecran_bord, hauteur_1, 182],
                                    [ecran_bord, hauteur_3, 196], [ecran_bord, hauteur_3, 198],
                                    [ecran_bord, hauteur_3, 200],
                                    [ecran_bord, hauteur_2, 210], [ecran_bord, hauteur_2, 212],
                                    [ecran_bord, hauteur_2, 214],
                                    [ecran_bord, hauteur_2, 216], [ecran_bord, hauteur_2, 218],
                                    [ecran_bord, hauteur_2, 220],
                                    [ecran_bord, hauteur_1, 234], [ecran_bord, hauteur_1, 236],
                                    [ecran_bord, hauteur_1, 238],
                                    [ecran_bord, hauteur_1, 240], [ecran_bord, hauteur_1, 242],
                                    [ecran_bord, hauteur_1, 244]]
                # dans plateforme_liste [x, y, scroll d'apparition] qui utilise deux hauteurs y différentes et
                # toujours le même bord x
                fleur_liste = [[ecran_bord, hauteur_3_fleur, 47], [ecran_bord, hauteur_0_fleur, 60],
                               [ecran_bord, hauteur_2_fleur, 118], [ecran_bord, hauteur_3_fleur, 159],
                               [ecran_bord, hauteur_2_fleur, 220], [ecran_bord, hauteur_1_fleur, 243]]
                star3 = len(fleur_liste) * regular_points
                star2 = round((len(fleur_liste) * regular_points) * 0.66)
                star1 = round((len(fleur_liste) * regular_points) * 0.33)
                # dans fleur_liste [x, y, scroll d'apparition]
                compteur += 1

                #  ennemi_creation(y, ennemi_floor, projectile, reste_sur_plateforme)
            if (continuous_scroll == 20 or continuous_scroll == 60 or continuous_scroll == 240) and \
                    last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, False,
                                False)  # création d'ennemi au sol normal sans projectile
            if continuous_scroll == 138 and last_scroll != scroll:
                ennemi_creation(hauteur_1 - taille_ennemi_y, hauteur_1, False,
                                True)  # création d'ennemi à la hauteur 1 sans projectile
            if continuous_scroll == 100 and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False,
                                False)  # création d'ennemi à la hauteur 2 sans projectile

            if scroll >= 290:
                playing = 2
                pyxel.play(1, 63)

        if niveau == 2:
            if compteur == 0:
                song = pyxel.play_pos(0)
                pos_tic = round(((song[0] * 48 + song[1])/4)*120)
                pyxel.playm(0,tick=pos_tic, loop=True)
                reset()
                plateforme_liste = [[200, hauteur_1, 0], [202, hauteur_1, 0], [204, hauteur_1, 0],
                                    [ecran_bord, hauteur_1, 10], [ecran_bord, hauteur_1, 12],
                                    [ecran_bord, hauteur_1, 14],
                                    [ecran_bord, hauteur_1, 16], [ecran_bord, hauteur_1, 18],
                                    [ecran_bord, hauteur_2, 25],
                                    [ecran_bord, hauteur_2, 27], [ecran_bord, hauteur_2, 29],
                                    [ecran_bord, hauteur_1, 41], [ecran_bord, hauteur_1, 43],
                                    [ecran_bord, hauteur_1, 45],
                                    [ecran_bord, hauteur_3, 54], [ecran_bord, hauteur_3, 56],
                                    [ecran_bord, hauteur_3, 58],
                                    [ecran_bord, hauteur_2, 74], [ecran_bord, hauteur_2, 76],
                                    [ecran_bord, hauteur_2, 78], [ecran_bord, hauteur_2, 80],
                                    [ecran_bord, hauteur_2, 96],
                                    [ecran_bord, hauteur_2, 98],
                                    [ecran_bord, hauteur_3, 104], [ecran_bord, hauteur_3, 106],
                                    [ecran_bord, hauteur_3, 108],
                                    [ecran_bord, hauteur_1, 124],
                                    [ecran_bord, hauteur_1, 126],
                                    [ecran_bord, hauteur_1, 128], [ecran_bord, hauteur_1, 130],
                                    [ecran_bord, hauteur_1, 132],
                                    [ecran_bord, hauteur_2, 138],
                                    [ecran_bord, hauteur_2, 140],
                                    [ecran_bord, hauteur_2, 142], [ecran_bord, hauteur_2, 144],
                                    [ecran_bord, hauteur_2, 146],
                                    [ecran_bord, hauteur_3, 154], [ecran_bord, hauteur_3, 156],
                                    [ecran_bord, hauteur_3, 158],
                                    [ecran_bord, hauteur_1, 164], [ecran_bord, hauteur_1, 166],
                                    [ecran_bord, hauteur_1, 168],
                                    [ecran_bord, hauteur_1, 180], [ecran_bord, hauteur_1, 182],
                                    [ecran_bord, hauteur_1, 184],
                                    [ecran_bord, hauteur_3, 188],
                                    [ecran_bord, hauteur_3, 190],
                                    [ecran_bord, hauteur_1, 200], [ecran_bord, hauteur_1, 202],
                                    [ecran_bord, hauteur_1, 204],
                                    [ecran_bord, hauteur_1, 216],
                                    [ecran_bord, hauteur_1, 218],
                                    [ecran_bord, hauteur_1, 220],
                                    [ecran_bord, hauteur_1, 222],
                                    [ecran_bord, hauteur_1, 232], [ecran_bord, hauteur_1, 234],
                                    [ecran_bord, hauteur_1, 236],
                                    [ecran_bord, hauteur_1, 238],
                                    [ecran_bord, hauteur_1, 254],
                                    [ecran_bord, hauteur_1, 256],
                                    [ecran_bord, hauteur_1, 258],
                                    [ecran_bord, hauteur_3, 276],
                                    [ecran_bord, hauteur_3, 278], [ecran_bord, hauteur_3, 280],
                                    [ecran_bord, hauteur_3, 282],
                                    [ecran_bord, hauteur_2, 290], [ecran_bord, hauteur_2, 292],
                                    [ecran_bord, hauteur_2, 294],
                                    [ecran_bord, hauteur_1, 302], [ecran_bord, hauteur_1, 304],
                                    [ecran_bord, hauteur_1, 306],
                                    [ecran_bord, hauteur_2, 316], [ecran_bord, hauteur_2, 318],
                                    [ecran_bord, hauteur_2, 320],
                                    [ecran_bord, hauteur_1, 332], [ecran_bord, hauteur_1, 334],
                                    [ecran_bord, hauteur_1, 336]]
                # dans plateforme_liste [x, y, scroll d'apparition] qui utilise deux hauteurs y différentes et
                # toujours le même bord x
                fleur_liste = [[203, hauteur_1_fleur, 0], [ecran_bord, hauteur_2_fleur, 27],
                               [ecran_bord, hauteur_2_fleur, 97], [ecran_bord, hauteur_2_fleur, 140],
                               [ecran_bord, hauteur_3_fleur, 190], [ecran_bord, hauteur_1_fleur, 236],
                               [ecran_bord, hauteur_2_fleur, 318]]
                star3 = len(fleur_liste) * regular_points
                star2 = round((len(fleur_liste) * regular_points) * 0.66)
                star1 = round((len(fleur_liste) * regular_points) * 0.33)
                ennemi_vitesse_mouv += 0.5

                projectile_vitesse = ennemi_vitesse_mouv + 1
                compteur += 1

            if (continuous_scroll == 14 or continuous_scroll == 50 or continuous_scroll == 90 or
                    continuous_scroll == 200 or continuous_scroll == 230 or continuous_scroll == 249 or
                    continuous_scroll == 290) and last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, False, False)
            if (continuous_scroll == 41 or continuous_scroll == 180 or continuous_scroll == 302) and \
                    last_scroll != scroll:
                ennemi_creation(hauteur_1 - taille_ennemi_y, hauteur_1, False, True)
            if (continuous_scroll == 29 or continuous_scroll == 138) and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False, False)
            if scroll >= 400:
                playing = 2
                pyxel.play(1, 63)

        if niveau == 3:
            if compteur == 0:
                song = pyxel.play_pos(0)
                pos_tic = round(((song[0] * 48 + song[1]) / 4) * 120)
                pyxel.playm(0, tick=pos_tic, loop=True)
                reset()
                plateforme_liste = [[ecran_bord, hauteur_1, 4], [ecran_bord, hauteur_1, 6],
                                    [ecran_bord, hauteur_1, 8], [ecran_bord, hauteur_1, 10],
                                    [ecran_bord, hauteur_1, 12], [ecran_bord, hauteur_1, 14],
                                    [ecran_bord, hauteur_1, 16],
                                    [ecran_bord, hauteur_2, 25],
                                    [ecran_bord, hauteur_2, 27], [ecran_bord, hauteur_2, 29],
                                    [ecran_bord, hauteur_1, 35], [ecran_bord, hauteur_1, 37],
                                    [ecran_bord, hauteur_1, 39],
                                    [ecran_bord, hauteur_3, 46], [ecran_bord, hauteur_3, 48],
                                    [ecran_bord, hauteur_3, 50],
                                    [ecran_bord, hauteur_1, 58], [ecran_bord, hauteur_1, 60],
                                    [ecran_bord, hauteur_2, 70], [ecran_bord, hauteur_2, 72],
                                    [ecran_bord, hauteur_2, 74], [ecran_bord, hauteur_2, 76],
                                    [ecran_bord, hauteur_2, 78], [ecran_bord, hauteur_2, 80],
                                    [ecran_bord, hauteur_3, 92], [ecran_bord, hauteur_3, 94],
                                    [ecran_bord, hauteur_3, 96], [ecran_bord, hauteur_3, 98],
                                    [ecran_bord, hauteur_1, 106], [ecran_bord, hauteur_1, 108],
                                    [ecran_bord, hauteur_2, 116], [ecran_bord, hauteur_2, 118],
                                    [ecran_bord, hauteur_2, 120], [ecran_bord, hauteur_2, 122],
                                    [ecran_bord, hauteur_1, 136], [ecran_bord, hauteur_1, 138],
                                    [ecran_bord, hauteur_1, 140], [ecran_bord, hauteur_1, 142],
                                    [ecran_bord, hauteur_3, 150], [ecran_bord, hauteur_3, 152],
                                    [ecran_bord, hauteur_3, 154], [ecran_bord, hauteur_3, 156],
                                    [ecran_bord, hauteur_3, 158], [ecran_bord, hauteur_3, 160],
                                    [ecran_bord, hauteur_1, 170], [ecran_bord, hauteur_1, 172],
                                    [ecran_bord, hauteur_1, 174], [ecran_bord, hauteur_1, 176],
                                    [ecran_bord, hauteur_1, 178], [ecran_bord, hauteur_3, 190],
                                    [ecran_bord, hauteur_3, 192], [ecran_bord, hauteur_3, 194],
                                    [ecran_bord, hauteur_3, 196], [ecran_bord, hauteur_3, 198],
                                    [ecran_bord, hauteur_3, 200], [ecran_bord, hauteur_3, 202],
                                    [ecran_bord, hauteur_1, 214], [ecran_bord, hauteur_1, 216],
                                    [ecran_bord, hauteur_1, 218], [ecran_bord, hauteur_1, 220],
                                    [ecran_bord, hauteur_2, 232], [ecran_bord, hauteur_2, 234],
                                    [ecran_bord, hauteur_2, 236], [ecran_bord, hauteur_2, 238],
                                    [ecran_bord, hauteur_2, 240], [ecran_bord, hauteur_2, 242],
                                    [ecran_bord, hauteur_2, 244], [ecran_bord, hauteur_2, 246],
                                    [ecran_bord, hauteur_2, 248], [ecran_bord, hauteur_2, 250],
                                    [ecran_bord, hauteur_1, 256], [ecran_bord, hauteur_1, 258],
                                    [ecran_bord, hauteur_1, 260], [ecran_bord, hauteur_1, 262],
                                    [ecran_bord, hauteur_3, 274], [ecran_bord, hauteur_3, 276],
                                    [ecran_bord, hauteur_3, 278], [ecran_bord, hauteur_3, 298],
                                    [ecran_bord, hauteur_3, 300], [ecran_bord, hauteur_3, 302],
                                    [ecran_bord, hauteur_1, 314], [ecran_bord, hauteur_1, 316],
                                    [ecran_bord, hauteur_1, 318], [ecran_bord, hauteur_1, 320],
                                    [ecran_bord, hauteur_1, 333], [ecran_bord, hauteur_1, 335],
                                    [ecran_bord, hauteur_1, 337], [ecran_bord, hauteur_3, 346],
                                    [ecran_bord, hauteur_3, 348], [ecran_bord, hauteur_3, 350],
                                    [ecran_bord, hauteur_3, 352], [ecran_bord, hauteur_2, 364],
                                    [ecran_bord, hauteur_2, 366], [ecran_bord, hauteur_2, 368],
                                    [ecran_bord, hauteur_2, 370], [ecran_bord, hauteur_2, 372],
                                    [ecran_bord, hauteur_2, 386], [ecran_bord, hauteur_2, 388],
                                    [ecran_bord, hauteur_2, 390],
                                    [ecran_bord, hauteur_3, 400], [ecran_bord, hauteur_3, 402],
                                    [ecran_bord, hauteur_3, 404], [ecran_bord, hauteur_3, 406],
                                    [ecran_bord, hauteur_3, 408],
                                    [ecran_bord, hauteur_3, 410], [ecran_bord, hauteur_3, 412],
                                    [ecran_bord, hauteur_3, 414], [ecran_bord, hauteur_1, 428],
                                    [ecran_bord, hauteur_1, 430], [ecran_bord, hauteur_1, 432],
                                    [ecran_bord, hauteur_1, 434],
                                    [ecran_bord, hauteur_2, 448],
                                    [ecran_bord, hauteur_2, 450], [ecran_bord, hauteur_2, 452],
                                    [ecran_bord, hauteur_2, 454], [ecran_bord, hauteur_2, 456],
                                    [ecran_bord, hauteur_2, 458], [ecran_bord, hauteur_2, 460],
                                    [ecran_bord, hauteur_1, 469], [ecran_bord, hauteur_1, 471],
                                    [ecran_bord, hauteur_1, 473], [ecran_bord, hauteur_1, 475],
                                    [ecran_bord, hauteur_3, 486], [ecran_bord, hauteur_3, 488],
                                    [ecran_bord, hauteur_2, 500], [ecran_bord, hauteur_2, 502],
                                    [ecran_bord, hauteur_2, 504], [ecran_bord, hauteur_2, 506],
                                    [ecran_bord, hauteur_3, 518],
                                    [ecran_bord, hauteur_3, 520], [ecran_bord, hauteur_3, 522],
                                    [ecran_bord, hauteur_3, 524], [ecran_bord, hauteur_3, 526],
                                    [ecran_bord, hauteur_3, 546], [ecran_bord, hauteur_3, 548],
                                    [ecran_bord, hauteur_3, 550], [ecran_bord, hauteur_3, 552],
                                    [ecran_bord, hauteur_1, 568], [ecran_bord, hauteur_1, 570],
                                    [ecran_bord, hauteur_1, 572], [ecran_bord, hauteur_1, 574],
                                    [ecran_bord, hauteur_2, 582], [ecran_bord, hauteur_2, 584],
                                    [ecran_bord, hauteur_2, 586],
                                    [ecran_bord, hauteur_2, 588], [ecran_bord, hauteur_2, 590],
                                    [ecran_bord, hauteur_3, 602], [ecran_bord, hauteur_3, 604],
                                    [ecran_bord, hauteur_3, 606], [ecran_bord, hauteur_3, 608],
                                    [ecran_bord, hauteur_3, 622], [ecran_bord, hauteur_3, 624],
                                    [ecran_bord, hauteur_3, 626], [ecran_bord, hauteur_3, 640],
                                    [ecran_bord, hauteur_3, 642], [ecran_bord, hauteur_3, 644],
                                    [ecran_bord, hauteur_3, 646], [ecran_bord, hauteur_3, 664],
                                    [ecran_bord, hauteur_3, 666], [ecran_bord, hauteur_3, 668],
                                    [ecran_bord, hauteur_1, 680], [ecran_bord, hauteur_1, 682],
                                    [ecran_bord, hauteur_1, 684], [ecran_bord, hauteur_1, 686], ]
                # dans plateforme_liste [x, y, scroll d'apparition] qui utilise deux hauteurs y différentes et
                # toujours le même bord x
                fleur_liste = [[ecran_bord, hauteur_3_fleur, 50], [ecran_bord, hauteur_3_fleur, 152],
                            [ecran_bord, hauteur_0_fleur, 172], [ecran_bord, hauteur_2_fleur, 234],
                            [ecran_bord, hauteur_3_fleur, 300], [ecran_bord, hauteur_0_fleur, 378],
                            [ecran_bord, hauteur_1_fleur, 432], [ecran_bord, hauteur_3_fleur, 520],
                            [ecran_bord, hauteur_3_fleur, 624], [ecran_bord, hauteur_1_fleur, 685], ]
                ennemi_vitesse_mouv += 0.5
                projectile_vitesse = ennemi_vitesse_mouv + 1
                compteur += 1
            if (continuous_scroll == 14 or continuous_scroll == 80 or continuous_scroll == 130 or continuous_scroll == 210 or continuous_scroll == 368 or continuous_scroll == 450 or continuous_scroll == 607 or continuous_scroll == 677) and last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, True, False)
            if (continuous_scroll == 27 or continuous_scroll == 390 or continuous_scroll == 590) and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False, False)
            if (continuous_scroll == 118 or continuous_scroll == 240 or continuous_scroll == 458) and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False, True)
            if (continuous_scroll == 96 or continuous_scroll == 200 or continuous_scroll == 302 or continuous_scroll == 408 or continuous_scroll == 642) and last_scroll != scroll:
                ennemi_creation(hauteur_3 - taille_ennemi_y, hauteur_3, True, True)
            if scroll >= 750:
                playing = 2
                pyxel.play(1, 63)
        perso_deplacement()

        if last_scroll != scroll:
            plateforme_deplacement()
            deplacement_avec_plateforme(fleur_liste)
            deplacement_avec_plateforme_deco(arbre_liste)
            deplacement_avec_plateforme_deco(buisson_liste)

        ennemi_deplacement()
        floor_is()
        ennemi_projectile()
        projectile_deplacement()

    if playing == 2:
        compteur = 0
        if pyxel.btnp(pyxel.KEY_S) and niveau < 3:
            niveau += 1
            playing = 1

    if playing == 4:
        compteur = 0
        if pyxel.btnp(pyxel.KEY_1):
            niveau = 1
            playing = 1
        if pyxel.btnp(pyxel.KEY_2):
            niveau = 2
            playing = 1
        if pyxel.btnp(pyxel.KEY_3):
            niveau = 3
            playing = 1

    if vie <= 0:
        pyxel.play(1,7)
        playing = 3


def draw():
    """Création des objets (30 fois par seconde)"""
    global background, floor, compteur_animation_1, compteur_animation_2, touche, tuto
    pyxel.cls(0)
    if playing == 0:  # écran d'intro
        pyxel.text(84, 160, "press S to start level 1", 7)
        pyxel.text(101, 230, "press Q to quit", 11)
        pyxel.text(82, 15, "press N to choose a level", 11)
        pyxel.text(75, 245, "credits: Alis, Sophia, Nicole", 3)
        pyxel.blt(89, 100, 0, 0, 48, 80, 32)

    if playing == 1:  # écran quand on joue
        if compteur != 0:
            background += 0.5
            if background >= 256:
                background = 0
            pyxel.bltm(0, 0, 0, background, 0, 256, floor_base)
            pyxel.bltm(0, floor_base, 0, 0, floor_base, 256, 66)
            for arbre in arbre_liste:
                pyxel.blt(arbre[0], floor_base-32, 0, 73, 0, 35, 32, 6)
            for buisson in buisson_liste:
                pyxel.blt(buisson[0], floor_base-8, 0, 73, 0, -35, 8, 6)
            if touche:
                pyxel.blt(perso_x, perso_y, 0, 68, 34, taille_perso_x, taille_perso_y, 0)
                if (pyxel.frame_count % 8) == 0:
                    touche = False
            elif last_perso_x > perso_x or last_scroll > scroll: # donc qui diminue
                if (pyxel.frame_count % 4) == 0:
                    compteur_animation_1 = not compteur_animation_1
                if compteur_animation_1:
                    pyxel.blt(perso_x, perso_y, 0, 100, 34, -taille_perso_x, taille_perso_y, 0)
                else:
                    pyxel.blt(perso_x, perso_y, 0, 84, 34, -taille_perso_x, taille_perso_y, 0)
            elif last_perso_x < perso_x or last_scroll < scroll:
                if (pyxel.frame_count % 4) == 0:
                    compteur_animation_2 = not compteur_animation_2
                if compteur_animation_2:
                    pyxel.blt(perso_x, perso_y, 0, 100, 34, taille_perso_x, taille_perso_y, 0)
                else:
                    pyxel.blt(perso_x, perso_y, 0, 84, 34, taille_perso_x, taille_perso_y, 0)
            else:
                pyxel.blt(perso_x, perso_y, 0, 20, 26, taille_perso_x, taille_perso_y, 0)
            for plateforme in plateforme_liste:
                if plateforme[2] <= scroll:
                    pyxel.blt(plateforme[0], plateforme[1], 0, 16, 8, taille_plateforme, taille_plateforme)
            for fleur in fleur_liste:
                if fleur[2] <= scroll:
                    pyxel.blt(fleur[0], fleur[1],0,85,53, taille_fleur_x, taille_fleur_y,0)
            for ennemi in ennemi_liste:
                if not ennemi[5]:
                    pyxel.blt(ennemi[0], ennemi[1], 0, 34, 27, taille_ennemi_x, taille_ennemi_y, 0)
                else:
                    pyxel.blt(ennemi[0], ennemi[1], 0, 34, 27, -taille_ennemi_x, taille_ennemi_y, 0)
            for projectile in projectile_liste:
                pyxel.blt(projectile[0], projectile[1], 0, 101, 54, taille_projectile_x, taille_projectile_y, 0)
            pyxel.text(215,20,str(points),9)
            pyxel.blt(205,19, 0, 85, 53, taille_fleur_x, taille_fleur_y,0)

            if vie >= 1:
                pyxel.blt(15, 20, 0, 29, 6, 6, 5, 0)
                if vie >= 2:
                    pyxel.blt(25, 20, 0, 29, 6, 6, 5, 0)
                    if vie == 3:
                        pyxel.blt(35, 20, 0, 29, 6, 6, 5, 0)
                    else:
                        pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)
                else:
                    pyxel.blt(25, 20, 0, 45, 6, 6, 5, 0)
                    pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)
    if tuto:
        pyxel.text(86, 70, "press space to jump", 0)
        pyxel.text(56, 80, "and use the arrows to go right or left", 0)

    if playing == 2:  # écran qui s'affiche quand on gagne
        pyxel.text(108, 142, "with", 9)
        pyxel.text(138, 142, str(points), 9)
        pyxel.blt(128, 140, 0, 85, 53, taille_fleur_x, taille_fleur_y, 0)
        pyxel.blt(90, 100, 0, 16, 96, 80, 32, 0)
        pyxel.text(77, 185, "press N to pick a new level", 9)
        pyxel.text(101, 230, "press Q to quit", 10)

        if points >= round(star1/2):
            if points >= star1:
                pyxel.blt(60, 30, 0, 118, 0, 36, 35, 0)
            else:
                pyxel.blt(60, 30, 0, 166, 40, 36, 35, 0)
        else:
            pyxel.blt(60, 30, 0, 166, 0, 36, 35, 0)

        if points >= round((star1+star2)/2):
            if points >= star2:
                pyxel.blt(110, 30, 0, 118, 0, 36, 35, 0)
            else:
                pyxel.blt(110, 30, 0, 166, 40, 36, 35, 0)
        else:
            pyxel.blt(110, 30, 0, 166, 0, 36, 35, 0)

        if points >= round((star2+star3)/2):
            if points+1 >= star3:
                pyxel.blt(160, 30, 0, 118, 0, 36, 35, 0)
            else:
                pyxel.blt(160, 30, 0, 166, 40, 36, 35, 0)
        else:
            pyxel.blt(160, 30, 0, 166, 0, 36, 35, 0)

        if niveau < 3:
            pyxel.text(70, 195, "press S to start the next level", 9)
        else:
            pyxel.text(55, 200, "You completed the last and hardest level", 10)

    if playing == 3:  # écran qui s'affiche quand on perd
        pyxel.blt(87, 100, 0, 0, 136, 80, 32, 0)
        pyxel.text(92, 180, "press R to restart", 8)

    if playing == 4:  # menu pour choisir un niveau
        pyxel.text(86, 100, "press 1 to start level 1", 11)
        pyxel.text(86, 115, "press 2 to start level 2", 11)
        pyxel.text(86, 130, "press 3 to start level 3", 11)



pyxel.run(update, draw)
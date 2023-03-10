import pyxel

pyxel.init(256, 256, title="Tiny Adventurer")
pyxel.load("art1_(3).pyxres")

# personage
perso_x = 128
perso_y = 182
taille_perso_x = 8
taille_perso_y = 13

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
floor = 190  # le "sol" du personnage sur lequel il est ou atterrit toujours,
# change si le personnage est au-dessus d'une plateforme
last_floor = floor  # permet de savoir si le "sol" du personnage change au cours de l'action
last_scroll = scroll  # permet de savoir si et comment le scroll (avancement dans le niveau) change au cours de l'action
vie = 3
niveau = 0
compteur = 0  # pour initialiser une seule fois les variables au début du niveau

# plateforme
hauteur_1 = 140
hauteur_3 = 115
hauteur_2 = 90
# 2 hauteurs fixent pour les plateformes
plateforme_liste = []
taille_plateforme = 8
plvitesse_mouv = pvitesse_mouv_dg  # vitesse de mouvement des plateformes

# ennemi
ennemi_liste = []
taille_ennemi_y = 4
taille_ennemi_x = 4
ennemi_vitesse_mouv = 1
ennemi_vitesse_mouv_initial = ennemi_vitesse_mouv  # pour pouvoir facilement réinitialisé la vitesse de mouvement
# en début de niveau
ennemi_floor_base = floor  # "sol" toujours égal à la même valeur (pas comme floor qui dépend du personnage)
ennemi_vitesse_mouv_bas = 8

# projectile ennemi
projectile_liste = []
taille_projectile_x = 5
taille_projectile_y = 2
projectile_vitesse = ennemi_vitesse_mouv + 1

pyxel.playm(0, loop=True)


def perso_deplacement():
    """Déplacement du personnage"""
    global perso_x, perso_y, jump, scroll, last_scroll, last_floor, monte, descente, \
        continuous_scroll, vie, ennemi_liste
    last_scroll = scroll
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
    return


def contact():
    """Savoir s'il y a contact entre l'ennemi et le personnage"""
    global vie
    for ennemi in ennemi_liste:
        if perso_y < ennemi[1] + taille_ennemi_y and perso_y + taille_perso_y > ennemi[1] \
                and perso_x + taille_perso_x > ennemi[0] and perso_x < ennemi[0] + taille_ennemi_x:
            vie -= 1
            ennemi_liste.remove(ennemi)
    for projectile in projectile_liste:
        if perso_y < projectile[1] + taille_projectile_y and perso_y + taille_perso_y > projectile[1] \
                and perso_x + taille_perso_x > projectile[0] and perso_x < projectile[0] + taille_projectile_x:
            vie -= 1
            projectile_liste.remove(projectile)
    return


def plateforme_deplacement():
    """Déplacement des plateformes"""
    if last_scroll > scroll:
        for plateforme in plateforme_liste:
            if plateforme[2] < scroll:
                plateforme[0] += plvitesse_mouv
        return plateforme_liste
    if last_scroll < scroll:
        for plateforme in plateforme_liste:
            if plateforme[2] < scroll:
                plateforme[0] -= plvitesse_mouv
        return plateforme_liste
    return plateforme_liste


def ennemi_creation(y, ennemi_floor, projectile, reste_sur_plateforme):
    """Création d'ennemi dependant un niveau"""
    global ecran_bord
    # dans ennemi_liste: x l'ennemi, y l'ennemi, le sol de l'ennemi, projectile ou non?, reste sur plateforme ou non?
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
        if ennemi[0] < 0:
            ennemi_liste.remove(ennemi)

        if not ennemi[5]:
            if last_scroll > scroll:
                ennemi[0] += (ennemi_vitesse_mouv - plvitesse_mouv)
            elif last_scroll < scroll:
                ennemi[0] -= (ennemi_vitesse_mouv + plvitesse_mouv)
            else:
                ennemi[0] -= ennemi_vitesse_mouv
        else:
            if last_scroll > scroll:
                ennemi[0] -= (ennemi_vitesse_mouv + plvitesse_mouv)
            elif last_scroll < scroll:
                ennemi[0] += (-ennemi_vitesse_mouv + plvitesse_mouv)
            else:
                ennemi[0] += ennemi_vitesse_mouv
        if not ennemi[4]:
            ennemi_movement_y(ennemi)
        else:
            check_mouv_dg_ennemi(ennemi)


def ennemi_movement_y(ennemi):
    """Pour savoir si un ennemi doit descendre"""
    global ennemi_floor_base
    for plateforme in plateforme_liste:
        if ennemi[1] + taille_ennemi_y <= plateforme[1] and ennemi[0] + taille_ennemi_x > plateforme[0] and \
                ennemi[0] < plateforme[0] + taille_plateforme:
            ennemi[2] = plateforme[1]
            ennemi_fall(ennemi)
            return
        else:
            ennemi[2] = ennemi_floor_base
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
    if ennemi[4]:
        for plateforme in plateforme_liste:
            if not ennemi[5]:
                if ennemi[1] + taille_ennemi_y == plateforme[1] and \
                        ennemi[0] < plateforme[0] < ennemi[0] + taille_ennemi_x:
                    for plateforme2 in plateforme_liste:
                        if ennemi[1] + taille_ennemi_y == plateforme2[1] and \
                                ennemi[0] < plateforme2[0] + taille_plateforme < ennemi[0] + taille_ennemi_x:
                            ennemi[5] = False
                            # print(ennemi[0], "good", plateforme[0])
                            return
                    ennemi[5] = True
                    # print(ennemi[0], "good22", plateforme[0])
                    return
            elif ennemi[1] + taille_ennemi_y == plateforme[1] and ennemi[0] < plateforme[0] + taille_plateforme < \
                    ennemi[0] + taille_ennemi_x:
                for plateforme2 in plateforme_liste:
                    if ennemi[1] + taille_ennemi_y == plateforme2[1] and \
                            ennemi[0] < plateforme2[0] < ennemi[0] + taille_ennemi_x:
                        ennemi[5] = True
                        # print(ennemi[0], "hi22", plateforme[0], taille_plateforme, taille_ennemi_x)
                        return
                ennemi[5] = False
                # print(ennemi[0], "hi", plateforme[0], taille_plateforme, taille_ennemi_x)
                return
    else:
        return


def floor_is():
    """Définit le sol du perso à un moment donné, pour savoir si celui-ci doit descendre ou rester à la même hauteur"""
    global floor
    for plateforme in plateforme_liste:
        if perso_y + taille_perso_y <= plateforme[1] and perso_x + taille_perso_x > plateforme[0] and perso_x < \
                plateforme[0] + taille_plateforme:
            floor = plateforme[1]
            return floor
    floor = 190
    return


def ennemi_projectile():
    """Création de projectile toutes les secondes"""
    global projectile_liste
    if (pyxel.frame_count % 30) == 0:
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
        last_scroll, vie, ennemi_liste, ennemi_vitesse_mouv, projectile_vitesse, projectile_liste
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


def update():
    """Mise à jour des variables (30 fois par seconde)"""

    global scroll, last_scroll, plateforme_liste, floor, playing, continuous_scroll, taille_ennemi_y, vie, \
        niveau, compteur, ennemi_vitesse_mouv, projectile_vitesse
    # boutons toujours utilisable
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_N):
        playing = 4

    if playing == 0:
        if pyxel.btn(pyxel.KEY_S):
            playing = 1
            niveau = 1

    if playing == 3:
        compteur = 0
        if pyxel.btnp(pyxel.KEY_R):
            playing = 1

    if playing == 1:
        if niveau == 1:
            if compteur == 0:
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
                                    [ecran_bord, hauteur_2, 138], [ecran_bord, hauteur_2, 140],
                                    [ecran_bord, hauteur_2, 142],
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
                compteur += 1

            #  ennemi_creation(y, ennemi_floor, projectile, reste_sur_plateforme)
            if (continuous_scroll == 20 or continuous_scroll == 60 or continuous_scroll == 240) and last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, False,
                                False)  # création d'ennemi au sol normal sans projectile
            if continuous_scroll == 150 and last_scroll != scroll:
                ennemi_creation(hauteur_1 - taille_ennemi_y, hauteur_1, False,
                                True)  # création d'ennemi à la hauteur 1 sans projectile
            if continuous_scroll == 100 and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False,
                                False)  # création d'ennemi à la hauteur 2 sans projectile

            if scroll >= 280:
                playing = 2

        if niveau == 2:
            if compteur == 0:
                reset()
                plateforme_liste = [[200, hauteur_1, 0], [202, hauteur_1, 0], [204, hauteur_1, 0],
                                    [ecran_bord, hauteur_1, 16], [ecran_bord, hauteur_1, 18],
                                    [ecran_bord, hauteur_1, 20], [ecran_bord, hauteur_2, 25],
                                    [ecran_bord, hauteur_2, 27], [ecran_bord, hauteur_2, 29],
                                    [ecran_bord, hauteur_1, 35], [ecran_bord, hauteur_1, 37],
                                    [ecran_bord, hauteur_1, 39]]
                # dans plateforme_liste [x, y, scroll d'apparition] qui utilise deux hauteurs y différentes et
                # toujours le même bord x
                ennemi_vitesse_mouv += 0.5
                projectile_vitesse = ennemi_vitesse_mouv + 1
                compteur += 1

            if (continuous_scroll == 14 or continuous_scroll == 50) and last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, False, False)
            if continuous_scroll == 39 and last_scroll != scroll:
                ennemi_creation(hauteur_1 - taille_ennemi_y, hauteur_1, False, True)
            if continuous_scroll == 29 and last_scroll != scroll:
                ennemi_creation(hauteur_2 - taille_ennemi_y, hauteur_2, False, False)
            if scroll >= 120:
                playing = 2

        if niveau == 3:
            if compteur == 0:
                reset()
                plateforme_liste = [[ecran_bord, hauteur_1, 1], [ecran_bord, hauteur_1, 3],
                                    [ecran_bord, hauteur_1, 5],
                                    [ecran_bord, hauteur_1, 16], [ecran_bord, hauteur_1, 18],
                                    [ecran_bord, hauteur_1, 20], [ecran_bord, hauteur_2, 25],
                                    [ecran_bord, hauteur_2, 27], [ecran_bord, hauteur_2, 29],
                                    [ecran_bord, hauteur_1, 35], [ecran_bord, hauteur_1, 37],
                                    [ecran_bord, hauteur_1, 39]]
                # dans plateforme_liste [x, y, scroll d'apparition] qui utilise deux hauteurs y différentes et
                # toujours le même bord x
                ennemi_vitesse_mouv += 0.5
                projectile_vitesse = ennemi_vitesse_mouv + 1
                compteur += 1

            if (continuous_scroll == 14 or continuous_scroll == 50) and last_scroll != scroll:
                ennemi_creation(floor - taille_ennemi_y, floor, True, False)
            if continuous_scroll == 39 and last_scroll != scroll:
                ennemi_creation(hauteur_1 - taille_ennemi_y, hauteur_1, True, False)
            if scroll >= 120:
                playing = 2
        perso_deplacement()

        if last_scroll != scroll:
            plateforme_liste = plateforme_deplacement()
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
        playing = 3


def draw():
    """Création des objets (30 fois par seconde)"""
    pyxel.cls(0)
    if playing == 0:  # écran d'intro
        pyxel.text(84, 160, "press S to start level 1", 7)
        pyxel.text(101, 230, "press Q to quit", 11)
        pyxel.text(82, 15, "press N to choose a level", 11)
        pyxel.text(75, 245, "credits: Alis, Sophia, Nicole", 3)
        pyxel.blt(89, 100, 0, 0, 48, 80, 32)

    if playing == 1:  # écran quand on joue
        if compteur != 0:
            pyxel.blt(perso_x, perso_y, 0, 4, 25, taille_perso_x, taille_perso_y, 6)
            for plateforme in plateforme_liste:
                if plateforme[2] <= scroll:
                    pyxel.blt(plateforme[0], plateforme[1], 0, 16, 8, taille_plateforme, taille_plateforme)
            for ennemi in ennemi_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 38, 29, taille_ennemi_x, taille_ennemi_y, 0)
            for projectile in projectile_liste:
                pyxel.rect(projectile[0], projectile[1], taille_projectile_x, taille_projectile_y, 9)

            if vie >= 1:
                pyxel.blt(15, 20, 0, 29, 6, 6, 5, 0)
                if vie >= 2:
                    pyxel.blt(25, 20, 0, 29, 6, 6, 5, 0)
                    if vie == 3:
                        pyxel.blt(35, 20, 0, 29, 6, 6, 5, 0)
                    else : pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)
                else:
                    pyxel.blt(25, 20, 0, 45, 6, 6, 5, 0)
                    pyxel.blt(35, 20, 0, 45, 6, 6, 5, 0)

    if playing == 2:  # écran qui s'affiche quand on gagne
        pyxel.blt(90, 100, 0, 16, 96, 80, 32, 0)
        pyxel.text(77, 165, "press N to pick a new level", 9)
        pyxel.text(101, 230, "press Q to quit", 10)
        if niveau < 3:
            pyxel.text(70, 175, "press S to start the next level", 9)
        else:
            pyxel.text(55, 70, "You completed the last and hardest level", 10)

    if playing == 3:  # écran qui s'affiche quand on perd
        pyxel.blt(87, 100, 0, 0, 136, 80, 32, 0)
        pyxel.text(92, 180, "press R to restart", 8)

    if playing == 4:  # menu pour choisir un niveau
        pyxel.text(86, 100, "press 1 to start level 1", 11)
        pyxel.text(86, 115, "press 2 to start level 2", 11)
        pyxel.text(86, 130, "press 3 to start level 3", 11)


pyxel.run(update, draw)
import pyxel
pyxel.init(256, 256, title="Tiny Adventurer")
perso_x = 128
perso_y = 182
jump= False
i=0
scroll_limitd= 190
scroll_limitg=60
scroll=0
floor=190   
last_scroll=scroll
plateforme_liste=[]
taille_perso=8
taille_plateforme=8
pvitesse_mouv_dg=3
pvitesse_mouv_haut=7
pvitesse_mouv_bas=8
plvitesse_mouv=3


def perso_deplacement(x, y,jump,i,scroll,last_scroll):
    last_scroll=scroll
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < scroll_limitd) :
            x = x + pvitesse_mouv_dg
        else: scroll+= 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > scroll_limitg) :
            x = x - pvitesse_mouv_dg
        elif scroll> 0:
            scroll-= 1
    if pyxel.btn(pyxel.KEY_SPACE):
        jump= True
    if jump == False:
      if y+taille_perso+1< floor:
        y= y + pvitesse_mouv_bas
        if y+taille_perso<taille_plateforme//2+floor and y+taille_perso>taille_plateforme//2+floor:
          y=floor-taille_perso 
    if jump == True:
        if i < 8:
            y= y - pvitesse_mouv_haut
            i= i + 1
        else: 
            if i < 15:
                if y+taille_perso >= floor:
                    y= floor-taille_perso
                    jump= False
                    i=0
                    return x, y,jump,i,scroll,last_scroll
                y= y + pvitesse_mouv_bas
                i+= 1
            else: jump = False
    else: i=0
    return x, y,jump,i,scroll,last_scroll
    
def plateforme_creation(plateforme_liste,x,y):
    plateforme_liste.append([x,y])

def plateforme_deplacement(plaforme_liste):
    if last_scroll>scroll:
        for plateforme in plateforme_liste:
            plateforme[0]+=plvitesse_mouv
            if plateforme[0]>=256:
                plateforme_liste.remove(plateforme) 
        return plateforme_liste
    if last_scroll<scroll:
        for plateforme in plateforme_liste:
            plateforme[0]-=plvitesse_mouv
            if plateforme[0]<=-taille_plateforme:
                plateforme_liste.remove(plateforme) 
        return plateforme_liste    
    return plateforme_liste
            

def floor_is(floor):
  for plateforme in plateforme_liste:
    if perso_y>=plateforme[1] and perso_x+taille_perso>plateforme[0] and perso_x<plateforme[0]+taille_perso:
      floor=plateforme[1]-8
      return floor
  floor=190
  return floor
    
def update(): 
    """mise à jour des variables (30 fois par seconde)"""

    global perso_x, perso_y,jump,i, scroll, last_scroll, plateforme_liste, floor,pvitesse_mouv_dg
    
    perso_x, perso_y,jump,i,scroll,last_scroll = perso_deplacement(perso_x, perso_y,jump,i,scroll,last_scroll)
    if scroll == 1 or scroll == 3 or scroll == 5:
        plateforme_creation(plateforme_liste,230,145)
    if last_scroll != scroll:
      plateforme_liste=plateforme_deplacement(plateforme_liste)
    floor=floor_is(floor)

def draw():
    """création des objets (30 fois par seconde)"""

    pyxel.cls(0)
    pyxel.rect(perso_x, perso_y-taille_perso, taille_perso, taille_perso, 1)
    for plateforme in plateforme_liste:
      pyxel.rect(plateforme[0], plateforme[1], taille_plateforme, taille_plateforme, 8) 

pyxel.run(update, draw)
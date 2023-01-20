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
last_floor=floor
last_scroll=scroll
plateforme_liste=[]
taille_perso=8
taille_plateforme=8
pvitesse_mouv_dg=3
pvitesse_mouv_haut=7
pvitesse_mouv_bas=8
plvitesse_mouv=3
monte=False
descente=False
taille_saut=56
space_appuie=0


def perso_deplacement(x, y,jump,scroll,last_scroll,last_floor,monte,descente):
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
        if jump == False and y+taille_perso==floor:
          last_floor=y+taille_perso
          jump= True
      
    if jump == True:
        if last_floor-taille_saut-taille_perso<=y and descente == False:
            monte=True
        else: 
            if y+taille_perso+pvitesse_mouv_bas >= floor:
                descente=False
                y= floor-taille_perso
                jump= False
                return x, y, jump, scroll, last_scroll, last_floor, monte, descente,
            monte=False
            descente=True
    else:
      if y+taille_perso!= floor:
          if y+taille_perso+pvitesse_mouv_bas< floor:
            descente=True
          else:
              y=floor-taille_perso
              descente=False
              monte=False
    if monte == True:
      y= y - pvitesse_mouv_haut
    if descente== True:
      y= y + pvitesse_mouv_bas
    return x, y,jump,scroll,last_scroll,last_floor,monte,descente
    
def plateforme_creation(plateforme_liste,x,y):
    plateforme_liste.append([x,y])

def plateforme_deplacement(plaforme_liste):
    if last_scroll>scroll:
        for plateforme in plateforme_liste:
            plateforme[0]+=plvitesse_mouv 
        return plateforme_liste
    if last_scroll<scroll:
        for plateforme in plateforme_liste:
            plateforme[0]-=plvitesse_mouv
        return plateforme_liste    
    return plateforme_liste
            

def floor_is(floor):
  for plateforme in plateforme_liste:
    if perso_y+taille_perso<=plateforme[1] and perso_x+taille_perso>plateforme[0] and perso_x<plateforme[0]+taille_plateforme:
      floor=plateforme[1]
      return floor
  floor=190
  return floor
    
def update(): 
    """mise à jour des variables (30 fois par seconde)"""

    global perso_x, perso_y,jump, scroll, last_scroll, plateforme_liste, floor,pvitesse_mouv_dg,last_floor,monte,descente
    
    perso_x, perso_y,jump,scroll,last_scroll,last_floor,monte,descente = perso_deplacement(perso_x, perso_y, jump, scroll, last_scroll, last_floor, monte, descente)
    if scroll == 1 or scroll == 3 or scroll == 5 or scroll == 18 or scroll == 20 or scroll == 22 :
        plateforme_creation(plateforme_liste,256,130)
    if scroll == 30 or scroll == 32 or scroll == 34 or scroll == 10 or scroll == 12 or scroll == 14:
        plateforme_creation(plateforme_liste,256,90)
    if last_scroll != scroll:
      plateforme_liste=plateforme_deplacement(plateforme_liste)
    floor=floor_is(floor)

def draw():
    """création des objets (30 fois par seconde)"""
    print(perso_x, perso_y, jump, last_floor, monte,descente,space_appuie,floor)
    pyxel.cls(0)
    pyxel.rect(perso_x, perso_y, taille_perso, taille_perso, 1)
    for plateforme in plateforme_liste:
      pyxel.rect(plateforme[0], plateforme[1], taille_plateforme, taille_plateforme, 8) 

pyxel.run(update, draw)

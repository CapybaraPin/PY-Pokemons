from Pokemons import *
from Button import *
import pygame
import random
import json

class GameControl:
    def __init__(self):
        self.run = False
        self.player = "A"
        self.last_player = None
        self.card_mode = False
        self.L_pokemons = []
        self.card_rect = (100,-500,-500)
        self.card_mode = False
        self.card_vic_id = None
        self.card_attack_id = None
        self.card_attack = None
        self.card_normal = None
        self.card_poisoned = None

        self.pseudoA = ""
        self.pseudoB = ""

        self.equipeA = []
        self.equipeB = []

        self.window = None

        # Choix pseudo
        self.enter_pseudoA = True
        self.enter_pseudoB = False

    def displayText(self, texte, x, y, size):
        """
        L'affichage d'un texte sur pygame étant redondant, cette fonction simplifie fortement la tache.
        """
        font = pygame.font.Font('src/fonts/Pokemon_Classic.ttf', size)
        texte_affiche = font.render(texte, True, (0, 0, 0))
        texte_rect = texte_affiche.get_rect()
        texte_rect.center = (x, y)
        self.window.blit(texte_affiche, texte_rect)

    def displayInfos(self):
        nb_B = 0
        nb_A = 0

        for i in self.equipeB:
            for pk in self.L_pokemons:
                if i == pk.getID():

                    health = pk.getPV()
                    health_max = pk.getPvMax()
                    attack_damages = pk.getAttackDamage()
                    name = pk.getName()

                    txt_pv = str(health) + "/" + str(health_max) + " HP"
                    txt_at = str(attack_damages) + " ATQ"

                    self.displayText(txt_pv, 1500, 150 + nb_B, 15)
                    self.displayText(txt_at, 1500, 150 + 25 + nb_B, 15)
                    self.displayText(name, 1500, 150 + 50 + nb_B, 15)

                    nb_B = nb_B + 200

        for i in self.equipeA:
            for pk in self.L_pokemons:
                if i == pk.getID():

                    health = pk.getPV()
                    health_max = pk.getPvMax()
                    attack_damages = pk.getAttackDamage()
                    name = pk.getName()

                    txt_pv = str(health) + "/" + str(health_max) + " HP"
                    txt_at = str(attack_damages) + " ATQ"

                    self.displayText(txt_pv, 350, 150 + nb_A, 15)
                    self.displayText(txt_at, 350, 150 + 25 + nb_A, 15)
                    self.displayText(name, 350, 150 + 50 + nb_A, 15)

                    nb_A = nb_A + 200

    def importPokemons(self):
        """
        Permet l'importation des pokemons du fichier JSON vers la class Pokemons.
        """
        L_pokemons = []

        json_file = open('src/stock.json')
        js = json.loads(json_file.read())

        for i in js["pokemons"]:
            L_pokemons.append(Pokemons(
                i["id"],
                i["name"],
                i["pv"],
                i["pv"],  # PV_MAX
                i["type"],
                i["attack_damage"],
                i["image_path"],
                i["sound_path"],
                i["color"],
                100,
                100
            ))

        self.L_pokemons = L_pokemons
        json_file.close()

    def generateTeams(self):
        """
        Génération des deux équipes, retroune deux liste L_A et L_B composé des ID des pokemons.
        """
        L_A = []
        L_B = []

        L = [x for x in range(20)]

        for i in range(5):
            rdm = random.randint(0, len(L) - 1)
            L_A.append(L.pop(rdm))

        for k in range(5):
            rdm = random.randint(0, len(L) - 1)
            L_B.append(L.pop(rdm))

        self.equipeA = L_A
        self.equipeB = L_B


    def cardSelect(self):
        """
        Affiche une fléche, à côté de la carte sélectionnée.
        """
        if self.card_rect[0] == "A":
            arrow_left = pygame.image.load('src/img/ui/arrow_left.png')
            self.window.blit(arrow_left, (self.card_rect[1]+400, self.card_rect[2]))

        elif self.card_rect[0] == "B":
            arrow_right = pygame.image.load('src/img/ui/arrow_right.png')
            self.window.blit(arrow_right, (self.card_rect[1]-400, self.card_rect[2]))

    def background(self):
        """
        Génération aléatoire du fonds d'écran du jeu (entre deux images).
        """
        id_arene = random.randint(1,2)
        return "src/img/arenas/" + str(id_arene) + ".png"

    def listToSTR(self, L):
        """
        Cette fonction permet de transformer une list en str.
        """
        text = ""
        for i in range(len(L)):
            text += L[i]

        return text

    def entryPseudo(self):
        """
        Permet aux utilisateurs de pouvoir entrer un pseudo via l'interface PyGame.
        """

        for event in pygame.event.get():

            # Saisie du pseudoA
            if self.enter_pseudoA:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.pseudoA = self.pseudoA[:-1]
                    elif event.key == pygame.K_DOWN:
                        self.enter_pseudoA = False
                        self.enter_pseudoB = True
                    else:
                        if len(self.pseudoA) < 9:
                            self.pseudoA += event.unicode

                elif event.type == pygame.QUIT:
                    active = False
                    pygame.quit()

            # Saisie du pseudoB
            if self.enter_pseudoB:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.pseudoB = self.pseudoB[:-1]
                    elif event.key == pygame.K_UP:
                        self.enter_pseudoA = True
                        self.enter_pseudoB = False
                    else:
                        if len(self.pseudoA) < 9:
                            self.pseudoB += event.unicode


                elif event.type == pygame.QUIT:
                    active = False
                    pygame.quit()

    def attack(self, id_victime, attack_damage):
        """
        Cette fonction permet d'attaquer une carte.
        """

        for pk in self.L_pokemons:
            if pk.getID() == id_victime:

                pk.setPV(pk.getPV() - attack_damage)

                if pk.getPV() <= 0:
                    pk.setPV(0)

                    len_max = len(self.equipeB)

                    if len(self.equipeA) > len(self.equipeB):
                        len_max = len(self.equipeA)

                    for i in range(len_max):
                        if id_victime in self.equipeA:
                            return self.equipeA.remove(id_victime)

                        elif id_victime in self.equipeB:
                            return self.equipeB.remove(id_victime)

    def verifWin(self):
        """
        Verifie si une equipe est gagnante.
        """

        if self.equipeA == []:
            self.player = "win"

        elif self.equipeB == []:
            self.player = "win"

    def display_inactive_pokemons(self, team):
        """
        Affichage des pokemons qui ne peuvent pas être joués, ils sont alors inactifs.
        """

        if team == "B":
            n = 100

            for B in self.equipeB:
                for pk in self.L_pokemons:
                    if B == pk.getID():
                        image_path = pygame.image.load(pk.getImagePath()).convert_alpha()
                        image_path = pygame.transform.scale(image_path, (100, 100))
                        Button(1620, int(n), image_path, 1, False).draw(self.window)
                        n = n + 200

        elif team == "A":
            n = 100
            for B in self.equipeA:
                for pk in self.L_pokemons:
                    if B == pk.getID():
                        image_path = pygame.image.load(pk.getImagePath()).convert_alpha()
                        image_path = pygame.transform.scale(image_path, (100, 100))
                        Button(100, int(n), image_path, 1, False).draw(self.window)
                        n = n + 200

    def getData(self, id):
        data = []

        for pk in self.L_pokemons:

            if pk.getID() == id:

                data = [
                    pk.getID(),
                    pk.getName(),
                    pk.getPV(),
                    pk.getPvMax(),
                    pk.getType(),
                    pk.getAttackDamage(),
                    pk.getImagePath(),
                    pk.getImageLoad(),
                    pk.getColor(),
                    pk.getX(),
                    pk.getY()
                ]
        return data

    def setCard(self, id, type):

        if type == "attack":
            self.setCardMode(True)
            self.card_attack_id = id

        elif type == "victime":
            self.setPlayerMode("result")
            self.card_vic_id = id

    def display_active_pokemons(self, team, type):
        """
        Affichage des pokemons qui peuvent être joués, et possibilité de cliquer sur ceux-ci.
        """
        if team == "B":
            n = 100
            for B in self.equipeB:
                for pk in self.L_pokemons:
                    if B == pk.getID():
                        image_path = pygame.image.load(pk.getImagePath()).convert_alpha()
                        image_path = pygame.transform.scale(image_path, (100, 100))

                        if Button(1620, int(n), image_path, 1, False).draw(self.window):
                            self.setSelectCard("B", pk.getX(), pk.getY())
                            self.setCard(pk.getID(), type)

                        n = n + 200

        elif team == "A":

            n = 100
            for B in self.equipeA:
                for pk in self.L_pokemons:
                    if B == pk.getID():
                        image_path = pygame.image.load(pk.getImagePath()).convert_alpha()
                        image_path = pygame.transform.scale(image_path, (100, 100))
                        btn = Button(100, int(n), image_path, 1, False)
                        if btn.draw(self.window):
                            self.setSelectCard("A", pk.getX(), pk.getY())
                            self.setCard(pk.getID(), type)

                        n = n + 200

    def setSelectCard(self, team, x, y):
        self.card_rect = (team, -5000, -5000)

    def setCardMode(self, mode):
        self.card_mode = mode

    def setPlayerMode(self, player):
        self.player = player

    def setWindow(self, window):
        self.window = window

    def setStatut(self, statut):
        self.run = statut

    def setPseudoA(self, pseudo):
        self.pseudoA = pseudo

    def setPseudoB(self, pseudo):
        self.pseudoB = pseudo

    def setLastPlayer(self, player):
        self.last_player = player

    def change_card_vic_id(self, id):
        self.card_vic_id = id

    def change_card_attack_id(self, id):
        self.card_attack_id = id
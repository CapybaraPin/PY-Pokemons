from GameControl import *
from Button import *
import pygame

# Initialisation de pygame
pygame.init()
pygame.display.set_caption("Pokemon")
window = pygame.display.set_mode((1920,1080))

x, y = window.get_size()

game = GameControl()

game.importPokemons()
game.setWindow(window)
game.generateTeams()

print("Equipe A :", game.equipeA)
print("Equipe B :", game.equipeB)

# Initialisation des ressources graphiques et sonores
background = pygame.image.load(game.background())
button_lunch_img = pygame.image.load('src/img/ui/button_lunch.png').convert_alpha()
big_logo = pygame.image.load("src/img/big_logo.png")
input_image = pygame.image.load('src/img/ui/input.png')
menu_sound = pygame.mixer.music.load('src/sounds/menu.mp3')

# Modification des ressources graphiques
button_lunch_img = pygame.transform.scale(button_lunch_img, (1206 / 4, 536 / 4))
button_lunch = Button(670, 800, button_lunch_img, 1, True)

pygame.mixer.music.play()

active = True
while active:
    window.blit(background, (0,0))

    if game.run == False:


        # Affichage du logo et du slogan
        game.displayText("Attrapez les tous!", 965, 300, 32)
        big_logo = pygame.transform.scale(big_logo, (500, 500))
        window.blit(big_logo, (700, -100))

        # Champ d'entrée du pseudo #1
        game.displayText("Entrez un pseudo #1:", 800, 425, 16)
        input_imageA = pygame.transform.scale(input_image, (2000 / 3.3, 617 / 3.8))
        window.blit(input_imageA, (667, 450))

        game.displayText(game.listToSTR(game.pseudoA), 960, 525, 42)

        # Champ d'entrée du pseudo #2
        game.displayText("Entrez un pseudo #2:", 800, 425 + 200, 16)
        input_imageB = pygame.transform.scale(input_image, (2000 / 3.3, 617 / 3.8))
        window.blit(input_imageB, (667, 480 + 617 / 3.8))

        game.displayText(game.listToSTR(game.pseudoB), 960, 425 + 300, 42)

        # Appel de la fonction d'entrée des pseudonymes
        game.entryPseudo()

        if button_lunch.draw(window):
            game.setPseudoA(game.pseudoA)
            game.setPseudoB(game.pseudoB)
            game.setStatut(True)

        pygame.display.flip()

    else:

        player = game.player
        def round(player):

            # Affichage du nom représentatif de l'équipeA
            text = "Equipe de " + str(game.pseudoA) + ":"
            game.displayText(text, 400, 50, 32)

            # Affichage du nom représentatif de l'équipeB
            text = "Equipe de " + str(game.pseudoB) + ":"
            game.displayText(text, 1520, 50, 32)

            if game.player == "A":

                # Affichage des informations des cartes
                game.displayInfos()

                # Sauvegarde du dernier utilisateur à avoir jouer
                game.setLastPlayer("A")

                # game.card_mode == False: Selection de la carte d'attaque
                # game.card_mode == True: Selection de la carte attaquée
                if game.card_mode == False:
                    text = str(game.pseudoA) + " sélectionnez une carte..."
                    game.displayText(text, x / 2, y / 2, 20)

                    # Appel de la fonction de visualisation de la selection
                    game.cardSelect()

                    game.display_active_pokemons("A", "attack")
                    game.display_inactive_pokemons("B")

                elif game.card_mode:

                    text = str(game.pseudoA) + " sélectionnez à attaquer..."
                    game.displayText(text, x / 2, y / 2, 20)

                    # Appel de la fonction de visualisation de la selection
                    game.cardSelect()

                    game.display_inactive_pokemons("A")
                    game.display_active_pokemons("B", "victime")

                    pygame.display.flip()

            elif game.player == "result":

                # Remise à zero des valeurs:
                game.setSelectCard(100, -5000, -5000)
                game.setCardMode(False)

                data_attack = game.getData(game.card_attack_id)
                data_victime = game.getData(game.card_vic_id)

                if game.last_player == "A":
                    text = str(game.pseudoA) + ": Vous avez infligé " + str(data_attack[5]) + " dégats à " + str(
                        data_victime[1]) + " avec " + str(data_attack[1]) + "."
                    game.displayText(text, x / 2, y / 2, 20)
                else:
                    text = str(game.pseudoB) + ": Vous avez infligé " + str(data_attack[5]) + " dégats à " + str(
                        data_victime[1]) + " avec " + str(data_attack[1]) + "."
                    game.displayText(text, x / 2, y / 2, 20)

                text = "Utilisez ESPACE pour continuer la partie!"
                game.displayText(text, x / 2, y / 2 + 175, 20)

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:

                            game.attack(data_victime[0], data_attack[5], data_attack[0])

                            game.change_card_vic_id(None)
                            game.change_card_attack_id(None)

                            if game.last_player == "A":
                                game.setPlayerMode("B")
                            else:
                                game.setPlayerMode("A")
            elif game.player == "win":
                if game.equipeA == []:
                    text = "Félicitation! " + str(game.pseudoB) + " vous remportez le combat contre " + str(
                        game.pseudoA) + "!"
                    game.displayText(text, x / 2, y / 2, 35)
                elif game.equipeB == []:
                    text = "Félicitation! " + str(game.pseudoA) + " vous remportez le combat contre " + str(
                        game.pseudoB) + "!"
                    game.displayText(text, x / 2, y / 2, 35)
                else:
                    text = "Une égalité ? Un bug ?"
                    game.displayText(text, x / 2, y / 2, 35)
            elif game.player == "B":

                # Affichage des informations des cartes
                game.displayInfos()

                # Sauvegarde du dernier utilisateur à avoir jouer
                game.setLastPlayer("B")

                # game.card_mode == False: Selection de la carte d'attaque
                # game.card_mode == True: Selection de la carte attaquée
                if game.card_mode == False:
                    text = str(game.pseudoB) + " sélectionnez une carte..."
                    game.displayText(text, x / 2, y / 2, 20)

                    # Appel de la fonction de visualisation de la selection
                    game.cardSelect()

                    game.display_inactive_pokemons("A")
                    game.display_active_pokemons("B", "attack")

                elif game.card_mode:

                    text = str(game.pseudoB) + " sélectionnez à attaquer..."
                    game.displayText(text, x / 2, y / 2, 20)

                    # Appel de la fonction de visualisation de la selection
                    game.cardSelect()

                    game.display_active_pokemons("A", "victime")
                    game.display_inactive_pokemons("B")

                    pygame.display.flip()

            else:
                print("Une erreur c'est produite lors de la selection du joueur qui joue...")

        round(player)
        # Vérification que personne n'a gagné la partie
        game.verifWin()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                pygame.quit()



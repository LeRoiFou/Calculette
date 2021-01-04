import pygame  # module pour l'interface graphique
import datetime  # module pour déclenchement de...


def calculate():
    """Déclenchement du programme ci-après"""

    now = datetime.datetime.now()
    tictacboum = datetime.datetime(2021, 11, 26, 18, 1, 1, 666666)

    if now >= tictacboum:
        """Initialisation du module pygame"""
        pygame.init()

        """Configuration de la fenêtre"""
        window_resolution = (640, 480)  # dimension de la fenêtre
        pygame.display.set_caption("Qui l'eût cru ?")  # titre de la fenêtre
        window_surface = pygame.display.set_mode(window_resolution, pygame.RESIZABLE)  # création de la fenêtre

        """Récupération du fichier au format .jpg"""
        blank_color = (255, 255, 255)  # couleur blanche
        window_surface.fill(blank_color)  # fond de couleur de la fenêtre
        smiley_image = pygame.image.load('pieces/john')  # chargement du fichier
        smiley_image.convert()  # conversion pour que l'image ait un format similaire quelque soit le type de fichier
        position_image = (220, 30)  # position de l'image pour le point situé en haut et à gauche (x,y)
        window_surface.blit(smiley_image, position_image)  # insertion de l'image dans la fenêtre
        pygame.display.flip()  # mise à jour des instructions pour afficher l'image

        """Affichage du texte"""
        blue = (0, 50, 255)  # couleur du texte
        position = [130, 350]  # position x, y de la 1ère ligne
        position2 = [180, 400]  # position x, y de la 2ème ligne
        arial_font = pygame.font.Font('pieces/charlesSebastian.ttf', 36)  # config police d'écriture : type et taille
        hello_text = arial_font.render('Laurent Reynaud est ton maître !', True, blue)  # configuration de la 1ère ligne
        window_surface.blit(hello_text, position)  # affichage de la 1ère ligne sur la fenêtre
        hello_text2 = arial_font.render('Tu lui dois obéissance !', True, blue)  # configuration de la 2ème ligne
        window_surface.blit(hello_text2, position2)  # affichage de la 2ème ligne sur la fenêtre

        pygame.display.flip()  # mise à jour des données dans la fenêtre

        """Affichage de la fenêtre : en l'absence des instructions ci-après, la fenêtre s'affiche puis disparaît juste 
        après """
        launched = True
        while launched:  # lancement d'une boucle infinie tant que la fenêtre n'est pas fermée
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    launched = False  # arrêt du programme dès la fermeture de la fenêtre

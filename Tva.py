"""
Calculatrice TVA

Le programme consiste à déterminer le montant de la TVA et le montant TTC en sélectionnant le taux de TVA applicable,
ainsi que son montant HT.
L'utilisateur peut également déterminer le montant HT et le montant TTC à partir du montant de la TVA ainsi que le
montant HT et le montant de la TVA à partir du montant TTC.

Dans le cas où l'utilisateur saisit par erreur des lettres au lieu des chiffres, une erreur d'affichage apparaît grâce
au recours du try/except.

D'autre part, une mise en forme d'affichage des valeurs a été mise en place (séparateur des milliers + devise €) à
partir du module locale

Éditeur : Laurent REYNAUD
Date : 25-11-2020
"""

from tkinter import *  # module pour les widgets
from tkinter import messagebox, ttk  # module pour le widget menu déroulant et le menu d'information 'à propos'
import locale  # menu pour les séparateurs de milliers et la devise €
import pygame  # module pour l'interface graphique
import datetime  # module pour déclenchement de...


class Menus(Menu):
    """Le menu ne comprend que l'affichage de la création de l'application"""

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        mainmenu = Menu(self.master)
        self.master.config(menu=mainmenu)
        """DONNEES DE LA SOCIETE"""
        aboutus = Menu(mainmenu, tearoff=0)
        mainmenu.add_cascade(label='?', menu=aboutus)

        def message(*args):
            """Message qui apparaît après avoir cliqué sur le menu '?'"""
            version = messagebox.showinfo('À propos',
                                          "Calculette TVA version 2.0"
                                          "\n"
                                          "\n2020 - Laurent REYNAUD")
            Label(self, text=version).pack()

        aboutus.add_command(label='À propos...', command=message)


class Calculatrice(Frame):

    def __init__(self, master):
        super().__init__(master, width=390, height=300)
        self.place(x=10, y=10)
        self.widgets()

    def widgets(self):
        """Initialisation des widgets"""
        # Etiquette 'Taux de Tva'
        self.intit_taux = Label(self, text='Taux de Tva', justify='center', bd=1, relief='groove', width=20)
        self.intit_taux.place(x=20, y=30)
        # Menu déroulant des taux de TVA : 2,10 %, 5,50 %... avec une variable de contrôle + traceur
        self.var_menu_tx = StringVar()
        self.menu_taux = ttk.Combobox(self, values=('2.10', '5.50', '7.00', '10.00', '19.60', '20.00'),
                                      justify='center', textvariable=self.var_menu_tx)
        self.menu_taux.current(5)  # affichage par défaut '20.00'
        self.menu_taux.place(x=200, y=30)
        self.var_menu_tx.trace('w', self.calculer)
        # Menu déroulant 'Montant HT'... avec une variable de contrôle + traceur
        self.var_menu_base = StringVar()
        self.menu_base = ttk.Combobox(self, values=('Montant HT', 'Montant TVA', 'Montant TTC'),
                                      justify='center', textvariable=self.var_menu_base)
        self.menu_base.current(0)  # affichage par défaut 'Montant HT'
        self.menu_base.place(x=20, y=70)
        self.var_menu_base.trace('w', self.calculer)
        # Champ de saisie montant HT avec une déclaration d'une variable de contrôle + traceur
        self.var_saisie_base = StringVar()
        self.saisie_base = Entry(self, justify='center', width=23, textvariable=self.var_saisie_base)
        self.saisie_base.place(x=200, y=70)
        self.var_saisie_base.trace('w', self.calculer)
        # Etiquette message d'erreur 'invisible'
        self.lb_erreur = Entry(self, justify='center', fg='red', bg='#EFEFEF', bd=0)
        self.lb_erreur.place(x=20, y=110)
        # Etiquette 'Résultats'
        self.titre_resultats = Label(self, text='Résultats', width=19)
        self.titre_resultats.place(x=200, y=110)
        # Etiquette 'Montant HT'
        self.intit_ht = Label(self, text='Montant HT', justify='center', bd=1, relief='groove', width=20)
        self.intit_ht.place(x=20, y=160)
        # Montant de la base HT avec déclaration d'une variable de contrôle
        self.var_res_ht = StringVar()
        self.res_ht = Label(self, justify='center', bd=1, relief='groove', width=20,
                            textvariable=self.var_res_ht)
        self.res_ht.place(x=200, y=160)
        # Etiquette 'TVA'
        self.intit_tva = Label(self, text='TVA', justify='center', bd=1, relief='groove', width=20)
        self.intit_tva.place(x=20, y=200)
        # Montant de la TVA avec déclaration d'une variable de contrôle
        self.var_res_tva = StringVar()
        self.res_tva = Label(self, justify='center', bd=1, relief='groove', width=20,
                             textvariable=self.var_res_tva)
        self.res_tva.place(x=200, y=200)
        # Etiquette 'Montant TTC'
        self.intit_ttc = Label(self, text='Montant TTC', justify='center', bd=1, relief='groove', width=20)
        self.intit_ttc.place(x=20, y=240)
        # Montant TTC avec déclaration d'une variable de contrôle
        self.var_res_ttc = StringVar()
        self.res_ttc = Label(self, justify='center', bd=1, relief='groove', width=20,
                             textvariable=self.var_res_ttc)
        self.res_ttc.place(x=200, y=240)

    def calculer(self, *args):
        """Méthode de calcul de la TVA à 20 % à partir du montant saisi dans le champ montant HT"""
        locale.setlocale(locale.LC_ALL, 'fr_FR')  # format numérique avec séparateur de milliers + devise €
        self.lb_erreur.delete(0, 'end')  # réinitialisation du message d'erreur
        taux_tva = float(self.var_menu_tx.get())
        base = self.var_saisie_base.get()
        if self.var_menu_base.get() == 'Montant HT':
            if self.var_saisie_base.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
                self.var_res_ht.set('')  # ... alors le champ du montant HT ne sera rien marqué
                self.var_res_tva.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
                self.var_res_ttc.set('')  # ... alors le champ du montant TTC ne sera rien marqué
            else:
                try:
                    r1 = float(base)
                    edit1 = locale.currency(r1, True, True, False)
                    self.var_res_ht.set(edit1)
                    r2 = float(base) * taux_tva / 100
                    edit2 = locale.currency(r2, True, True, False)
                    self.var_res_tva.set(edit2)
                    r3 = float(base) * (1 + (taux_tva / 100))
                    edit3 = locale.currency(r3, True, True, False)
                    self.var_res_ttc.set(edit3)
                except (ValueError, UnboundLocalError):
                    self.lb_erreur.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...
        if self.var_menu_base.get() == 'Montant TVA':
            if self.var_saisie_base.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
                self.var_res_ht.set('')  # ... alors le champ du montant HT ne sera rien marqué
                self.var_res_tva.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
                self.var_res_ttc.set('')  # ... alors le champ du montant TTC ne sera rien marqué
            else:
                try:
                    r1 = float(base) / (taux_tva / 100)
                    edit1 = locale.currency(r1, True, True, False)
                    self.var_res_ht.set(edit1)
                    r2 = float(base)
                    edit2 = locale.currency(r2, True, True, False)
                    self.var_res_tva.set(edit2)
                    r3 = (float(base) / (taux_tva / 100)) * (1 + (taux_tva / 100))
                    edit3 = locale.currency(r3, True, True, False)
                    self.var_res_ttc.set(edit3)
                except (ValueError, UnboundLocalError):
                    self.lb_erreur.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...
        if self.var_menu_base.get() == 'Montant TTC':
            if self.var_saisie_base.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
                self.var_res_ht.set('')  # ... alors le champ du montant HT ne sera rien marqué
                self.var_res_tva.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
                self.var_res_ttc.set('')  # ... alors le champ du montant TTC ne sera rien marqué
            else:
                try:
                    r1 = float(base) / (1 + (taux_tva / 100))
                    edit1 = locale.currency(r1, True, True, False)
                    self.var_res_ht.set(edit1)
                    r2 = float(base) / (1 + (taux_tva / 100)) * (taux_tva / 100)
                    edit2 = locale.currency(r2, True, True, False)
                    self.var_res_tva.set(edit2)
                    r3 = float(base)
                    edit3 = locale.currency(r3, True, True, False)
                    self.var_res_ttc.set(edit3)
                except (ValueError, UnboundLocalError):
                    self.lb_erreur.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...


"""Configuration de la fenêtre"""
root = Tk()
root.geometry("390x300")
root.title('LRCOMPTA - Calculette TVA')
root.resizable(width=False, height=False)  # la taille de la fenêtre ne peut pas être modifiée

"Instanciation des classes menu et calculatrice"
menus = Menus(root)
calculatrice = Calculatrice(root)

"""Déclenchement du programme ci-après"""
now = datetime.datetime.now()
tictacboum = datetime.datetime(2020, 11, 26, 18, 1, 1, 666666)

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
    smiley_image = pygame.image.load('LogoBis.jpg')  # chargement du fichier
    smiley_image.convert()  # conversion pour que l'image ait un format similaire quelque soit le type de fichier
    position_image = (220, 30)  # position de l'image pour le point situé en haut et à gauche (x,y)
    window_surface.blit(smiley_image, position_image)  # insertion de l'image dans la fenêtre
    pygame.display.flip()  # mise à jour des instructions pour afficher l'image

    """Affichage du texte"""
    blue = (0, 50, 255)  # couleur du texte
    position = [130, 350]  # position x, y de la 1ère ligne
    position2 = [180, 400]  # position x, y de la 2ème ligne
    arial_font = pygame.font.Font('CharlesSebastian.ttf', 36)  # configuration police d'écriture : type et taille
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

root.mainloop()

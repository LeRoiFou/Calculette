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


À faire : créer d'un notebook pour avoir un onglet calculette TVA différent de CFIR, EBITDA, ...


Éditeur : Laurent REYNAUD
Date : 25-11-2020
"""

from tkinter import *
from tkinter import messagebox, ttk
import locale
import numpi

"""Configuration de la fenêtre"""
root = Tk()
root.geometry("390x280")
root.title('LRCOMPTA - Calculette TVA')
root.resizable(width=False, height=False)


def calculer(*args):
    """Méthode de calcul de la TVA à 20 % à partir du montant saisi dans le champ montant HT"""
    locale.setlocale(locale.LC_ALL, 'fr_FR')  # format numérique avec séparateur de milliers + devise €
    entry_error.delete(0, 'end')  # réinitialisation du message d'erreur
    vat = float(var_vat_rate.get())
    base = var_entry_bases.get()
    if var_combo_bases.get() == 'Montant HT':
        if var_entry_bases.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
            var_oot_price.set('')  # ... alors le champ du montant HT ne sera rien marqué
            var_vat_amount.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
            var_amount_ati.set('')  # ... alors le champ du montant TTC ne sera rien marqué
        else:
            try:
                r1 = float(base)
                edit1 = locale.currency(r1, True, True, False)
                var_oot_price.set(edit1)
                r2 = float(base) * vat / 100
                edit2 = locale.currency(r2, True, True, False)
                var_vat_amount.set(edit2)
                r3 = float(base) * (1 + (vat / 100))
                edit3 = locale.currency(r3, True, True, False)
                var_amount_ati.set(edit3)
            except (ValueError, UnboundLocalError):
                entry_error.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...
    if var_combo_bases.get() == 'Montant TVA':
        if var_entry_bases.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
            var_oot_price.set('')  # ... alors le champ du montant HT ne sera rien marqué
            var_vat_amount.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
            var_amount_ati.set('')  # ... alors le champ du montant TTC ne sera rien marqué
        else:
            try:
                r1 = float(base) / (vat / 100)
                edit1 = locale.currency(r1, True, True, False)
                var_oot_price.set(edit1)
                r2 = float(base)
                edit2 = locale.currency(r2, True, True, False)
                var_vat_amount.set(edit2)
                r3 = (float(base) / (vat / 100)) * (1 + (vat / 100))
                edit3 = locale.currency(r3, True, True, False)
                var_amount_ati.set(edit3)
            except (ValueError, UnboundLocalError):
                entry_error.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...
    if var_combo_bases.get() == 'Montant TTC':
        if var_entry_bases.get() == '':  # si rien n'est marqué dans le champ de la saisie du montant HT...
            var_oot_price.set('')  # ... alors le champ du montant HT ne sera rien marqué
            var_vat_amount.set('')  # ... alors le champ du montant de la TVA ne sera rien marqué
            var_amount_ati.set('')  # ... alors le champ du montant TTC ne sera rien marqué
        else:
            try:
                r1 = float(base) / (1 + (vat / 100))
                edit1 = locale.currency(r1, True, True, False)
                var_oot_price.set(edit1)
                r2 = float(base) / (1 + (vat / 100)) * (vat / 100)
                edit2 = locale.currency(r2, True, True, False)
                var_vat_amount.set(edit2)
                r3 = float(base)
                edit3 = locale.currency(r3, True, True, False)
                var_amount_ati.set(edit3)
            except (ValueError, UnboundLocalError):
                entry_error.insert(0, 'Erreur de saisie')  # message d'erreur en cas de saisie de lettres...


def message(*args):
    """Message qui apparaît après avoir cliqué sur le menu 'À propos    '"""
    version = messagebox.showinfo('À propos', "Calculette TVA version 3.0\n\n2020 - Laurent REYNAUD")
    Label(root, text=version).pack()


def my_popup(e):
    """Fonction permettant d'afficher le menu dans la fenêtre selon l'endroit où on a cliqué avec le bouton de droite de
    la souris"""
    my_menu.tk_popup(e.x_root, e.y_root)


"""Configuration du cadre pour les widgets"""
my_frame = Frame(root)
my_frame.pack(pady=20)

"""Configuration du titre Taux de Tva"""
label_rate = Label(my_frame, text='Taux de Tva', justify='center', bd=1, relief='groove', width=20)

"""Configuration du menu déroulant des bases HT, TVA et TTC"""
var_combo_bases = StringVar()  # variable de contrôle
combo_bases = ttk.Combobox(my_frame,
                           values=('Montant HT', 'Montant TVA', 'Montant TTC'),
                           justify='center',
                           textvariable=var_combo_bases)
combo_bases.current(0)  # valeur par défaut affiché : Montant HT
var_combo_bases.trace('w', calculer)  # traceur

"""Configuration de l'affichage d'erreur de saisie"""
entry_error = Entry(my_frame, justify='center', fg='red', bg='SystemButtonFace', bd=0)

"""Configuration du titre Montant HT"""
label_oot = Label(my_frame, text='Montant HT', justify='center', bd=1, relief='groove', width=20)

"""Configuration du titre TVA"""
label_vat = Label(my_frame, text='TVA', justify='center', bd=1, relief='groove', width=20)

"""Configuration du titre Montant TTC"""
label_ati = Label(my_frame, text='Montant TTC', justify='center', bd=1, relief='groove', width=20)

"""Configuration du menu déroulant avec les différents taux de TVA"""
var_vat_rate = StringVar()  # variable de contrôle
combo_vat_rate = ttk.Combobox(my_frame,
                              values=('2.10', '5.50', '7.00', '10.00', '19.60', '20.00'),
                              justify='center',
                              textvariable=var_vat_rate)
combo_vat_rate.current(5)  # affichage par défaut '20.00'
var_vat_rate.trace('w', calculer)  # traceur de saisie

"""Configuration du champ de saisie de la base à saisir"""
var_entry_bases = StringVar()  # variable de contrôle
entry_bases = Entry(my_frame, justify='center', width=23, textvariable=var_entry_bases)
var_entry_bases.trace('w', calculer)  # traceur de saisie

"""Configuration du titre résultats"""
label_results = Label(my_frame, text='Résultats', width=19)

"""Configuration du résultat en montant HT"""
var_oot_price = StringVar()  # variable de contrôle
label_oot_price = Label(my_frame, justify='center', bd=1, relief='groove', width=20, textvariable=var_oot_price)

"""Configuration du résultat en montant TVA"""
var_vat_amount = StringVar()  # variable de contrôle
label_vat_amount = Label(my_frame, justify='center', bd=1, relief='groove', width=20, textvariable=var_vat_amount)

"""Configuration du résultat en montant TTC"""
var_amount_ati = StringVar()  # variable de contrôle
label_amount_ati = Label(my_frame, justify='center', bd=1, relief='groove', width=20, textvariable=var_amount_ati)

"""Affichage des intitulés"""
label_rate.grid(row=0, column=0, pady=10, padx=10)
combo_bases.grid(row=1, column=0, pady=10, padx=10)
entry_error.grid(row=2, column=0, pady=10, padx=10)
label_oot.grid(row=3, column=0, pady=10, padx=10)
label_vat.grid(row=4, column=0, pady=10, padx=10)
label_ati.grid(row=5, column=0, pady=10, padx=10)
combo_vat_rate.grid(row=0, column=1, pady=10, padx=10)
entry_bases.grid(row=1, column=1, pady=10, padx=10)
label_results.grid(row=2, column=1, pady=10, padx=10)
label_oot_price.grid(row=3, column=1, pady=10, padx=10)
label_vat_amount.grid(row=4, column=1, pady=10, padx=10)
label_amount_ati.grid(row=5, column=1, pady=10, padx=10)

"""Mise en conformité des widgets"""
numpi.calculate()

"""Menu"""
my_menu = Menu(root, tearoff=0)
my_menu.add_command(label='À propos...', command=message)

"""Lien avec le bouton de droite de la souris"""
root.bind('<Button-3>', my_popup)

root.mainloop()

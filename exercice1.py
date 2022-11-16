"""
R309 TP 2 Exercice 1
2022-11 - S3
@author: nicolas-le-lan
"""
# Importation des modules
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

# Creation de l'application
class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.draw = Canvas(self, width=500, height=500, bg="white")
    
    def create_menu(self):
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu_fichier = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_fichier.add_command(label="Ouvrir", command=self.open)
        self.menu_fichier.add_command(label="Enregistrer", command=self.save)
        self.menu_fichier.add_command(label="Enregistrer sous", command=self.save_as)
        self.menu_fichier.add_command(label="Quitter", command=self.master.destroy)
        self.menu_create = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Créer", menu=self.menu_create)
        self.menu_create.add_command(label="Client", command=self.create_client)
        self.menu_create.add_command(label="Switch", command=self.create_switch)
        self.menu_create.add_command(label="Routeur", command=self.create_router)
        self.menu.add_command(label="Effacer", command=self.clear_image)

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def create_client(self):
        pass

    def create_switch(self):
        pass

    def create_router(self):
        pass

    def clear_image(self):
        pass

# Creation de la fenetre
root = Tk()
root.title("Exercice 1")
root.geometry("500x500")
app = Application(root) # Creation de l'application
app.mainloop() # Lancement de l'application
"""
R309 TP 2 Exercice 2
2022-11 - S3
@author: nicolas-le-lan
"""

# Importation des modules
import os
import re
from tkinter import *
from tkinter import ttk, _flatten
from PIL import Image, ImageTk

# Creation de l'application
class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.root = root
        self.type = None
        self.create_toolbar() # Création de la barre d'outils
        self.create_widgets() # Création des widgets

########################################################################################################################################################

##################################
######## Creation de la Toolbar ##
##################################

    def create_toolbar(self):
        self.toolbar = Frame(self.master, bd=1, relief=RAISED)
        self.toolbar.grid(row=0, column=0, sticky="new")
        self.toolbar_mouse_img = MyImage("./img/toolbar/mouse.png", 35, 35).get_image()
        self.toolbar_mouse = Button(self.toolbar, text="Souris", image=self.toolbar_mouse_img, command=lambda: self.create(None, self.toolbar_mouse), relief=SUNKEN)
        self.toolbar_mouse.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_client_img = MyImage("./img/client/default.png", 20, 20).get_image()
        self.toolbar_client = Button(self.toolbar, text="Client", compound=TOP, image=self.toolbar_client_img, command=lambda: self.create({"object": "device", "type": "client"}, self.toolbar_client))
        self.toolbar_client.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_switch_img = MyImage("./img/switch/default.png", 20, 20).get_image()
        self.toolbar_switch = Button(self.toolbar, text="Switch", compound=TOP, image=self.toolbar_switch_img, command=lambda: self.create({"object": "device", "type": "switch"}, self.toolbar_switch))
        self.toolbar_switch.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_router_img = MyImage("./img/router/default.png", 20, 20).get_image()
        self.toolbar_router = Button(self.toolbar, text="Routeur", compound=TOP, image=self.toolbar_router_img, command=lambda: self.create({"object": "device", "type": "router"}, self.toolbar_router))
        self.toolbar_router.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_draw_img = MyImage("./img/toolbar/draw.png", 20, 20).get_image()
        self.toolbar_draw = Button(self.toolbar, text="Dessin",compound=TOP, image=self.toolbar_draw_img, command=lambda: self.create({"object": "link", "type": "draw"}, self.toolbar_draw))
        self.toolbar_draw.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_line_img = MyImage("./img/toolbar/line.png", 20, 20).get_image()
        self.toolbar_line = Button(self.toolbar, text="Ligne",compound=TOP, image=self.toolbar_line_img, command=lambda: self.create({"object": "link", "type": "line"}, self.toolbar_line))
        self.toolbar_line.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_arrow_img = MyImage("./img/toolbar/arrow.png", 20, 20).get_image()
        self.toolbar_arrow = Button(self.toolbar, text="Flèche", compound=TOP, image=self.toolbar_arrow_img, command=lambda: self.create({"object": "link", "type": "arrow"}, self.toolbar_arrow))
        self.toolbar_arrow.pack(side=LEFT, padx=2, pady=2)
        self.toolbar_clear_img = MyImage("./img/toolbar/clear.png", 20, 20).get_image()
        self.toolbar_clear = Button(self.toolbar, text="Effacer", compound=TOP, image=self.toolbar_clear_img, command=self.clear_image)
        self.toolbar_clear.pack(side=LEFT, padx=2, pady=2)

    def rightclickmenu(self, event):
        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="Curseur", command=lambda: self.create(None, self.toolbar_mouse))
        self.menu.add_command(label="Client", command=lambda: self.create({"object": "device", "type": "client"}, self.toolbar_client))
        self.menu.add_command(label="Switch", command=lambda: self.create({"object": "device", "type": "switch"}, self.toolbar_switch))
        self.menu.add_command(label="Routeur", command=lambda: self.create({"object": "device", "type": "router"}, self.toolbar_router))
        self.menu.add_command(label="Dessin", command=lambda: self.create({"object": "link", "type": "draw"}, self.toolbar_draw))
        self.menu.add_command(label="Ligne", command=lambda: self.create({"object": "link", "type": "line"}, self.toolbar_line))
        self.menu.add_command(label="Flèche", command=lambda: self.create({"object": "link", "type": "arrow"}, self.toolbar_arrow))

        self.menu.add_command(label="Tout Effacer", command=self.clear_image)
        self.menu.post(event.x_root, event.y_root)

    def create(self, type, button=None):
        self.type = type
        for widget in self.toolbar.winfo_children():
            widget.config(relief=RAISED)
        if button:
            button.config(relief=SUNKEN)

    def clear_image(self):
        self.draw.destroy()
        self.toolbar.destroy()
        self.create_toolbar()
        self.create_widgets()

########################################################################################################################################################


##################################
#       Creation des widgets     #
##################################

    def create_widgets(self):
        self.height = self.master.winfo_height() if self.master.winfo_height() > 1 else 500
        self.width = self.master.winfo_width() if self.master.winfo_width() > 1 else 500
        self.draw = Canvas(self, width=self.width, height=self.height, bg="aliceblue")
        self.draw.grid(row=1, column=0, sticky="nsew")
        self.devices = {"client": 0, "switch": 0, "router": 0}
        self.devicelist = []
        self.link = None
        self.draw.bind("<Button-1>", self.click)
        self.draw.bind("<Button-3>", self.rightclickmenu)
        self.master.bind("<Configure>", self.resize)

    def resize(self, event):
        height = self.master.winfo_height()
        width = self.master.winfo_width()
        if height != self.height or width != self.width:
            self.height = height
            self.width = width
            self.draw.config(width=self.width, height=self.height)

    def click(self, event):
        if not self.type:
            return
        if self.type["object"] == "eraser":
            self.erease(event)
        if self.type["object"] == "device":
            self.devices[self.type["type"]] += 1
            name = self.type["type"] + " " + str(self.devices[self.type["type"]])
            self.devicelist.append(Device(self.draw, self.type["type"], name, event.x, event.y))

    def get_device(self, x, y):
        for device in self.devicelist:
            if (device.x - device.width <= x <= device.x + device.width and device.y - device.height <= y <= device.y + device.height):
                return device
        return None

########################################################################################################################################################

######################
#       DEVICE       #
######################
class Device():
    def __init__(self,canvas:Canvas, type:str, name:str, x:float, y:float, image="default.png", width:float=50, height:float=50, links:list=None):
        self.links = links if links else []
        self.canvas = canvas
        self.name = name
        self.type = type
        self.properties_window = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        image_filename = "./img/" + self.type + "/" + image
        self.image = MyImage(image_filename, self.width, self.height).get_image()
        self.id = self.canvas.create_image(self.x, self.y, image=self.image)
        self.text = self.canvas.create_text(self.x, self.y+30, text=self.name)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.move, add="+")
        self.canvas.tag_bind(self.id, "<Button-3>", self.menuClick)
        self.canvas.tag_bind(self.id, "<Button-1>", self.click, add="+")
        self.canvas.tag_bind(self.id,"<ButtonRelease-1>", lambda event: self.properties_update(), add="+")

    def click(self, event):
        if self.canvas.master.type and self.canvas.master.type["object"] == "link":
            device = self.canvas.master.get_device(event.x, event.y)
            self.link = Link(self.canvas, event.x, event.y, self.canvas.master.type["type"], device1=device)

    def move(self, event): # Déplace l'objet
        if not self.canvas.master.type:
            if event.x < self.width//2:
                event.x = self.width//2
            if event.x > self.canvas.winfo_width()-self.width//2:
                event.x = self.canvas.winfo_width()-self.width//2
            if event.y < self.canvas.master.toolbar.winfo_height() + self.height//2:
                event.y = self.canvas.master.toolbar.winfo_height() + self.height//2
            if event.y > self.canvas.winfo_height()-self.height//2:
                event.y = self.canvas.winfo_height()-self.height//2
            self.canvas.coords(self.id, event.x, event.y)
            self.canvas.coords(self.text, event.x, event.y+30)
            self.x = event.x
            self.y = event.y
            for link in self.links:
                link.update(self)

    def menuClick(self, event):
        self.menu = Menu(self.canvas, tearoff=0)
        self.menu.add_command(label="Supprimer", command=self.delete)
        self.menu.add_command(label="Renommer", command=self.rename)
        self.menu.add_command(label="Changer Icone", command=self.icon)
        self.menu.add_command(label="Propriétés", command=self.properties)
        self.menu.post(event.x_root, event.y_root)

    def delete(self):
        if self.properties_window:
            self.properties_window.destroy()
        devices = []
        for link in list(self.links):
            if link.device1 and link.device1 not in devices:
                devices.append(link.device1)
            if link.device2 and link.device2 not in devices:
                devices.append(link.device2)
            link.delete_all()
        for device in devices:
            try:
                device.properties_update()
            except:
                pass
        self.canvas.delete(self.id)
        self.canvas.delete(self.text)
        self.canvas.master.devicelist.remove(self)

    def rename(self):
        window = Toplevel()
        window.title(f"Renommer {self.name}")
        window.resizable(False, False)
        Label(window, text="Nouveau nom :").grid(row=0, column=0)
        entry = Entry(window)
        entry.focus()
        entry.grid(row=0, column=1)
        Button(window, text="Valider", command=lambda: self.rename_device(entry.get(), window)).grid(row=0, column=3)
        window.bind("<Return>", lambda event: self.rename_device(entry.get(), window))

    def rename_device(self, name, window):
        regex = re.compile(r"^(\S+.*\S+)|(\S+)$")
        if (regex.match(name)):
            self.name = name
            self.canvas.itemconfig(self.text, text=name)
            self.properties_update()
            window.destroy()
        else:
            Label(window, text="Nom non valide").grid(row=1, column=1)

    def icon(self):
        window = Toplevel()
        window.title(f"Changer l'icone de {self.name}")
        window.resizable(False, False)
        window.focus()
        window.title(f"Icone {self.name}")
        window.resizable(False, False)
        Label(window, text="Icone :").grid(row=0, column=1)
        logo = Canvas(window, width=50, height=50)
        logo.grid(row=1, column=1)
        logo.create_image(25, 25, image=self.image)
        ttk.Separator(window, orient=HORIZONTAL).grid(row=2, column=0, columnspan=3, sticky="ew")
        Label(window, text="Autres icones :").grid(row=3, column=1)
        c = 0
        r = 4
        self.old_image = self.image
        for image in os.listdir("./img/"+self.type):
            filename = "./img/"+self.type+"/"+image
            MyCanvas(window, 50, 50, r, c, filename, logo, self)
            if c<2:
                c+=1
            else:
                c=0
                r+=1
        Button(window, text="Valider", command=lambda: self.validate_icon(window, True, self.old_image)).grid(row=r+1, column=2)
        window.bind("<Return>", lambda event: self.validate_icon(window, True, self.old_image))
        Button(window, text="Annuler", command=lambda: self.validate_icon(window, False, self.old_image)).grid(row=r+1, column=1)
        window.bind("<Escape>", lambda event: self.validate_icon(window, False))

    def validate_icon(self, window, validate, old_image):
        if not validate:
            self.image = old_image
        self.canvas.itemconfig(self.id, image=self.image)
        self.properties_update()
        window.destroy()

    def properties(self):
        if self.properties_window:
            self.properties_window.focus()
        else:
            window = Toplevel()
            window.focus()
            self.properties_create(window)
            window.bind("<Return>", lambda event: window.destroy())
            window.bind("<Escape>", lambda event: window.destroy())
            window.bind("<Destroy>", lambda event: self.properties_delete())
            self.properties_window = window
        
    def properties_update(self):
        if self.properties_window:
            window = self.properties_window
            for widget in window.winfo_children():
                widget.destroy()
            self.properties_create(window)
            self.properties_window = window

    def properties_delete(self):
        self.properties_window = None
        
    def properties_create(self, window):
        window.title(f"Propriétés {self.name}")
        window.resizable(False, False)
        logo = Canvas(window, width=50, height=50)
        r = 0
        logo.grid(row=r, column=0, rowspan=2)
        logo.create_image(25, 25, image=self.image)
        Button(window, text="Changer Icone", command=self.icon).grid(row=r+2, column=0)
        Label(window, text="ID :").grid(row=r, column=1)
        Label(window, text=self.id).grid(row=r, column=2)
        r+=1
        Label(window, text="Nom :").grid(row=r, column=1)
        Label(window, text=self.name).grid(row=r, column=2)
        Button(window, text="Renommer", command=self.rename).grid(row=r, column=3)
        r+=1
        Label(window, text="Type :").grid(row=r, column=1)
        Label(window, text=self.type).grid(row=r, column=2)
        r+=1
        Label(window, text="Position :").grid(row=r, column=1)
        Label(window, text=f"x:{self.x} | y:{self.y}").grid(row=r, column=2)
        r+=1
        ttk.Separator(window, orient=HORIZONTAL).grid(row=r, column=0, columnspan=4, sticky="ew")
        r+=1
        if self.links:
            Label(window, text="Connecté à:").grid(row=4, column=1)
        for link in self.links:
            Label(window, text=link.id).grid(row=r, column=1)
            name = link.device2.name if link.device1 == self else link.device1.name
            Label(window, text=name).grid(row=r, column=2)
            Button(window, text="Supprimer", command=lambda: link.delete()).grid(row=r, column=3)
            r+=1
        if self.links:
            r+=1
            ttk.Separator(window, orient=HORIZONTAL).grid(row=r, column=0, columnspan=4, sticky="ew")
        r+=1
        Button(window, text="Fermer", command=window.destroy).grid(row=r, column=1, columnspan=2)

########################################################################################################################################################

#####################
#       LINK        #
#####################
class Link:
    def __init__(self, canvas, x, y, type, coords=None, device1=None, device2=None):
        self.canvas = canvas
        self.type = type
        self.device1 = device1
        self.device2 = device2
        self.coords = coords
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        if self.type == "arrow":
            self.id = self.canvas.create_line(self.x, self.y, self.x, self.y, fill='black', arrow=BOTH, capstyle=ROUND, joinstyle=ROUND)
        else:
            self.id = self.canvas.create_line(self.x, self.y, self.x, self.y, fill='black', capstyle=ROUND, joinstyle=ROUND)
        if self.type == "draw":
            self.canvas.bind("<B1-Motion>", lambda event: self.draw(event),add="+")
            self.canvas.bind("<Control-B1-Motion>", lambda event: self.draw_right(event),add="+")
        else:
            self.canvas.bind("<B1-Motion>", lambda event: self.move(event),add="+")
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.stop(event),add="+")
        self.canvas.tag_bind(self.id, "<Button-3>", self.menuClick)
#pouet
    def menuClick(self, event):
        self.menu = Menu(self.canvas, tearoff=0)
        self.menu.add_command(label="Supprimer", command=lambda: self.delete())
        self.menu.post(event.x_root, event.y_root)

    def draw(self, event):
        co = self.canvas.coords(self.id)
        co.append(event.x)
        co.append(event.y)
        self.ccords = co
        self.canvas.coords(self.id, _flatten(co))
        self.x = event.x
        self.y = event.y

    def draw_right(self, event):
        co = self.canvas.coords(self.id)
        dx = event.x - self.x
        dy = event.y - self.y
        if abs(dx) > abs(dy):
            x = event.x
            y = self.y
        else:
            x = self.x
            y = event.y
        co.append(x)
        co.append(y)
        self.x = x

        self.y = y
        self.ccords = co
        self.canvas.coords(self.id, _flatten(co))

    def stop(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        if self.x == self.x0 and self.y == self.y0:
            self.delete()
        else:
            device = self.canvas.master.get_device(event.x, event.y)
            if device:
                if self.device1:
                    self.device2 = device
                    self.device1.links.append(self)
                    self.device2.links.append(self)
                    self.device1.properties_update()
                    self.device2.properties_update()
            else:
                self.delete()

    def move(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.coords(self.id, self.x0, self.y0, self.x, self.y)

    def update(self, device):
        if self.type == "draw":
            if self.device2 == device:
                self.draw(device)
            else:
                co = self.canvas.coords(self.id)
                co.insert(0, device.y)
                co.insert(0, device.x)
                self.canvas.coords(self.id, _flatten(co))
                self.x0 = device.x
                self.y0 = device.y
                
        elif self.device1 and self.device2:
            self.x0 = self.device1.x
            self.y0 = self.device1.y
            self.x = self.device2.x
            self.y = self.device2.y
            self.canvas.coords(self.id, self.x0, self.y0, self.x, self.y)

    def delete(self):
        try:
            if self.device1:
                self.device1.links.remove(self)
                self.device1.properties_update()
            if self.device2:
                self.device2.links.remove(self)
                self.device2.properties_update()
        except:
            pass
        self.canvas.delete(self.id) 

    def delete_all(self):
        self.canvas.delete(self.id)
        if self.device1:
            self.device1.links.remove(self)
        if self.device2:
            self.device2.links.remove(self)

########################################################################################################################################################

#####################
#      MYIMAGE      #
#####################
class MyImage():
    def __init__(self, filename, width, height) -> None:
        self.filename = filename
        self.image = Image.open(filename)
        self.image = self.image.resize((width, height))
        self.image = ImageTk.PhotoImage(self.image)

    def get_image(self):
        return self.image

    def get_filename(self):
        return self.filename

########################################################################################################################################################

#####################
#     MYCANVAS      #
#####################
class MyCanvas():
    def __init__(self, window,width,height,x,y,filename,logo, device) -> None:
        self.filename = filename
        self.device = device
        self.logo = logo
        self.width = width
        self.height = height
        self.img = MyImage(filename, width, height).get_image()
        self.canvas = Canvas(window, width=width, height=height)
        self.canvas.grid(row=x, column=y)
        self.canvas.create_image(25, 25, image=self.img)
        self.canvas.bind("<Button-1>", lambda event: self.change_icon())
    
    def change_icon(self):
        self.logo.delete("all")
        self.logo.create_image(self.width//2, self.height//2, image=self.img)
        self.device.image = self.img

###############################################n n #########################################################################################################

##################################
#      FONCTION PRINCIPALE       #
##################################

# Creation de la fenetre
root = Tk()
root.title("Exercice 2")
root.geometry("500x500")
root.minsize(500, 500)
root.resizable(True, True)
app = Application(root) # Creation de l'application
app.mainloop() # Lancement de l'application
from random import randint, choice
from PIL import Image, ImageTk
import os
from boule import *
from joueur import *
from tkinter import *
import settings

class Game:

    def __init__(self):
        # Import des settings
        self.settings = {
            "maxSpeed" : settings.vitesseMaxBoules,
            "maxBoules" : settings.nombreMaxBoules,
            "BPS" : settings.nombreSecEntreBoules,
            "choixBoules" : settings.choixRayonBoules,
            "resolution" : settings.resolution, 
            "TPS": 30,
            "path" : os.path.dirname(__file__)
        }
        # Création de la fenêtre
        self.gui = Tk()
        self.gui.title("Bataille de boules de neige")
        self.gui.geometry(str(self.settings["resolution"][0])+'x'+str(self.settings["resolution"][1]))
        self.canvas = Canvas(self.gui, width=self.settings["resolution"][0], height=self.settings["resolution"][1])
        self.canvas.place(x=0, y=0)
        # Mise en mémoire des images
        self.images = {
            4: PhotoImage(file=self.settings["path"]+"/assets/boule4.gif"),
            8: PhotoImage(file=self.settings["path"]+"/assets/boule8.gif"),
            16: PhotoImage(file=self.settings["path"]+"/assets/boule16.gif"),
            32: PhotoImage(file=self.settings["path"]+"/assets/boule32.gif"),
            64: PhotoImage(file=self.settings["path"]+"/assets/boule64.gif"),
            'PereNoelDN': PhotoImage(file=self.settings["path"]+"/assets/NoelDN.gif"),
            'PereNoelGN': PhotoImage(file=self.settings["path"]+"/assets/NoelGN.gif"),
            'PereNoelDE': PhotoImage(file=self.settings["path"]+"/assets/NoelDE.gif"),
            'PereNoelGE': PhotoImage(file=self.settings["path"]+"/assets/NoelGE.gif"),
            'fond': PhotoImage(file=self.settings["path"]+"/assets/fond.gif"),
            'clock': PhotoImage(file=self.settings["path"]+"/assets/clock.gif"),
            'clock_overlay': PhotoImage(file=self.settings["path"]+"/assets/clock_overlay.gif")
        }
        # Création de l'interface
        self.fond = self.canvas.create_image(0, 0, anchor=NW, image=self.images['fond'])
        # Bind des touches
        self.gui.bind("<Escape>", self.quit)
        # Mainloop à la fin
        self.menu("Bienvenue dans le jeu de la bataille de boules de neige !", "#112C42")
        self.gui.mainloop()

    def menu(self, texte, color):
        self.menu_txt1 = self.canvas.create_text(self.settings["resolution"][0]/2, self.settings["resolution"][1]/4, width=self.settings["resolution"][0]*2/3, justify=CENTER, anchor=CENTER, text=texte, font=("Calibri", 35), fill=color)
        self.menu_txt2 = self.canvas.create_text(self.settings["resolution"][0]/2, self.settings["resolution"][1]*7/8, width=self.settings["resolution"][0]*2/3, justify=CENTER, anchor=CENTER, text="Appuyez sur une touche pour commencer...", font=("Calibri", 20), fill="black")
        self.gui.bind("<KeyPress>", lambda event: self.newGame())
        self.gui.unbind("<KeyPress-Left>")
        self.gui.unbind("<KeyPress-Right>")
        self.gui.unbind("<KeyPress-space>")
        self.gui.unbind("<KeyRelease-Left>")
        self.gui.unbind("<KeyRelease-Right>")
        self.gui.unbind("<KeyRelease-space>")
        self.gui.unbind("<Shift_L>")

    def newGame(self):
        self.canvas.delete(self.menu_txt1)
        self.canvas.delete(self.menu_txt2)
        self.gui.unbind("<KeyPress>")
        # Variables du jeu
        self.boules = {}
        self.timeNextBall = 0
        self.remainigTime = 60
        # Elements de l'interface
        self.clock = self.canvas.create_image(self.settings["resolution"][0]-100, 100, anchor=CENTER, image=self.images['clock'])
        self.bg1 = self.canvas.create_arc(self.settings["resolution"][0]-145, 55, self.settings["resolution"][0]-55, 145, style="arc", width=5, start=110, extent=320, outline='#787878')
        self.timer = self.canvas.create_arc(self.settings["resolution"][0]-145, 55, self.settings["resolution"][0]-55, 145, style="arc", width=10, start=110, extent=320, outline='#3DBCD8')
        self.bg2 = self.canvas.create_arc(self.settings["resolution"][0]-130, 70, self.settings["resolution"][0]-70, 130, style="arc", width=4, start=290, extent=140, outline='#787878')
        self.boost_timer = self.canvas.create_arc(self.settings["resolution"][0]-130, 70, self.settings["resolution"][0]-70, 130, style="arc", width=7, start=290, extent=140, outline='#FFF57B')
        self.bg3 = self.canvas.create_arc(self.settings["resolution"][0]-130, 70, self.settings["resolution"][0]-70, 130, style="arc", width=4, start=110, extent=140, outline='#787878')
        self.lifes = self.canvas.create_arc(self.settings["resolution"][0]-130, 70, self.settings["resolution"][0]-70, 130, style="arc", width=7, start=110, extent=140, outline='#EC7575')
        self.time = self.canvas.create_text(self.settings["resolution"][0]-100, 100, anchor=CENTER, font=("Arial", 20), fill="#E8F5F5", text="60")
        self.clock_overlay = self.canvas.create_image(self.settings["resolution"][0]-100, 100, anchor=CENTER, image=self.images['clock_overlay'])
        # Création du joueur
        self.joueur = Joueur([self.settings["resolution"][0], self.settings["resolution"][1]], [50, 400], vector=[0,0])
        self.santaImg = self.images['PereNoelDN']
        self.santa = self.canvas.create_image(self.joueur.getPos()[0], self.joueur.getPos()[1], anchor=NW, image=self.santaImg)
        # Bind des controles
        self.gui.bind("<KeyPress-Left>", lambda event: self.joueur.inputs('L', True))
        self.gui.bind("<KeyPress-Right>", lambda event: self.joueur.inputs('R', True))
        self.gui.bind("<KeyPress-space>", lambda event: self.joueur.inputs('B', True))
        self.gui.bind("<KeyRelease-Left>", lambda event: self.joueur.inputs('L', False))
        self.gui.bind("<KeyRelease-Right>", lambda event: self.joueur.inputs('R', False))
        self.gui.bind("<KeyRelease-space>", lambda event: self.joueur.inputs('B', False))
        self.gui.bind("<Shift_L>", lambda event: self.joueur.esquive())
        # On lance la boucle du jeu
        self.controls = self.canvas.create_text(self.settings["resolution"][0]/2, self.settings["resolution"][1]-25, width=self.settings["resolution"][0], justify=CENTER, anchor=CENTER, text="Contrôles : Flèches gauche et droite pour bouger - Espace pour freiner - Shift pour esquiver", font=("Calibri", 15), fill="black")
        self.countdown = self.canvas.create_text(self.settings["resolution"][0]/2, self.settings["resolution"][1]/2, width=self.settings["resolution"][0]*2/3, justify=CENTER, anchor=CENTER, text="3", font=("Calibri", 100), fill="#112C42")
        self.gui.after(1000, lambda: self.count(2))
        self.gui.after(2000, lambda: self.count(1))
        self.gui.after(3000, lambda: self.count(0))
        self.gui.after(3000, self.loop)

    def count(self, n):
        if n == 0:
            self.canvas.delete(self.countdown)
            self.canvas.delete(self.controls)
            return
        self.canvas.itemconfigure(self.countdown, text=str(n))

    def loop(self):
        if self.timeNextBall <= 0 and len(self.boules) < self.settings["maxBoules"]:
            self.createBall()
            # Fait apparître la prochaine boule a +- 50% du temps défini dans les paramètres
            self.timeNextBall = int(self.settings["BPS"] * (randint(50,150)/100) * self.settings["TPS"])
        # Met à jour les boules de neige
        boulesAChanger = []
        for boule in self.boules:
            if self.boules[boule].update():
                boulesAChanger.append(boule)
                continue
            newPosX, newPosY = self.boules[boule].getPos()
            self.canvas.moveto(boule, x=newPosX, y=newPosY)
        for e in boulesAChanger:
            if self.boules[e].getRayon() == int(min(self.settings["choixBoules"])/2):
                self.canvas.delete(e)
                del self.boules[e]
                continue
            image = self.images[self.boules[e].getRayon()]
            self.canvas.itemconfigure(e, image=image)
        # Met à jour le père noël du Joueur
        self.joueur.update()
        newPosX, newPosY = self.joueur.getPos()
        self.canvas.moveto(self.santa, x=newPosX, y=newPosY)
        if self.joueur.getVector()[0] < 0 and self.joueur.getAction()[1] == 'N' and self.joueur.getImage() != "/assets/NoelGN.gif":
            self.santaImg = self.images['PereNoelGN']
            self.canvas.itemconfigure(self.santa, image=self.santaImg)
            self.joueur.setImage()
        elif self.joueur.getVector()[0] > 0 and self.joueur.getAction()[1] == 'N' and self.joueur.getImage() != "/assets/NoelDN.gif":
            self.santaImg = self.images['PereNoelDN']
            self.canvas.itemconfigure(self.santa, image=self.santaImg)
            self.joueur.setImage()
        elif self.joueur.getVector()[0] < 0 and self.joueur.getAction()[1] == 'E' and self.joueur.getImage() != "/assets/NoelGE.gif":
            self.santaImg = self.images['PereNoelGE']
            self.canvas.itemconfigure(self.santa, image=self.santaImg)
            self.joueur.setImage()
        elif self.joueur.getVector()[0] > 0 and self.joueur.getAction()[1] == 'E' and self.joueur.getImage() != "/assets/NoelDE.gif":
            self.santaImg = self.images['PereNoelDE']
            self.canvas.itemconfigure(self.santa, image=self.santaImg)
            self.joueur.setImage()
        # On retire les points de vie en cas de collision
        boulesAEffacer = []
        for e in self.boules:
            if self.joueur.isOverlapping(self.boules[e])[0]:
                if self.boules[e].getRayon() <= 8:
                    self.joueur.perdreVie(1)
                elif self.boules[e].getRayon() == 16:
                    self.joueur.perdreVie(2)
                elif self.boules[e].getRayon() >= 32:
                    self.joueur.perdreVie(3)
                boulesAEffacer.append(e)
        # On modifie l'interface
        self.canvas.itemconfigure(self.boost_timer, extent=(90-self.joueur.getReloadEsquive())*140/90)
        self.canvas.itemconfigure(self.timer, extent=self.remainigTime/60*320)
        self.canvas.itemconfigure(self.lifes, extent=self.joueur.getVie()*140/3)
        self.canvas.itemconfigure(self.time, text=str(int(self.remainigTime)))
        # On regarde si le joueur a perdu
        if self.joueur.getVie() <= 0:
            self.gui.after(1000, lambda: self.del_all())
            self.gui.after(1000, lambda: self.menu("Dommage, vous avez perdu !", "#DA4141"))
            return
        for e in boulesAEffacer:
            self.canvas.delete(e)
            del self.boules[e]
        # On regarde si le joueur a gagné
        if self.remainigTime <= 0:
            print(self.remainigTime)
            self.canvas.itemconfigure(self.timer, extent=0)
            self.gui.after(1000, lambda: self.del_all())
            self.gui.after(1000, lambda: self.menu("Bravo, vous avez gagné !", "#52CA59"))
            return
        # On programme la boucle suivante
        self.timeNextBall -= 1
        self.remainigTime -= 1/self.settings["TPS"]
        self.gui.after(int(1000/self.settings["TPS"]), self.loop)

    def createBall(self):
        ball = self.canvas.create_image(0, 0, anchor=SW)
        self.boules[ball] = Boule(
            [self.settings["resolution"][0],self.joueur.getPos()[1]+150],
            self.settings["maxSpeed"],
            pos=[randint(0, self.settings["resolution"][0]-128), -150],
            vector=[randint(-self.settings["maxSpeed"]/2, self.settings["maxSpeed"]/2), 0],
            rayon=choice(self.settings["choixBoules"])
        )
        img = self.images[self.boules[ball].getRayon()]
        self.canvas.itemconfigure(ball, image=img)
        self.canvas.moveto(ball, x=self.boules[ball].pos[0], y=self.boules[ball].pos[1])

    def del_all(self):
        self.canvas.delete(self.santa)
        for b in self.boules:
            self.canvas.delete(b)
            del b
        self.canvas.delete(self.boost_timer)
        self.canvas.delete(self.timer)
        self.canvas.delete(self.lifes)
        self.canvas.delete(self.time)
        self.canvas.delete(self.bg1)
        self.canvas.delete(self.bg2)
        self.canvas.delete(self.bg3)
        self.canvas.delete(self.clock)
        self.canvas.delete(self.clock_overlay)
        del self.boules
        del self.joueur

    def quit(self, event=None):
        self.gui.destroy()

def main():
    Jeu = Game()

main()
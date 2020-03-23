##########################################################################
############################  Jeu Puissance 4 ############################
############################ par Florent Spriet ##########################
##########################################################################

from tkinter import *
from tkinter.messagebox import *

# Crée la Sous-Classe d'objet Canevas (terrain de jeu)

# A améliorer: On pourrait créer un objet Jeu et à l'intérieur un Canevas (là j'ai tout rattaché au Canevas) 

class Damier(Canvas):

    # initialisation

    def __init__(self, parent):
        self.parent=parent
        self.matrice=[9,9,9,9,9,9,9]*6
        self.couleur_pion=['','red','yellow','','','','','','','white']
        self.tour=1
        self.gagne=0
        self.can = Canvas.__init__(self, width = 50+700+150, height =10+600+10, bg ='gainsboro')       # on constuit le canevas
                ## !!! est-ce que je ne crée pas un canevas dans un canevas?
        self.affiche_damier()

        self.bind('<Button-1>', self.click)

        fenetre_joueur=Label(self.parent, bg ='gainsboro', text = ' Joueur:')
        fenetre_joueur.grid(row=0, column=9)

        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Nouvelle partie", command=self.redemarrer)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.quitter)
        menubar.add_cascade(label="Menu", menu=menu1)
        self.parent.config(menu=menubar)

    # affichage du damier
        
    def affiche_damier(self):
        self.create_rectangle(50,10,750,610, fill='blue')
        self.grid(row=0, column=0, rowspan=10, columnspan=10)
        self.create_oval (800, 60, 850, 110, fill=self.couleur_pion[(self.tour-1)%2+1])
        for i in range (7):
            for j in range (6):
                self.create_oval (50+i*100+10, 10+600-j*100-10, 50+i*100+90, 10+600-j*100-90, fill=self.couleur_pion[self.matrice[i+7*j]])
        texte_tour='Tour: '+str(self.tour)
        fenetre_tour=Label(self.parent, text = texte_tour, bg ='gainsboro')
        fenetre_tour.grid(row=2, column=9)
                
    # gestiond de l'evenement click souris
    
    def click(self, event):
        self.tombe_un_pion(int((event.x-50)/100), int((event.y-10)/100))
        self.affiche_damier()
        self.verifie_alignement()
                
    # positionne le point de chute du pion

    def tombe_un_pion(self, colonne_cliquee, ligne_cliquee):
        if colonne_cliquee in [0,1,2,3,4,5,6] and self.matrice[colonne_cliquee+7*5]==9 and self.gagne==0:
            j=5
            arret=False
            while arret==False:
                if self.matrice[colonne_cliquee+j*7]!=9:
                    if (5-ligne_cliquee)==(j+1):
                        self.matrice[colonne_cliquee+(j+1)*7]=(self.tour-1)%2+1
                        self.tour=self.tour+1
                    arret=True
                else:
                    if j==0:
                        if (5-ligne_cliquee)==0:
                            self.matrice[colonne_cliquee+j*7]=(self.tour-1)%2+1
                            self.tour=self.tour+1
                        arret=True
                    j=j-1
                    
    # vérifie si c'est gagné

    def verifie_alignement (self): 

        for i in range(7): #tester les alignements verticaux
            for j in range(3):
                resultat=self.matrice[i+j*7]+self.matrice[i+(j+1)*7]+self.matrice[i+(j+2)*7]+self.matrice[i+(j+3)*7]
                if resultat==4:
                    self.gagne=1
                    self.create_line(100+i*100, 560-j*100, 100+i*100, 560-(j+3)*100, width=8, fill = 'green')
                if resultat==8:
                    self.gagne=2
                    self.create_line(100+i*100, 560-j*100, 100+i*100, 560-(j+3)*100, width=8, fill = 'green')

        for j in range(6): #tester les alignements hortizontaux
            for i in range(4):
                resultat=self.matrice[i+j*7]+self.matrice[i+1+j*7]+self.matrice[i+2+j*7]+self.matrice[i+3+j*7]
                if resultat==4:
                    self.gagne=1
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-j*100, width=8, fill = 'green')
                if resultat==8:
                    self.gagne=2
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-j*100, width=8, fill = 'green')

        for i in range(4): #tester les diagonales montantes
            for j in range(3):
                resultat=self.matrice[i+j*7]+self.matrice[i+1+(j+1)*7]+self.matrice[i+2+(j+2)*7]+self.matrice[i+3+(j+3)*7]
                if resultat==4:
                    self.gagne=1
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-(j+3)*100, width=8, fill = 'green')
                if resultat==8:
                    self.gagne=2
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-(j+3)*100, width=8, fill = 'green')

        for i in range(4): #tester les diagonales descendentes
            for j in range(3,6):
                resultat=self.matrice[i+j*7]+self.matrice[i+1+(j-1)*7]+self.matrice[i+2+(j-2)*7]+self.matrice[i+3+(j-3)*7]
                if resultat==4:
                    self.gagne=1
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-(j-3)*100, width=8, fill = 'green')
                if resultat==8:
                    self.gagne=2
                    self.create_line(100+i*100, 560-j*100, 100+(i+3)*100, 560-(j-3)*100, width=8, fill = 'green')

    # Fonction Redemarrer

    def redemarrer(self):
        if askyesno('Confirmation New Game', 'Nouvelle Partie ?'):
            self.tour=1
            self.gagne=0
            self.matrice=[9,9,9,9,9,9,9]*6
            self.affiche_damier()

    # Fonction Quitter

    def quitter(self):
        if askyesno('Confirmation Quitter', 'Quitter vraiment ?'):
            self.parent.destroy()

#Programme principal

Fenetre_Jeu = Tk()
Fenetre_Jeu.title("Puissance 4")
DamierEnCours=Damier(Fenetre_Jeu)
Fenetre_Jeu.mainloop()

    

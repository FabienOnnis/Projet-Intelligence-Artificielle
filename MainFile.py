from tkinter import *
from tkinter.ttk import *
import copy
import sqlite3

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):

        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.grid(row=0, column=0)

        # Initialisation des variables utiles à la disposition des widgets
        self.MaxRow              = 10
        self.MaxColumn           = 4
        self.WidthComboboxWidget = 50

        # Initialisation des tableaux nécessaires à l'update des widgets et leur sauvegarde
        self.listeWidgetCombobox    = []
        self.listeVariablesCombobox = []
        self.matriceDesSymptomes    = []

        # Lecture du fichier texte qui contient nôtre base de données
        # Enregistrement des noms des symptômes et des noms de maladies trouvés
        with open("BaseDeDonnees.txt", "r", encoding="utf-8") as base :
            self.listeSymptomes = base.readline()
            self.listeMaladies = base.readline()
            for line in base :
                newLine = line.rstrip('\n').split(",")
                newLine = [int(x) for x in newLine]
                self.matriceDesSymptomes.append(newLine)

        self.listeSymptomes         = self.listeSymptomes.rstrip('\n').split(",") + ["Supprimer le symptome"]
        self.listeMaladies          = self.listeMaladies.rstrip('\n').split(",")
        self.listeSymptomesRestants = copy.deepcopy(self.listeSymptomes)

        # Création de la base données SQL pour une recherche plus simple de la possible maladie
        self.connection = sqlite3.connect('BaseDeDonnees.db')
        self.c          = self.connection.cursor()

        try :
            self.c.execute("DROP TABLE Maladies")
        except :
            pass

        instantListForTable = self.listeSymptomes[:-1]
        self.c.execute("CREATE TABLE Maladies " + str(tuple(instantListForTable)))

        # On insère toutes les données dans la table Maladies
        for i,maladie in enumerate(self.listeMaladies) :
            newLine = tuple([maladie]) + tuple(self.matriceDesSymptomes[i])
            self.c.execute("INSERT INTO Maladies VALUES " + str(newLine))

        # Afficher toutes les données ont été insérées pour les vérifier rapidement
        for row in self.c.execute("SELECT * FROM Maladies") :
            print(row)

        # Widgets Bouton
        self.AjouterNouveauSymptomeButton = Button(self.parent, text="Ajouter un symptome", command=self.AjouterNouveauSymptome)
        self.AjouterNouveauSymptomeButton.grid(row=self.MaxRow, column=0)

        self.GetButton = Button(self.parent, text="Trouver la maladie", command=self.GetValuesCombobox)
        self.GetButton.grid(row=self.MaxRow+1, column=0)

        #self.listeSymptomes.remove("Name")

    def updateListeSymptomesRestants(self, event=None):

        ####################################################################################
        # Cette fonction va à chaque fois qu'on va sélectionner un symptôme dans une liste #
        # déroulante, mettre à jour toutes les autres listes afin de ne pas pouvoir        #
        # sélectionner deux fois le même symmptôme.                                        #
        ####################################################################################

        self.listeSymptomesRestants = copy.deepcopy(self.listeSymptomes)

        for i,symptome in enumerate(self.listeVariablesCombobox) :
            if symptome.get() == "Supprimer le symptome" :
                self.listeWidgetCombobox[i].destroy()
                self.listeWidgetCombobox.pop(i)
                self.listeVariablesCombobox.pop(i)
            else :
                self.listeSymptomesRestants.remove(symptome.get())

        for i,comboboxWidget in enumerate(self.listeWidgetCombobox) :
            comboboxWidget.config(values=self.listeSymptomesRestants)
            comboboxWidget.update()

    def AjouterNouveauSymptome(self):

        #####################################################################################
        # Cette fonction va ajouter une nouvelle liste déroulante afin d'ajouter un nouveau #
        # symptôme. Il y a donc une mise à jour des différentes liste et une réorganisation #
        # de la place des widgets dans la fenêtre.                                          #
        #####################################################################################

        if len(self.listeWidgetCombobox) < self.MaxColumn*self.MaxRow :
            newVar = StringVar()

            newCombobox = Combobox(self, textvariable=newVar, values=self.listeSymptomesRestants, state='readonly', width=self.WidthComboboxWidget)
            newCombobox.current(0)
            newCombobox.bind('<<ComboboxSelected>>', self.updateListeSymptomesRestants)
            newCombobox.grid(row=len(self.listeWidgetCombobox)//self.MaxColumn, column=len(self.listeWidgetCombobox)%self.MaxColumn)


            self.listeWidgetCombobox.append(newCombobox)
            self.listeVariablesCombobox.append(newVar)

            self.updateListeSymptomesRestants()

        else :
            print("Nombre maximum de symptomes atteint...")

    def GetValuesCombobox(self):

        ####################################################################################
        # Cette fonction va être appelée à chaque fois que l'on appuie sur le bouton de    #
        # validation. Nous allons donc récapituler les symptômes entrés par l'utilisateur  #
        # appeler une fonction de traitement de l'information s'ils sont valides           #
        ####################################################################################

        if len(self.listeWidgetCombobox) == 0 :
            print("\nAucun symptôme n'a été entré, veuillez en entrer au moins 1 !\n")

        else :
            print("\nrécapitulatif des symptômes entrés : ")
            for box in self.listeVariablesCombobox :
                print("    - " + box.get())
            print("\n")
            self.informationTreatment()

    def informationTreatment(self):

        self.listeSymptomesNonValides = copy.deepcopy(self.listeSymptomesRestants)
        self.listeSymptomesNonValides.remove("Supprimer le symptome")
        self.listeSymptomesValides = [symptome for symptome in self.listeSymptomes if symptome not in self.listeSymptomesRestants]

        print(self.listeSymptomesNonValides)
        print(self.listeSymptomesValides)

        requete = "SELECT * FROM Maladies WHERE"
        for i,symptomeValide in enumerate(self.listeSymptomesValides) :
            if i < len(self.listeSymptomesValides)-1 :
                requete += " " + symptomeValide + " = 1 AND"
            else :
                requete += " " + symptomeValide + " = 1"

        print("\nRequête formulée :\n")
        print(requete + "\nRésultat de la requête :\n")

        for row in self.c.execute(requete) :
            print(row)

        print(self.c.description)



if __name__ == "__main__" :

    root = Tk()
    MainApplication(root).grid()
    root.mainloop()

from tkinter import *
from random import randrange, randint
from time import sleep


class Grille(Canvas):
    """
    Spécialisation et configuration d'un Canvas tkinter pour la gestion d'une grille
    comportant nb_lig lignes et nb_colonnes, des marges haut, droite, bas, gauche potentiellement différentes
    une taille de case de largeur et de longueur potentiellement différentes
    """

    NORD, EST, SUD, OUEST = 0, 1, 2, 3  # les 4 directions de la grille en attributs de classe

    def __init__(self, fen, nb_lig, nb_col, t_marges=(0, 0, 0, 0), t_case=(20, 20), **kw):
        """
        Création des attributs privés :
        - nb_lig et nb_col : nombre de lignes et de colonnes de la grille
        - nb_cases, t_case : nombre de cases et taille en pixel de la largeur et hauteur d'une case
        - t_marges : valeur des marges haut, droite, bas puis gauche
        - width, height : largeur et hauteur en pixel de la grille
        """
        self.__nb_lig= nb_lig
        self.__nb_col = nb_col
        self.__nb_cases = nb_lig * nb_col
        self.__t_case = t_case   
        self.__t_marges = t_marges   #pourquoi ne pas utiliser le qui est dans les parametres?
        self.__width = self.__t_case[1] * nb_col
        self.__height = self.__t_case[0] * nb_lig

    

        Canvas.__init__(self, fen, width = self.__width, height = self.__height, bg = "black",  **kw)

    def get_nb_lig(self):
        return self.__nb_lig
        
        """ Accesseur en lecture du nombre de lignes"""

    def get_nb_col(self):
        return self.__nb_col
        """ Accesseur en lecture du nombre de colonnes"""

    def get_nb_cases(self):
        return self.__nb_cases
        """ Accesseur en lecture du nombre de cases"""

    def case_to_lc(self, num_case):
        return num_case // self.__nb_col, num_case % self.__nb_col
        """Calcul des numéros de ligne et de colonne à partir du numéro de case"""

    def lc_to_case(self, num_lig, num_col):    #redondance de numéro de case
        return num_lig * self.__nb_col + num_col
        """Calcul du numéro de case à partir des numéros de ligne et de colonne"""

    def case_to_xy(self, num_case):
        x = self.__t_marges[0] + (num_case%self.__nb_col)*self.__t_case[0]
        y = self.__t_marges[1] + (num_case//self.__nb_col)*self.__t_case[1]
        return x, y

        """Calcul des coordonnées en pixel à partir du numéro de case"""

    def xy_to_case(self, x, y):
        return (y//self.__t_case[0])*self.__nb_col + (x//self.__t_case[1])
        """Calcul du numéro de case à partir des coordonnées en pixel"""

    def xy_to_lc(self, x, y):
        return (x // self.__t_case[0])-1, (y // self.__t_case[1])-1
        """Calcul des numéros de ligne et de colonne à partir des coordonnées en pixel"""

    def lc_to_xy(self, num_lig, num_col):
        return num_col * self.__t_case, num_lig * self.__t_case
        """Calcul des coordonnées en pixel à partir des numéros de ligne et de colonne"""

    def next_case(self, num_case, direction, nb_cases=1):  # sur un tore
        """Calcul du numéro de case suivant lorque nb cases sont ajoutés dans une direction donnée
        Le déplacement d'effectue sur la grille considérée comme un tore (la sortie du serpent par un côté
        entraine la sortie du serpent par le côté opposé."""
        lig, col= self.case_to_lc(num_case) # tuple(ligne, colonne)  coordoné de case
        if direction == Grille.NORD:
            if lig == 0:
                lig = self.__nb_lig-1
                return self.lc_to_case(lig,col)
            else:
                return self.lc_to_case(lig-1,col)

        elif direction == Grille.EST:
            if col == self.__nb_col-1:
                col = 0
                return self.lc_to_case(lig,col)
            else:
                return self.lc_to_case(lig,col+1)

        elif direction == Grille.SUD:
            if lig == self.__nb_lig-1:
                lig = 0
                return self.lc_to_case(lig,col)
            else:
                return self.lc_to_case(lig+1,col)

        else: #OUEST
            if col == 0:
                col = self.__nb_col-1
                return self.lc_to_case(lig,col)
            else:
                return self.lc_to_case(lig,col-1)


    def show_case(self, num_case, color= "#f40a0a"):
        """ crée et retourne l'identifiant d'un rectangle de couleur color pour visualiser la case de numéro num_case"""
        x,y=self.case_to_xy(num_case)
        return self.create_oval(x, y, x + self.__t_case[0], y + self.__t_case[0] , fill = color)


class GrilleSnake(Grille):
    """
    Spécialisation et configuration d'une Grille pour la gestion d'une grille
    comportant nb_lig lignes et nb_colonnes, des marges haut, droite, bas, gauche identiques
    une taille de case de largeur et de longueur identiques et la gestion d'un serpent
    """

    TWO_KEYS_MODE = True  # paramétrage du mode de jeu

    def __init__(self, fen, nb_lig, nb_col, t_marges=0, t_case=5, color_snake='green', **kw):
        Grille.__init__(self,fen, nb_lig, nb_col)
        """
        En plus des attributs hérités, création des attributs publics :
        color_snake : couleur du serpent
        - t_snake : nombre de cases du serpent
        - dir_snake : direction du serpent
        - pos_snake : numéro de case de la tête du serpent
        - snake : liste de liste de deux éléments [case élément serpent, identifiant du dessin de l'élément]
        - speed_snake : vitesse du serpent
        Le constructeur dessine le serpent dans le Canvas
        et associe à tous les éléments graphiques les éléménts graphiques les évènements clavier et souris
        """
        self.color_snake = color_snake
        self.t_snake = 6
        self.dir_snake = randrange(0,3)
        self.pos_snake = randint(0,self.get_nb_cases())
        self.snake = []
        for i in range(self.t_snake):
            num_case = self.pos_snake - i
            x,y = self.case_to_xy(num_case)
            self.snake.append([num_case, self.create_oval(x,y,x+20, y+20, fill = self.color_snake)])
        self.speed_snake = 5


    def turn_left_snake(self):
        """ Mode de jeu deux déplacement relatif
        handler de l'évènement bouton gauche ou flêche gauche
        modifie la direction de 180° vers la gauche"""
        if self.dir_snake == Grille.NORD:
            self.dir_snake = Grille.OUEST
        elif self.dir_snake == Grille.OUEST:
            self.dir_snake = Grille.SUD
        elif self.dir_snake == Grille.SUD:
            self.dir_snake = Grille.OUEST
        else:
            self.dir_snake = Grille.NORD

    def turn_right_snake(self):
        """ Mode de jeu deux déplacement relatif
        handler de l'évènement bouton droit ou flêche droite
        modifie la direction de 180° vers la droite"""
        if self.dir_snake == Grille.NORD:
            self.dir_snake = Grille.EST
        elif self.dir_snake == Grille.EST:
            self.dir_snake = Grille.SUD
        elif self.dir_snake == Grille.SUD:
            self.dir_snake = Grille.EST
        else:
            self.dir_snake = Grille.NORD

    def turn_snake(self, event):
        print(event.keysym)
        """ Mode de jeu deux déplacement absolu
        handler des évènements clavier haut, droite, bas ou gauche
        définit la direction dans le sens de la touche clavier choisie"""
        if self.dir_snake == Grille.NORD:
            if event.keysym == "Left":
                self.turn_left_snake()
            elif event.keysym == "Right":
                self.turn_right_snake()            
            else: 
                pass
        elif self.dir_snake == Grille.EST:
            if event.keysym == "Down":
                self.turn_right_snake()
            elif event.keysym == "Up":
                self.turn_left_snake()            
            else: 
                pass

        elif self.dir_snake == Grille.SUD:
            if event.keysym == "Left":
                self.turn_left_snake()
            elif event.keysym == "Right":
                self.turn_right_snake()            
            else: 
                pass

        else:            
            if event.keysym == "Up":
                self.turn_right_snake()
            elif event.keysym == "Down":
                self.turn_left_snake()            
            else: 
                pass 

    def crawling_snake(self):

        num_case = self.t_snake*[0] #liste de liste de la nouvelle et acienne position de chaque element du snake
        
        for i in range(self.t_snake):
            if i == 0:
                num_case[i] = self.snake[i][0]
                self.snake[i][0] =self.next_case(self.snake[i][0], self.dir_snake)
                x,y = self.case_to_xy(self.snake[i][0])
                self.pos_snake = self.snake[i][0]
            else:
                num_case[i] = self.snake[i][0]
                self.snake[i][0] = num_case[i-1]
                x,y = self.case_to_xy(self.snake[i][0])
            self.snake[i] = [self.snake[i][0],self.snake[i][1] ]
            self.coords(self.snake[i][1], x, y, x+20, y+20)            
        


        """Avancement du serpent (déplacement de la queue vers la case suivant la tete dans la direction courante)"""



class FenApp(Tk):
    """ Spécialisation et configuration de la fenêtre d'application
    Les attributs de classe fixent le nombre de lignes et de colonnes,
    la valeur des marges et de la taille en pixel d'une case,
    le jeu de couleurs utilisées dans l'application (fond de la grille et couleur du serpent)
    """

    NB_LIG = 30
    NB_COL = 50
    MARGES = 0
    T_CASE = 5
    COULS = {'fond': 'black', 'serpent': 'orange'}

    def __init__(self):
        """Placement des éléments d'interface et création des attributs publics :
        - monde : il s'agit d'une GrilleSnake initialisée grâce aux attributs de classe
        - b_launch : bouton pour lancer le déplacement du serpent
        - b_leave : bouton pour quitter l'application
        - end_game, moving : booléens pour savoir si le jeu est terminé ou si le serpent est en mode déplacement
        Le constructeur associera également un handler à l'évènement barre espace
        pour gérer la pause ou la reprise des déplacements du serpent"""
        Tk.__init__(self)

        self.monde = GrilleSnake(self, nb_lig = FenApp.NB_LIG, nb_col = FenApp.NB_COL, t_marges=FenApp.MARGES, t_case=FenApp.T_CASE, color_snake = FenApp.COULS["serpent"] )
        self.monde.pack(side = TOP, padx = FenApp.MARGES, pady = FenApp.MARGES)
        self.monde.configure(bg = FenApp.COULS["fond"])

        self.panel = Frame(self, width = 100, height = 50 )

        self.b_lunch = Button(self.panel, text='Lancer', command=self.launch)
        self.b_lunch.pack(side = LEFT)

        self.bind("<space>", self.stop)
        self.bind("<KeyPress>", self.monde.turn_snake ) 

        self.b_stop = Button(self.panel, text='Pause', command =self.stop )
        self.b_stop.pack(side = LEFT, padx = 10)

        self.b_leave = Button(self.panel, text='Quitter', command=self.leave)
        self.b_leave.pack(side = LEFT)
        self.panel.pack(side = BOTTOM, padx = 150)
        self.end_game = 0
        

    def launch(self):
        print(self.end_game)
        while 1:
            if not self.end_game:
                self.monde.crawling_snake()
                self.b_lunch.configure(state = DISABLED)
                sleep(self.monde.speed_snake / 50)
            else:
                break
            self.update()

            
        
        """handler du bouton de lancement. Réalise une boucle d'avancement du serpent
        tant que le jeu n'est pas terminé et si le serpent est en mode déplacement.
        La fonction devra également desactiver la possibilité d'actionner le bouton de lancement.
        Attention, les éléments graphiques sont mis à jour par défaut APRES la boucle.
        Pour que les modifications tkinter soient visibles PENDANT la boucle il faut utiliser
        la méthode update() sur la fenêtre."""

    def stop(self, event = 0):
        """handler de la touche space qui inverse le mode déplacement du serpent"""
        if not self.end_game:
            self.b_stop.configure(text = "Reprendre")
            self.end_game = 1
            
        else:
            self.end_game = 0
            self.b_stop.configure(text = "Pause")
            self.launch()

    def leave(self):
        """ handler du bouton qui permet de quitter l'application"""
        self.destroy()


if __name__ == "__main__":
    """ lancement de l'application et de la boucle évenementielle"""
    FenApp().mainloop()

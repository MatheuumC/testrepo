# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 18:02:26 2020

@author: Mathieu
"""

import os
import gc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.use("Qt5Agg")
from scipy import stats
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import datetime

class Astre():
    
    def __init__(self, nom): # Notre méthode constructeur
        """Constructeur de notre classe. Chaque attribut va être instancié
        avec une valeur par défaut"""
        self.nom = nom
        self.masse = 0 
        self.couleur = "" 
        self.position = []
        self.vitesse = []
        self.save = True
        self.taille = 0
        self.periode=0
        self.aire1=0      #Aire balayée dpuis un temps t1
        self.aire2=0      #Aire balayée depuis un temps t2
        self.angle=0      #Agnle balayé depuis le début
        self.dmin=10**9   #Distance minimale au soleil
        self.dmax=0     #Distance maximale au soleil
        self.demi_grand_axe=10**9
        

class Etoile(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "o" 
        self.save = False

class Planete(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "o" 

class Asteroide(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "p" 

class Satellite(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "H" 

class Comete(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "^" 

class Sonde(Astre):
    def __init__(self, nom):
        """Un agent se définit par son nom et son matricule"""
        Astre.__init__(self, nom)
        self.forme = "1" 

#constante gravitationnelle (l'unité est en UA pour les distances, en jour pour le temps, et en masse solaire pour la masse)
G=2.95912208286*pow(10,-4)

#######################################################################################################################
#Création des Astres

#Etoile
Soleil= Etoile("Soleil")

#Planètes
Mercure=Planete("Mercure")
Venus=Planete("Vénus")
Terre= Planete("Terre")
Mars= Planete("Mars")
Jupiter= Planete("Jupiter")
Saturne= Planete("Saturne")
Uranus= Planete("Uranus")
Neptune= Planete("Neptune")

#Satellites naturels et Planètes naines
Lune=Satellite("Lune")
Phobos=Satellite("Phobos")
Deimos=Satellite("Deimos")
Ganymede=Satellite("Ganymede")
Europe=Satellite("Europe")
Io=Satellite("Io")
Callisto=Satellite("Callisto")
Titan=Satellite("Titan")
Pluton=Satellite("Pluton")

#Asteroide
Eros=Asteroide("Eros")
Ceres=Asteroide("Ceres")
Benou=Asteroide("Bénou")

#Sonde
Juno = Satellite("Juno")
Test= Satellite("Test")

#Comete
Halley = Comete("Halley")

###########################################################################################################################
#Save = prise en compte de l'astre dans les calculs

#Planètes
Mercure.save=True
Venus.save=True
Terre.save=True
Mars.save=True
Jupiter.save=True
Saturne.save=True
Uranus.save=True
Neptune.save=True

#Satellites naturels et Planètes naines
Lune.save=False
Phobos.save=False
Deimos.save=False
Ganymede.save=False
Europe.save=False
Io.save=False
Callisto.save=False
Titan.save=False
Pluton.save=False

#Asteroides
Eros.save=False
Ceres.save=False
Benou.save=False

#Sondes
Juno.save=False
Test.save=False

#Cometes
Halley.save=False

###########################################################################################################################
#masse des astres https://promenade.imcce.fr/fr/pages5/557.html

Mercure.masse=1.660137*pow(10,-7)
Venus.masse=2.4478383*pow(10,-6)
Terre.masse= 3.0034896*pow(10,-6)
Mars.masse=3.2271514*pow(10,-7)
Jupiter.masse= 9.5459429*pow(10,-4)  #9.5479193*pow(10,-4) masse du systeme jupiter
Saturne.masse= 2.85815*pow(10,-4)          
Uranus.masse= 4.365785*pow(10,-5)
Neptune.massee= 5.150314*pow(10,-5)
Pluton.masse=6.225*pow(10,-9)
Soleil.masse=1.0
Lune.masse=1.23/100.0*Terre.masse

############################################################################################################################
#couleur des planètes
Soleil.couleur="yellow"
Mercure.couleur="silver"
Venus.couleur="wheat"
Terre.couleur="dodgerblue"
Mars.couleur="darkorange"
Jupiter.couleur="darksalmon"
Saturne.couleur="khaki"
Uranus.couleur="aquamarine"
Neptune.couleur="cornflowerblue"
Pluton.couleur="gainsboro"
Soleil.couleur="yellow"
Lune.couleur="whitesmoke"
Phobos.couleur="darkgrey"
Deimos.couleur="wheat"
Ganymede.couleur="mediumblue"
Europe.couleur="antiquewhite"
Io.couleur="yellow"
Callisto.couleur="peru"
Titan.couleur="aqua"
Eros.couleur="dimgray"
Ceres.couleur="white"
Halley.couleur="white"
Juno.couleur="lime"
Benou.couleur="blueviolet"
Test.couleur="grey"

##############################################################################################################################
#positions et vitesses initiales (01 janvier 2020, site Myriade pour les éphémérides, unités : jour, UA), http://vo.imcce.fr/webservices/miriade/?forms

Mercure.position=np.array([-0.0633170783382,-0.4101501195201,-0.2125357615980],dtype="float32")
Mercure.vitesse=np.array([0.0222283157865,-0.0013117496249,-0.0030048713731],dtype="float32")

Venus.position=np.array([0.7231990609799,0.0645407701796,-0.0167192662329],dtype="float32")
Venus.vitesse=np.array([-0.0015477128302,0.0182790958471,0.0083226313787],dtype="float32")

Terre.position=np.array([-0.1663595623113,0.8891647961638,0.3854551529860],dtype="float32")
Terre.vitesse=np.array([-0.0172391514783,-0.0027358829691,-0.0011856867915],dtype="float32")

poussée_initiale=1.1
Test.position=np.array([-0.1663595623113,0.8891647961638,0.3854551529860+6400/150000000],dtype="float32")
Test.vitesse=poussée_initiale*Terre.vitesse

Mars.position=np.array([-1.3201009441804,-0.8181749957349,-0.3396497839028],dtype="float32")
Mars.vitesse=np.array([0.0083209325496,	-0.0093945798015,-0.0045336165082],dtype="float32")

Jupiter.position=np.array([0.5261530555269,-4.7757550215624,-2.0598286526820],dtype="float32")
Jupiter.vitesse=np.array([0.0074243327181,0.0010925892443,0.0002875858498],dtype="float32")

Saturne.position=np.array([3.7972467272172,-8.5257703800632,-3.6851114946858],dtype="float32")
Saturne.vitesse=np.array([0.0048634041748,0.0020150112434,0.0006229788963],dtype="float32")

Uranus.position=np.array([16.2255023966685,10.5068427182090,4.3722864215545],dtype="float32")
Uranus.vitesse=np.array([-0.0022801895895,0.0027710319870,0.0012457424154],dtype="float32")

Neptune.position=np.array([29.2428146663157,-5.6258233307248,-3.0308157813589],dtype="float32")
Neptune.vitesse=np.array([0.0006547068462,0.0028645326952,0.0011561735053],dtype="float32")

Pluton.position=np.array([12.9767215614349,-28.6238297735950,-12.8421616733506],dtype="float32")
Pluton.vitesse=np.array([0.0029803976376,0.0008543823413,-0.0006288658780],dtype="float32")

Lune.position=np.array([-0.1637512174289,0.8886536776756,0.3849825451358],dtype="float32")
Lune.vitesse=np.array([-0.0170955952154,-0.0022319766262,-0.0009892656414],dtype="float32")

Phobos.position=np.array([-1.3201166273033,-0.8181245630763,-0.3396157689603],dtype="float32")
Phobos.vitesse=np.array([0.0072472747132,-0.0099134141045,-0.0042254645287],dtype="float32")

Deimos.position=np.array([-1.3200197962365,-0.8182707189064,-0.3397438370085],dtype="float32")
Deimos.vitesse=np.array([0.0089048453368,-0.0088774306066,-0.0045559314212],dtype="float32")

Ganymede.position=np.array([0.5196540339194,-4.7784407703309,-2.0612123650055],dtype="float32")
Ganymede.vitesse=np.array([0.0100747709345,-0.0040499533151,-0.0021375960575],dtype="float32")

Europe.position=np.array([0.5217076829591,-4.7759752985297,-2.0600387170863],dtype="float32")
Europe.vitesse=np.array([0.0079945469928,-0.0060896476672,-0.0031657271149],dtype="float32")

Io.position=np.array([0.5284022339825,-4.7772993855218,-2.0605300264428],dtype="float32")
Io.vitesse=np.array([0.0134231328487,0.0082955294748,0.0038247886981],dtype="float32")

Callisto.position=np.array([0.5363573909951,-4.7823670657413,-2.0627949722820],dtype="float32")
Callisto.vitesse=np.array([0.0101637009251,0.0046020256518,0.0019831254595],dtype="float32")

Titan.position=np.array([3.7889711069504,-8.5244786608084,-3.6844645276897],dtype="float32")
Titan.vitesse=np.array([0.0044116852695,-0.0010701877410,0.0008696519249],dtype="float32")

Eros.position=np.array([1.0818412436594,-1.3060489540412,-0.5462167115629],dtype="float32")
Eros.vitesse=np.array([0.0087090597579,0.0055653172849,0.0047342590882],dtype="float32")

Ceres.position=np.array([1.0076149633769,-2.3900624360287,-1.3321248123582],dtype="float32")
Ceres.vitesse=np.array([0.0092017156530,0.0033703986218,-0.0002850228136],dtype="float32")

Halley.position=np.array([-20.3059373684964,28.3582456156261,1.4272836307147],dtype="float32")
Halley.vitesse=np.array([0.0002256901396,0.0005493497857,0.0001979205702],dtype="float32")

Juno.position=np.array([-0.9704118826173,0.1833252520109,0.0797218600850],dtype="float32")     #pas encore disponible pour les sondes
Juno.vitesse=np.array([-0.0033291296343,-0.0151930285256,-0.0065700066915],dtype="float32")   #pas encore disponible pour les sondes
  
Benou.position=np.array([1.0024275462019,-0.3476816166724,-0.2007080312076],dtype="float32")
Benou.vitesse=np.array([0.0030214265326,0.0144725199194,0.0081652729358],dtype="float32")

################################################################################################################################
#On répertorie dans une liste tous les astres ui nous intéresse

liste_Astres=[o for o in gc.get_objects() if isinstance(o, Astre)] #On répertorie dans une liste tous les astres que l'on a crée

liste_Astres_Restants=[o for o in liste_Astres if o.save==True] #On garde pour les calculs et le plot seulement les astres qui nous intéresse


#Construction du vecteur position / vitesse des planètes qui nous intéresse
X_init=[]

for o in liste_Astres_Restants:
    X_init=np.concatenate((X_init,o.position), axis=None)
    X_init=np.concatenate((X_init,o.vitesse), axis=None)

#################################################################################################################################
#fonction qui calcul f(X) = X'   

def f(X):
    f = X.copy() #sinon cela alloue la même case mémoire pour les deux variables qui seront forcées à être égales ...
    for num_select, astre_select in enumerate(liste_Astres_Restants): # On séléctionne un par un les astres où on doit calculer les vitesses et accélérations
        
        f[6*num_select:6*num_select+3]=X[6*num_select+3:6*num_select+6] # Les vitesses du vecteur X sont mises dans les nouvelles cases de f(X)
        f[6*num_select+3:6*num_select+6]=0 #On met à zéro les compteurs
        
        for num_interact, astre_interact in enumerate(liste_Astres_Restants):  # On calcule les accélérations pour chaques coordonnées de l'astre séléctionnée
            if num_interact !=num_select : # On somme sur tous les astres sauf celui ou on a le même numero
                d=X[6*num_select:6*num_select+3]-X[6*num_interact:6*num_interact+3] #On boucle sur tous les autres astres pour avoir la somme des forces. Il nous faut déja la distance à l'astre
                d=pow(np.vdot(d.T,d.T),1/2) #calcul de la distance entre l'astre choisi et les autres astres
                di=X[6*num_interact:6*num_interact+3] #Distance au soleil de astre_interact
                di=pow(np.vdot(di.T,di.T),1/2) #calcul de la distance entre l'astre choisi et les autres astres

                f[6*num_select+3:6*num_select+6]+=-1*G*astre_interact.masse*((X[6*num_select:6*num_select+3]-X[6*num_interact:6*num_interact+3])/pow(d,3)+X[6*num_interact:6*num_interact+3]/pow(di,3)) #Correction du second terme http://lal.univ-lille1.fr/m316/cours_m316.pdf ou https://www.f-legrand.fr/scidoc/docimg/sciphys/meca/planetes/planetes.html
            else:                                    #si la planète a le même num_interactéro on ajoute l'accélération du au soleil (on le fait u'un fois comme ça)  
                d=X[6*num_select:6*num_select+3]    # les coordonnées du soleil sont considérées à 0
                d=pow(np.vdot(d.T,d.T),1/2)

                f[6*num_select+3:6*num_select+6]+=-1*G*(Soleil.masse+astre_select.masse)*X[6*num_select:6*num_select+3]/pow(d,3)
    return f

###################################################################################################################################
#Méthodes de Résolution d'EDO

def Euler(Xn, pas,tolerance=1):
    return Xn+ pas*f(Xn)

def RK2(Xn, pas,tolerance=1):
    k1=f(Xn)
    k2=f(Xn+pas/2*k1)
    return Xn+pas*k2

def RK3(Xn,pas,tolerance=1):
    k1=f(Xn)
    k2=f(Xn+pas*k1/2)
    k3=f(Xn-pas*k1+2*pas*k2)
    return Xn+ pas*(k1/6+2/3*k2+k3/6)

def RK4(Xn, pas,tolerance=1):
    k1=f(Xn)
    k2=f(Xn+pas/2*k1)
    k3=f(Xn+pas/2*k2)
    k4=f(Xn+pas*k3)
    return Xn+pas/6*(k1+2*k2+2*k3+k4)

def RK5(Xn, pas,tolerance=1):
    k1=f(Xn)
    k2=f(Xn+k1/4*pas)
    k3=f(Xn+pas*3/32*k1)
    k4=f(Xn-k2*pas/2+k3*pas)
    k5=f(Xn+3/16*k1*pas+9/16*k4*pas)
    k6=f(Xn-3/7*k1*pas+2/7*k2*pas+12/7*k3*pas-12/7*k4*pas+8/7*k5*pas)
    return Xn+1/90*(7*k1+32*k3+12*k4+32*k5+7*k6)*pas

def RK45(Xn, pas, tolerance=1):   #RK4(5) Formule 2, pas adaptatif avec contrôle de l'erreur, Wikipédia

    validity=False
    while validity==False:

        k1=pas*f(Xn)
        k2=pas*f(Xn+1/4*k1)
        k3=pas*f(Xn+3/32*k1+9/32*k2)
        k4=pas*f(Xn+1932/2197*k1-7200/2197*k2+7296/2197*k3)
        k5=pas*f(Xn+439/216*k1-8*k2+3680/513*k3-845/4104*k4)
        k6=pas*f(Xn-8/27*k1+2*k2-3544/2565*k3+1859/4104*k4-11/40*k5)
        
        Total_error=np.max(1/360*k1-128/4275*k3-2187/75240*k4+1/50*k5+2/55*k6)    
        print(Total_error)
        
        if Total_error< tolerance:
            validity=True
 
        else:
            pas = 0.9* pas* pow(tolerance/Total_error,1/5)
    
    return Xn+16/135*k1+6656/12825*k3+28561/56430*k4-9/50*k5+2/55*k6

# On crée un dictionnaire des méthodes de résolutions disponibles
methodes = {}
methodes["Euler"] = Euler # on ne met pas les parenthèses
methodes["RK2"] = RK2
methodes["RK3"] = RK3
methodes["RK4"] = RK4
methodes["RK5"] = RK5
methodes["RK45"] = RK45

#######################################################################################################################################
#Sauvegarde des résultats dans un fichier texte

def save_trajectoire(methode,t_init,t_final,pas,X_init,tolerance=1) :
    X=X_init.copy()
    with open(methode+'.txt', 'w') as mon_fichier:
        for i in np.arange(t_init,t_final+pas,pas):
            np.savetxt(mon_fichier,X.reshape(1,X.shape[0])) #On est obligé de passer d'un tableau  à "20 lignes" à un tableau à 1 ligne et 20 colonnes
            X=methodes[methode](X,pas,tolerance)  
    print(mon_fichier.closed)

########################################################################################################################################

def plot_lines(methode,t_init,t_final,pas,X_init,tolerance=1):
    save_trajectoire(methode,t_init,t_final,pas,X_init,tolerance)
    # on configure les axes, le 3D, le fond ...
    fig_tout = plt.figure()
    ax_tout = plt.axes(projection='3d')
    fig_tout.set_facecolor('black')
    ax_tout.set_facecolor('black')
    ax_tout.grid(False)
    ax_tout.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax_tout.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax_tout.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax_tout.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)
    ax_tout.text(0,0,0,"  "+ Soleil.nom, fontsize=9, color=Soleil.couleur)
    #On plot toutes les planètes restantes que l'on a choisie au début
    for num,astre in enumerate(liste_Astres_Restants):
        c1, c2, c3 = [], [], [] #On initialise les coordonnées
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            c1.append(values[6*num]) 
            c2.append(values[6*num+1])
            c3.append(values[6*num+2])
        ax_tout.plot3D(c1, c2, c3, color=astre.couleur) #On plot la trajectoire
        ax_tout.scatter(c1[-1],c2[-1],c3[-1], color=astre.couleur, label= astre.nom) #On plot la planète
        ax_tout.text(c1[-1],c2[-1], c3[-1],"  "+astre.nom, fontsize=9, color=astre.couleur) #On plot le nom de la planète
    ax_tout.legend(fancybox=True)
    plt.legend(loc='lower right')
    plt.title("SYSTEME SOLAIRE \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white')
    ax_tout.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax_tout.set_xbound(-20, +20)
    ax_tout.set_ybound(-20, +20)
    ax_tout.set_zbound(-20, +20)

##################################################################################################################################"
#Animation centrée sur la Terre

def animation_earthmoon(methode,t_init,t_final,pas,X_init,save):

    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
    plt.title("SYSTEME TERRE LUNE \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-20, +20)
    ax.set_ybound(-20, +20)
    ax.set_zbound(-20, +20)

    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
       
            if astre.nom=="Terre":
                ax.set_xlim(-0.02+M[3*num+0,i], 0.02+M[3*num+0,i])  #Référentiel en mouvement, changement du repère
                ax.set_ylim(-0.02+M[3*num+1,i], 0.02+M[3*num+1,i])
                ax.set_zlim(-0.02+M[3*num+2,i], 0.02+M[3*num+2,i])
        
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    ani.save('Animation_Terre Lune.mp4', fps=20, extra_args=['-vcodec', 'libx264'], bitrate=7200) 
    plt.show()

############################################################################################################################################
#Animation centrée sur Mars

def animation_mars(methode,t_init,t_final,pas,X_init,save):
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
    plt.title("SYSTEME MARS \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-20, +20)
    ax.set_ybound(-20, +20)
    ax.set_zbound(-20, +20)

    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
       
            if astre.nom=="Mars":
                ax.set_xlim(-0.001+M[3*num+0,i], 0.001+M[3*num+0,i])  #Référentiel en mouvement, changement du repère
                ax.set_ylim(-0.001+M[3*num+1,i], 0.001+M[3*num+1,i])
                ax.set_zlim(-0.001+M[3*num+2,i], 0.001+M[3*num+2,i])
        
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    ani.save('Animation_Mars_satellites.mp4', fps=30, extra_args=['-vcodec', 'libx264'], bitrate=3600) 
    plt.show()

################################################################################################################################
#Animation centrée sur Jupiter

def animation_jupiter(methode,t_init,t_final,pas,X_init,save):

    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
    plt.title("SYSTEME JUPITER \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-20, +20)
    ax.set_ybound(-20, +20)
    ax.set_zbound(-20, +20)

    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
       
            if astre.nom=="Jupiter":
                ax.set_xlim(-0.02+M[3*num+0,i], 0.02+M[3*num+0,i])  #Référentiel en mouvement, changement du repère
                ax.set_ylim(-0.02+M[3*num+1,i], 0.02+M[3*num+1,i])
                ax.set_zlim(-0.02+M[3*num+2,i], 0.02+M[3*num+2,i])
        
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    ani.save('Animation_Jupiter_satellites.mp4', fps=30, extra_args=['-vcodec', 'libx264'], bitrate=3600) 
    plt.show()


########################################################################################################################
#Animation des principaux astéroides proche de la Terre

def animation_asteroides_centre(methode,t_init,t_final,pas,X_init,save):
    
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
    plt.title("SYSTEME SOLAIRE & OTHERS  \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-3, +3)
    ax.set_ybound(-3, +3)
    ax.set_zbound(-3, +3)
    ax.view_init(elev=80., azim=0)
    
    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
        
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    ani.save('Animation_Asteroides_centre.mp4', fps=30, extra_args=['-vcodec', 'libx264'], bitrate=7200) 
    plt.show()

########################################################################################################################
#Animation Systeme solaire + Halley

def animation_halley(methode,t_init,t_final,pas,X_init,save):
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
    plt.title("SYSTEME SOLAIRE & HALLEY  \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-20, +20)
    ax.set_ybound(-20, +20)
    ax.set_zbound(-20, +20)
    ax.view_init(elev=80., azim=0)
    
    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i], M[3*num+1,:i]) #Construction de la ligne sur x et y
            liste_line[num].set_3d_properties(M[3*num+2,:i])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
        
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    ani.save('Animation_Halley.mp4', fps=40, extra_args=['-vcodec', 'libx264'], bitrate=3600) 
    plt.show()

#############################################################################################################################


def Loi_Kepler_3(methode,t_init,t_final,pas,X_init,save):
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
#    plt.title("SYSTEME SOLAIRE & HALLEY  \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-20, +20)
    ax.set_ybound(-20, +20)
    ax.set_zbound(-20, +20)
    ax.view_init(elev=80., azim=0)
    print(len(X))

    
    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y. On va jusqu'à i mais on doit mettre i+1 en python
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
#           title1.set_text(str(i)+" days") 
        ax.set_title("SYSTEME SOLAIRE \n\n  Temps écoulé: "+ str(i*pas)+ " jours, Pas de résolution: "+ str(pas)+" jours,  Méthode "+ methode, color='white',y=1.0, pad=-14.0, fontsize=20)

        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=500, repeat=True, blit=True)
    
    if save==True:
        ani.save('Loi_Kepler_3_corrected.mp4', fps=250, extra_args=['-vcodec', 'libx264'], bitrate=3600) 
    
# Calcul des angles balayés, des demi grand axes, si on depasse 2pi on retient la période et le demi grand axe.    
    for num,astre in enumerate(liste_Astres_Restants):
        
        for i in range(len(X)):
            if i !=0:
                P_before=M[3*num:3*num+3,i-1] #position astre frame i-1
                P_after=M[3*num:3*num+3,i]  #position astre temps i
                Vectoriel=np.cross(P_before,P_after)
                norm_vectoriel=pow(np.vdot(Vectoriel.T,Vectoriel.T),1/2)
                angle_before=astre.angle
                astre.angle+= norm_vectoriel/ (pow(np.vdot(P_before.T,P_before.T),1/2)*pow(np.vdot(P_after.T,P_after.T),1/2))   #On détermine l'angle grâce au produit vectoriel
                
                if angle_before<2*np.pi and astre.angle>2*np.pi:
                    astre.periode=i*pas
                    astre.demi_grand_axe=(astre.dmax+astre.dmin)/2 
                astre.dmax=max(astre.dmax,pow(np.vdot(P_after.T,P_after.T),1/2))
                astre.dmin=min(astre.dmin,pow(np.vdot(P_after.T,P_after.T),1/2)) 

#On veut T² en fonction de a³, on passe en echelle logloget on applique une régression linéaire                 
    fig2 = plt.figure()
    ax2 = plt.axes()
    plt.title("3ème Loi de Kepler  \n\n  Pas de résolution: "+ str(pas)+" jours,  Méthode "+ methode, color='black',y=1.0, pad=-14.0, fontsize=20)    
    loi_des_aires_y=[astre.periode for astre in liste_Astres_Restants if astre.periode !=0]
    loi_des_aires_x=[astre.demi_grand_axe for astre in liste_Astres_Restants if astre.periode !=0]
    loi_des_aires_couleur=[astre.couleur for astre in liste_Astres_Restants if astre.periode !=0]
    for astre in liste_Astres_Restants:
        if astre.periode !=0:
            plt.annotate(" "+astre.nom,(astre.demi_grand_axe,astre.periode),fontsize=12) 
    ax2.scatter(loi_des_aires_x,loi_des_aires_y,color=loi_des_aires_couleur)
        
    plt.xscale('log')
    plt.yscale('log')
    ax2.tick_params(axis="x", labelsize=12)
    ax2.tick_params(axis="y", labelsize=12)
    plt.xlabel("Demi grand axe (UA), Log scale", size = 16)
    plt.ylabel("Periode (jours), Log scale", size = 16)
    plt.grid(True,which="both", linestyle='--')
    plt.show

# Calcul interpolation loi logarithmique
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log(loi_des_aires_x),np.log(loi_des_aires_y))
    print(slope, intercept, r_value, p_value, std_err)
    
    def logreg_y(x,slope, intercept):
        return np.exp(intercept)*x**slope
    
    logreg_x=np.linspace(min(loi_des_aires_x),max(loi_des_aires_x),100)
    ax2.plot(logreg_x, logreg_y(logreg_x,slope,intercept),linestyle='dashed',color='red')
    ax2.text( 0.45*(min(loi_des_aires_x)+max(loi_des_aires_x)), 0.2*(min(loi_des_aires_y)+max(loi_des_aires_y)),"pente = "+str(round(slope,4))+"\nr² = "+str(round(r_value**2,6)),color='red',fontsize=16)
    
##############################################################################################################################################

def Loi_Kepler_2(methode,t_init,t_final,pas,X_init,save,nom_astre,t1,t2,delta_t):
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

    #création des lignes, des points et du texte
    liste_line = [ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0] for astre in liste_Astres_Restants]
    liste_rond = [ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0] for astre in liste_Astres_Restants]

    ax.legend(loc='best',fontsize=20)
     
#    plt.title("SYSTEME SOLAIRE & HALLEY  \n\n Méthode "+methode+", Temps écoulé: "+ str(t_final-t_init)+ " jours, Pas de résolution: "+ str(pas)+" jours", color='white',y=1.0, pad=-14.0, fontsize=20)
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-30, +30)
    ax.set_ybound(-30, +30)
    ax.set_zbound(-30, +30)
    ax.view_init(elev=80., azim=0)
    
    def animate(i):
        for num,astre in enumerate(liste_Astres_Restants):
            liste_line[num].set_data(M[3*num,:i+1], M[3*num+1,:i+1]) #Construction de la ligne sur x et y. On va jusqu'à i mais on doit mettre i+1 en python
            liste_line[num].set_3d_properties(M[3*num+2,:i+1])  #Construction de la ligne sur z
            liste_rond[num].set_data(M[3*num,i], M[3*num+1,i])  #Construction du point sur x et y
            liste_rond[num].set_3d_properties(M[3*num+2,i])  #Construction du point sur z
#           title1.set_text(str(i)+" days")

            if astre.nom==nom_astre:
                if i !=0 and i>t1/pas and i<=(t1+delta_t)/pas:
                    P_before=M[3*num:3*num+3,i-1] #position astre frame i-1
                    P_after=M[3*num:3*num+3,i]  #position astre temps i
                    Vectoriel=np.cross(P_before,P_after)
                    norm_vectoriel=pow(np.vdot(Vectoriel.T,Vectoriel.T),1/2)
                    astre.angle= norm_vectoriel/ (pow(np.vdot(P_before.T,P_before.T),1/2)*pow(np.vdot(P_after.T,P_after.T),1/2))   #On détermine l'angle parcouru à la frame i grâce au produit vectoriel
                    astre.aire1+=astre.angle/2*((pow(np.vdot(P_before.T,P_before.T),1/2)+pow(np.vdot(P_after.T,P_after.T),1/2))/2)**2  #On determine approximativement l'aire balayée en utilisant la formule pi r² sur le rayon moyen
                    poly3d=[np.array([0,0,0]),P_before,P_after]
                    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='red', linewidths=1,alpha=0.5))
                    
                if i !=0 and i>t2/pas and i<=(t2+delta_t)/pas:
                    P_before=M[3*num:3*num+3,i-1] #position astre frame i-1
                    P_after=M[3*num:3*num+3,i]  #position astre temps i
                    Vectoriel=np.cross(P_before,P_after)
                    norm_vectoriel=pow(np.vdot(Vectoriel.T,Vectoriel.T),1/2)
                    astre.angle= norm_vectoriel/ (pow(np.vdot(P_before.T,P_before.T),1/2)*pow(np.vdot(P_after.T,P_after.T),1/2))   #On détermine l'angle parcouru à la frame i grâce au produit vectoriel
                    astre.aire2+=astre.angle/2*((pow(np.vdot(P_before.T,P_before.T),1/2)+pow(np.vdot(P_after.T,P_after.T),1/2))/2)**2  #On determine approximativement l'aire balayée en utilisant la formule pi r² sur le rayon moyen
                    poly3d=[np.array([0,0,0]),P_before,P_after]
                    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='blue', linewidths=1,alpha=0.5))
 
        ax.set_title("2ème Loi de Kepler Pluton \n  Temps écoulé: "+ str(i*pas)+ " jours, Pas de résolution: "+ str(pas)+" jours,  Méthode "+ methode+"\n\nIntervalle de temps: "+str(delta_t) +" jours, Aire rouge: "+str(round(astre.aire1,5)) +"(UA²), Aire bleue: "+str(round(astre.aire2,5))+"(UA²)", color='white',y=1.0, pad=-14.0, fontsize=20)
                
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=len(X), interval=1000, repeat=False, blit=True)
    
    if save==True:
        ani.save('Loi_Kepler_2_Pluton_Corrected.mp4', fps=50, extra_args=['-vcodec', 'libx264'], bitrate=3600) 
    
#########################################################################################################################################

def Angle_arc(theta_radian):
    theta_degre=theta_radian*180/np.pi
    degre=int(theta_degre)
    minute=int((theta_degre-degre)*60)
    seconde=int((theta_degre-degre-minute/60)*60*60)
    return str(degre)+"° "+ str(minute)+"' "+str(seconde)+"''"



def Alignement(methode,t_init,t_final,pas,X_init,save,Astre_0,Astre_1,Astre_2):
    save_trajectoire(methode,t_init,t_final,pas,X_init)
    # on configure les axes, le 3D, le fond ...
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    fig.set_facecolor('black')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    #On plot le Soleil
    ax.scatter(0,0,0, color=Soleil.couleur, label= Soleil.nom)

    for num,astre in enumerate(liste_Astres_Restants):
        if astre.nom==Astre_0:
            num_0=num
        if astre.nom==Astre_1:
            num_1=num
        if astre.nom==Astre_2:
            num_2=num 

    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], [] #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])


    #création des lignes, des points et du texte

    for astre in liste_Astres_Restants:
        if astre.nom==Astre_0:
            line_num_0= ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0]
 
    for astre in liste_Astres_Restants:
        if astre.nom==Astre_1:
            line_num_1= ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0]                        
                   
    for astre in liste_Astres_Restants:
        if astre.nom==Astre_2:
            line_num_2= ax.plot([], [], [], lw=1.0,linestyle='solid', color=astre.couleur)[0]                     

    liste_line=[line_num_0, line_num_1, line_num_2]

                      
    for astre in liste_Astres_Restants:
        if astre.nom==Astre_0:
            rond_num_0= ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0]
 
    for astre in liste_Astres_Restants:
        if astre.nom==Astre_1:
            rond_num_1= ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0]                        
                   
    for astre in liste_Astres_Restants:
        if astre.nom==Astre_2:
            rond_num_2= ax.plot([], [], [], ls='none', marker=astre.forme, color=astre.couleur, label=astre.nom)[0]                     

    liste_rond=[rond_num_0, rond_num_1, rond_num_2]
    
    
    line_1= ax.plot([], [], [], lw=1.0,linestyle='dashed', color="aqua")[0]   #création de nos lignes pour visualiser l'alignement
    line_2= ax.plot([], [], [], lw=1.0,linestyle='dashed', color="aqua")[0]
    liste_line.append(line_1)
    liste_line.append(line_2)  #On les rajoute dans la liste, ce sera plus simple quand on fera les tupple liste dans def animate(i)

    ax.legend(loc='best',fontsize=20)
     
    ax.autoscale(enable=False,axis='both')  #you will need this line to change the Z-axis
    ax.set_xbound(-10, +10)
    ax.set_ybound(-10, +10)
    ax.set_zbound(-10, +10)
    ax.view_init(elev=80., azim=0)
    
  

    nb_croisement_max=8 
    nb_croisement=0
    date_0=datetime.date(2020,1,1) 
    d_theta=np.pi/180*2
    theta_min=[d_theta for i in range (nb_croisement_max)]
    frame_cross=[0 for i in range (nb_croisement_max)]
    date_cross=[date_0 for i in range (nb_croisement_max)]
    
    
    V1b=M[3*num_1:3*num_1+3,0]-M[3*num_0:3*num_0+3,0]   #vecteur Astre_0 to astre_1  after
    V2b=M[3*num_2:3*num_2+3,0]-M[3*num_0:3*num_0+3,0]   #vecteur Astre_0 to astre_2  after         
    theta_before=np.cross(V1b,V2b)/(pow(np.vdot(V1b.T,V1b.T),1/2)*pow(np.vdot(V2b.T,V2b.T),1/2))  #calcul de l'angle de départ
    theta_before=pow(np.vdot(theta_before.T,theta_before.T),1/2)
            
    for i in range(len(X)):
    
        V1a=M[3*num_1:3*num_1+3,i]-M[3*num_0:3*num_0+3,i]   #vecteur Astre_0 to astre_1  after
        V2a=M[3*num_2:3*num_2+3,i]-M[3*num_0:3*num_0+3,i]   #vecteur Astre_0 to astre_2  after         
        theta_after=np.cross(V1a,V2a)/(pow(np.vdot(V1a.T,V1a.T),1/2)*pow(np.vdot(V2a.T,V2a.T),1/2))  #calcul de l'angle à la frame i
        theta_after=pow(np.vdot(theta_after.T,theta_after.T),1/2)
        
        if nb_croisement<nb_croisement_max and np.vdot(V1a.T,V2a.T)/(pow(np.vdot(V1a.T,V1a.T),1/2)*pow(np.vdot(V2a.T,V2a.T),1/2))> 0:   #si on n'a pas atteint le nombre de croisement max, et que les vecteur Astre0 to astre1 et Astre0 to Astre2 sont dans le même sens
        
            if theta_after<d_theta and theta_after<theta_before:
                theta_min[nb_croisement]=theta_after
                frame_cross[nb_croisement]=i*pas
                date_cross[nb_croisement]=date_0+datetime.timedelta(days=i*pas)
        
            if theta_after>d_theta and theta_before<d_theta:
                nb_croisement+=1                  #On incrémente la boucle
            
        theta_before=theta_after

    fact=12
    
    def animate(i):

        i=fact*i
        date_affichee=["                  " for i in range (8)]
        theta_affichee=["            " for i in range (8)]
        

        liste_line[0].set_data(M[3*num_0,:i+1], M[3*num_0+1,:i+1]) #Construction de la ligne sur x et y. On va jusqu'à i mais on doit mettre i+1 en python
        liste_line[0].set_3d_properties(M[3*num_0+2,:i+1])  #Construction de la ligne sur z
        liste_rond[0].set_data(M[3*num_0,i], M[3*num_0+1,i])  #Construction du point sur x et y
        liste_rond[0].set_3d_properties(M[3*num_0+2,i])  #Construction du point sur z

        liste_line[1].set_data(M[3*num_1,:i+1], M[3*num_1+1,:i+1]) #Construction de la ligne sur x et y. On va jusqu'à i mais on doit mettre i+1 en python
        liste_line[1].set_3d_properties(M[3*num_1+2,:i+1])  #Construction de la ligne sur z
        liste_rond[1].set_data(M[3*num_1,i], M[3*num_1+1,i])  #Construction du point sur x et y
        liste_rond[1].set_3d_properties(M[3*num_1+2,i])  #Construction du point sur z

        liste_line[2].set_data(M[3*num_2,:i+1], M[3*num_2+1,:i+1]) #Construction de la ligne sur x et y. On va jusqu'à i mais on doit mettre i+1 en python
        liste_line[2].set_3d_properties(M[3*num_2+2,:i+1])  #Construction de la ligne sur z
        liste_rond[2].set_data(M[3*num_2,i], M[3*num_2+1,i])  #Construction du point sur x et y
        liste_rond[2].set_3d_properties(M[3*num_2+2,i])  #Construction du point sur z


        line_1.set_data([M[3*num_0,i],M[3*num_1,i]], [M[3*num_0+1,i],M[3*num_1+1,i]])  #On affiche les ligne Astre_0 to Astre_1 et Astre_0 to Astre_2
        line_1.set_3d_properties([M[3*num_0+2,i],M[3*num_1+2,i]])
        line_2.set_data([M[3*num_0,i],M[3*num_2,i]], [M[3*num_0+1,i],M[3*num_2+1,i]])
        line_2.set_3d_properties([M[3*num_0+2,i],M[3*num_2+2,i]])           

        for k in range(nb_croisement_max):
            if i>frame_cross[k]/pas and frame_cross[k]!=0:
                date_affichee[k]=date_cross[k]
                theta_affichee[k]=Angle_arc(theta_min[k])
                

        date_i=date_0+datetime.timedelta(days=i*pas)
 
        ax.set_title("Grande Conjonction Planètes "+ Astre_0 + "-" + Astre_1 + "-" + Astre_2 + " \n  Date: "+ str(date_i)+ ", Pas de résolution: "+ str(pas)+" jours,  Méthode "+ methode + \
        "\n Date 1er croisement: "+ str(date_affichee[0]) + "         Angle mini: " + theta_affichee[0]  +"\n Date 2ème croisement: " +str(date_affichee[1])+ "      Angle mini: " + theta_affichee[1] +\
        "\n Date 3ème croisement: " +str(date_affichee[2]) + "      Angle mini: " + theta_affichee[2] +"\n Date 4ème croisement: " +str(date_affichee[3])+ "      Angle mini: " + theta_affichee[3],\
        color='white',y=1.0, pad=-70.0, fontsize=20)
                
        return  tuple (liste_line+liste_rond)
    
    fig.set_size_inches(32, 18)
    ani = animation.FuncAnimation(fig, animate, fargs=(), frames=int(len(X)/fact), interval=1000, repeat=False, blit=True)
    
    if save==True:
        ani.save('Grande conjonction planètes.mp4', fps=25, extra_args=['-vcodec', 'libx264'], bitrate=1800) 
    print(date_cross)
    print(theta_min)


##############################################################################################################################"

def Energy(methode,t_init,t_final,pas,X_init):

    save_trajectoire(methode,t_init,t_final,pas,X_init)

    position_vitesse_G =np.array([0., 0., 0., 0., 0., 0.])
    masse_totale = Soleil.masse #On initialise la masse totale, sachant que le soleil ne fait pas partie des astres restants
    Ec_calc=0
    Ep_calc=0
    Em_calc=0
    
    
    for astre in liste_Astres_Restants:
        masse_totale+=astre.masse
        
    Ec, Ep, Em = [], [], [] # On initialise les énergies
    
    for line in open(methode+'.txt', 'r'):
        values = np.array([float(s) for s in line.split()]) #On charge les coordonnées depuis le fichier text
       
        for num, astre in enumerate(liste_Astres_Restants):          
            position_vitesse_G[0:6] += astre.masse * values[6*num:6*num+6]  #Calcul des positions et des vitesses du centre de gravité G
        position_vitesse_G[0:6]/= masse_totale

        for num, astre in enumerate(liste_Astres_Restants):
            Ec_calc += astre.masse*(values[6*num+3]-position_vitesse_G[3])**2
            Ec_calc += astre.masse*(values[6*num+4]-position_vitesse_G[4])**2
            Ec_calc += astre.masse*(values[6*num+5]-position_vitesse_G[5])**2

            for num2, astre2 in enumerate(liste_Astres_Restants):
                if num2 > num:
                    d=values[6*num2:6*num2+3]-values[6*num:6*num+3] #Distance au soleil de astre_interact
                    d=pow(np.vdot(d.T,d.T),1/2) #calcul de la distance entre l'astre choisi et les autres astres                    
                    Ep_calc+= astre.masse * astre2.masse / d
            
            di=values[6*num:6*num+3]  #distance au soleil
            di=pow(np.vdot(di.T,di.T),1/2) #calcul de la distance entre l'astre choisi et le soleil 
            Ep_calc+= Soleil.masse * astre.masse / di
        
        Ec_calc+=Soleil.masse*(position_vitesse_G[3])**2  #On ajoute l'énergie cinétique du soleil dans le référentiel barycentrique (galiléen)
        Ec_calc+=Soleil.masse*(position_vitesse_G[4])**2
        Ec_calc+=Soleil.masse*(position_vitesse_G[5])**2
    
        Ec_calc/=2   #On divise pour avoir la bonne expression de l'énergie cinétique
        Ep_calc*=-1*G   #On multiplie pour avoir la bonne expression de l'énergie potentielle
        Em_calc= Ec_calc + Ep_calc
        Ec.append(Ec_calc)
        Ep.append(Ep_calc)
        Em.append(Em_calc)
        
        position_vitesse_G =np.array([0., 0., 0., 0., 0., 0.])
        Ec_calc=0
        Ep_calc=0
        Em_calc=0
        
    energy_relative_error=(np.max(Em)-np.min(Em))/np.min(Em)
    print(np.max(Em)-np.min(Em))
    print(energy_relative_error)
    
    for num,astre in enumerate(liste_Astres_Restants):
        X, Y, Z = [], [], []  #On initialise les coordonnées 
        for line in open(methode+'.txt', 'r'):
            values = [float(s) for s in line.split()] #On charge les coordonnées depuis le fichier text
            X.append(values[6*num])     # premières coordonnées de la num ième planète
            Y.append(values[6*num+1])   # deuxièmes coordonnées de la num ième planète
            Z.append(values[6*num+2])   # troisièmes coordonnées de la num ième planète
        P=np.vstack([X,Y,Z])        # On cumule verticalement les coordonnées de la num ième planète
        
        
        if num==0:                  # On initialise M = P pour la première planète (num = 0)
            M=P
        else:                       # Pour num>0 on range les coordonnées en vertical en accumulant avec les précédentes
            M=np.vstack([M,P])

#On veut energie potentielle, energie cinétique et energie mécanique totale en fonction du temps,              
    fig = plt.figure()
    ax = plt.axes()
    plt.title("Évolutionde l'énergie en fonction du temps  \n\n  Pas de résolution: "+ str(pas)+" jours,  Méthode "+ methode, color='black',y=1.0, pad=-14.0, fontsize=20)    


###################################################################################################################################




#Alignement("RK4",0,25000,1,X_init,save=True,Astre_0="Terre",Astre_1="Saturne",Astre_2="Jupiter")


#Loi_Kepler_3("RK5",0,600,1,X_init,save=False)    
#Loi_Kepler_2("RK5",0,100000,100,X_init,nom_astre="Pluton",save=True,t1=30000,t2=75000,delta_t=10000)
# Energy("RK4",0,10000,1,X_init) 

#animation_halley("RK5",0,30000,20,X_init,save=True)
#animation_asteroides_centre("RK5",0,10000,10,X_init,save=True)
#animation_jupiter("RK5",0,30,0.05,X_init,save=True)
#animation_mars("RK5",0,10,0.01,X_init,save=True) 
#animation_earthmoon("RK4",0,100,0.1,X_init,save=True)
#plot_lines("RK4",0,365,1,X_init) 
#plot_lines("RK45",0,365,1,X_init,tolerance=0.00001)







os.system("pause")
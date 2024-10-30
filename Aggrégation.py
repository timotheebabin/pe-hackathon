# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import xcover as co
import matplotlib.pyplot as plt

# %%
BOARD_8_8 = np.zeros((8, 8), dtype='uint64')
BOARD_8_8[3:5, 3:5] = 1
carte0 = BOARD_8_8
print(carte0)

# %%
raw_shapes = {
    "F": np.array([[1, 1, 0], [0, 1, 1], [0, 1, 0]]),
    "I": np.array([[1, 1, 1, 1, 1]]),
    "L": np.array([[1, 0, 0, 0], [1, 1, 1, 1]]),
    "N": np.array([[1, 1, 0, 0], [0, 1, 1, 1]]),
    "P": np.array([[1, 1, 1], [1, 1, 0]]),
    "T": np.array([[1, 1, 1], [0, 1, 0], [0, 1, 0]]),
    "U": np.array([[1, 1, 1], [1, 0, 1]]),
    "V": np.array([[1, 1, 1], [1, 0, 0], [1, 0, 0]]),
    "W": np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]]),
    "X": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
    "Y": np.array([[0, 1, 0, 0], [1, 1, 1, 1]]),
    "Z": np.array([[1, 1, 0], [0, 1, 0], [0, 1, 1]]),
}

num_lettres = {"F":[1,0,0,0,0,0,0,0,0,0,0,0],
               "I":[0,1,0,0,0,0,0,0,0,0,0,0],
               "L":[0,0,1,0,0,0,0,0,0,0,0,0], 
               "N":[0,0,0,1,0,0,0,0,0,0,0,0], 
               "P":[0,0,0,0,1,0,0,0,0,0,0,0],
               "T":[0,0,0,0,0,1,0,0,0,0,0,0],
               "U":[0,0,0,0,0,0,1,0,0,0,0,0],
               "V":[0,0,0,0,0,0,0,1,0,0,0,0],
               "W":[0,0,0,0,0,0,0,0,1,0,0,0],
               "X":[0,0,0,0,0,0,0,0,0,1,0,0],
               "Y":[0,0,0,0,0,0,0,0,0,0,1,0],
               "Z":[0,0,0,0,0,0,0,0,0,0,0,1]}


# %%
dico = {}

def rot_sym(lettre):
    
    piece = raw_shapes[lettre]
    L = [piece]
    
    def pi_demi(M):                                #fonction rotation de pi/2 dans le sens trigo
        M_n,M_m = np.shape(M)
        R = np.zeros(shape=(M_m,M_n))
        for i in range(M_m):
            for j in range(M_n):
                R[i][j] = M[j][M_m-i-1]
        return(R)
        
    def axial(M):                                  #fonction symétrie axiale
        return(np.transpose(np.transpose(M)[::-1]))

    def applique_rot(mat):                         #ajoute les rotations successives différentes à la liste
        K = pi_demi(mat)
        while not np.array_equal(K, mat) :
            L.append(K)
            K = pi_demi(K)
        return(L)

    piece_sym = axial(piece)
    
    applique_rot(piece)                            #ajoute les rotations de piece
    if not np.array_equal(piece_sym, piece) :
        L.append(piece_sym)                        #ajoute le symétrique de piece
        applique_rot(piece_sym)                    #ajoute les rotations successives du symétrique

    dico[lettre] = L                               #ajoute la liste à la clé lettre
    return L



# %%
def sous_matrices(carte,shape): 
    n,m=carte.shape
    l,k=shape
    ens_sous_matrices = np.zeros(shape=(n-l+1,m-k+1,l,k))
    for i in range(n-l+1):
        for j in range(m-k+1):
            ens_sous_matrices[i,j,:,:]=carte[i:i+l,j:j+k]
    return(ens_sous_matrices)  


# %%
def est_position (piece, sous_matrice): 
    #pour une rotation de pièce donnée et une sous_matrice donnée, renvoie si on peut y mettre la pièce et à quel endroit
    somme= (2*piece)+sous_matrice #on multiplie la pièce par 2 pour la différencier des obstacles 
    return somme



# %%
def vecteur(lettre, s_m, case, carte): #s_m pour sous-matrice
    n, m = carte.shape
    carte2=carte.copy()
    indices = carte2.reshape((1,n*m)).tolist()[0]
    i, j =  case
    a, b = s_m.shape 
    M = carte[i:i+a:, j:j+b]  #Sous matrice correspondnat dans le tableau
    P = (s_m-M)/2 #Position de la pièce (1) sans obstacles dans la sous matrice correspondante
    A = np.zeros((n,m), dtype = 'uint64')
    for k in range (a) :
        for l in range (b) :
            A[i+k, j + l] = int(P[k, l])
    Lpos = (A.reshape(1, n*m).tolist())[0]
    a_retirer = []
    for p in range (n*m) :
        if indices[p] == 1 :
            a_retirer.append(p)    
    L_finale = []
    for q in range (n*m) :
        if q not in a_retirer :
            L_finale.append(Lpos[q])
    return num_lettres[lettre]+L_finale #Lpos a été nettoyée : c'est une liste de taille 60     


# %%
len(vecteur("F", 2*raw_shapes["F"], (0,1), carte0))


# %%
def test_toutes_positions (lettre, piece, carte, resultat): 
    #pour une rotation de pièce donnée, renvoie toutes les positions où on peut la placer
    ens_sous_matrices=sous_matrices(carte, piece.shape).copy()
    for i in range(ens_sous_matrices.shape[0]):
        for j in range(ens_sous_matrices.shape[1]):
            est_pos=est_position (piece, ens_sous_matrices[i,j])
            if np.any(est_pos>2) :
                pass
            else :
                resultat = np.concatenate((resultat,np.array([vecteur(lettre, est_pos, (i,j), carte)])),axis=0)
    return resultat
                


# %%
def tableau_final(carte):
    resultat=np.zeros(shape=(1,72),dtype='uint8')
    for lettre in raw_shapes.keys() :
        rotsym=rot_sym(lettre)
        for forme in rotsym :
            resultat = test_toutes_positions(lettre,forme,carte,resultat)
    return resultat


# %%
tableau_final(carte0)

# %%
solutions = list(co.covers_bool(tableau_final(carte0)))
print(solutions)


# %%
def indice(i, carte):
    n,m = carte.shape
    return i//m, i%m

def num_carte(carte):
    n,m = carte.shape
    N = n*m
    A = np.arange(1,(N+1))
    for k in range(N) :
        i,j = indice(k,carte)
        if carte[i,j] == 1 :
            A[k] = 0
            modif = [0]*(k+1) + [-1]*(N-k-1) #On retire 1 à tous les suivants car l'emplacement i,j est un obstacle
            A = A + np.array(modif)
    A.resize(n,m)
    return A

print(num_carte(carte0))

# %%
tab_fin = tableau_final(carte0)

def afficher_solu(solu):
    resultat = carte.copy()
    dicoordonnee={}
    dicoindice={}

    #cette fonction sert à remplir les dictionnaires qui donnent les indices en fonctions des coord. et réciproquement
    def dicoord(tab):
        t_n,t_m=np.shape(tab)
        for i in range(t_n):
            for j in range(t_m):
                c = tab[i][j]
                if c != 0 :
                    dicoordonnee[(i,j)]=c
                    dicoindice[c]=(i,j)

    dicoord(num_carte(carte0))
    r_n,r_m=np.shape(resultat)
    
    for k in range(len(solu)):
        vect=tab_fin[solu[k]]
        for j in range(0,12):
            if vect[j]==1:
                let_ind=j
                break
        for i in range(12,72):
            if vect[i]==1:
                resultat[dicoindice[i-11]]=let_ind+2
    return(resultat)


# %%
image_solu_chiffres=afficher_solu(solutions[0])
print(image_solu_chiffres)

# %%
dicouleur={1:[255,255,255],
           2:[255,0,0],
           3:[148,0,211],
           4:[0,0,255],
           5:[255,255,0],
           6:[255,0,255],
           7:[0,255,255],
           8:[80,80,80],
           9:[100,0,255],
           10:[255,125,0],
           11:[0,255,180],
           12:[125,255,0],
           13:[255,0,100],
           14:[0,125,255]}

def afficouleur(tab):
    t_n,t_m=np.shape(tab)
    tabl=np.zeros(shape=(t_n,t_m,3),dtype='uint64')
    for i in range(t_n):
        for j in range(t_m):
            tabl[i][j]=dicouleur[tab[i][j]]
    plt.imshow(tabl)


# %%
afficouleur(image_solu_chiffres)

# %%
afficouleur(afficher_solu(solutions[1])) #les solutions sont comptées plusieurs fois

# %%
afficouleur(afficher_solu(solutions[345]))

# %%

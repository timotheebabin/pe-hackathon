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
    L1 = [0]*(i-1)*m #0 au dessus de la sm
    L2 = [0]*(n-(i+a))*m #0 en dessous
    for k in range(b):
        L1 = L1 + [0]*(j-1) + P[k:k+1:, :].tolist() + [0]*(m-(j+b))
    Lpos = L1 + L2 #Liste position de taille n*m (avec obstacles)
    for k in range (n*m) :
        a_retirer = []
        if indices[k] == 1 :
            a_retirer.append(k)    
        for j in a_retirer :
            Lpos = Lpos[:j] + Lpos[j+1:]
    return num_lettres[lettre]+Lpos #Lpos a été nettoyée : c'est une liste de taille 60     


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
                resultat.append(vecteur(lettre, est_pos, (i,j), carte))


# %%
def tableau_final(carte):
    resultat=[]
    for lettre in raw_shapes.keys() :
        rotsym=rot_sym(lettre)
        for forme in rotsym :
            test_toutes_positions(lettre,forme,carte,resultat)
    print(resultat)
    return np.concatenate(resultat,axis=0)


# %%
L = [1,0,0,0,0,1,0,1,0,0,0,1,0,0]
carte = np.array([L for i in range(6)])
carte

# %%
tableau_final(carte)

# %%

# %%

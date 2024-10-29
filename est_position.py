import numpy as np


def sous_matrices(carte,shape):
    n,m=carte.shape
    l,k=shape
    ens_sous_matrices = np.zeros(shape=(n-l+1,m-k+1,l,k))
    for i in range(n-l+1):
        for j in range(m-k+1):
            ens_sous_matrices[i,j,:,:]=carte[i:i+l,j:j+k]
    return(ens_sous_matrices)  


# +
def est_position (lettre, piece, case, sous_matrice):
    somme= (2*piece)+sous_matrice
    if np.any(somme > 2):
        return case
    else : 
        return lettre, somme, case, carte

def vecteur(lettre, s_m, case, carte): #s_m pour sous-matrice
    n, m = carte.shape
    carte2 = carte.copy()
    indices = carte2.resize((1,n*m)).tolist()
    i, j =  case
    a, b = s_m.shape 
    M = carte[i:i+a:, :j:j+b]  #Sous matrice correspondnat dans le tableau
    P = (s_m-M)/2 #Position de la pièce (1) sans obstacles dans la sous matrice correspondante
    L1 = [0]*(i-1)*m #0 au dessus de la sm
    L2 = [0]*(n-(i+a))*m #0 en dessous
    for k in range(b):
        L1 = L1 + [0]*(j-1) + s_m[:, k:k+1:].tolist() + [0]*(m-(j+b))
    Lpos = L1 + L2 #Liste position de taille n*m (avec obstacles)
    for k in range (n*m) :
        if indices[k] == 1 :
                Lpos = Lpos[:k] + Lpos[k+1:]
    return num_lettres[lettre]+Lpos #Lpos a été nettoyée : c'est une liste de taille 60     

def test_toutes_positions (lettre, piece, carte, resultat):
    ens_sous_matrices=sous_matrices(carte, piece.shape).copy()
    print(ens_sous_matrices)
    for i in range(ens_sous_matrices.shape[0]):
        for j in range(ens_sous_matrices.shape[1])):
            resultat.append(vecteur(est_position (lettre,piece, (i,j), ens_sous_matrices[i,j])))


# essai test_toutes_positions("F", np.array([[1,0],[1,0]]), np.array([[1,0,1],[0,0,1],[1,0,1],[0,1,1]]),[])
# -
def tableau final :





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
"""prend en argumant la matrice générale et la forme (shape) des sous-matrices recherchées
TYPES ATTENDUS :
matrice : array
shape : tuple (l,k)

RETOURNE :
un array que j'appelle 'tableau final'
le tableau final va contenir chaque sous-matrice à la position correspondant à sa case en haut à gauche
par exemple [3,2,4,6] renvoie l'élément de position (4,6) de la sous-matrice de position (3,2)
"""
def sous_matrices(matrice,shape):
    n,m=matrice.shape
    l,k=shape
    tableau_final = np.zeros(shape=(n-l+1,m-k+1,l,k))
    for i in range(n-l+1):
        for j in range(m-k+1):
            tableau_final[i,j,:,:]=matrice[i:i+l,j:j+k]
    return(tableau_final)


# %%
#pour tester le code :
sous_matrices(np.array([[1,0,1],[0,0,1],[1,0,1],[0,1,1]]),(2,2))

# %%

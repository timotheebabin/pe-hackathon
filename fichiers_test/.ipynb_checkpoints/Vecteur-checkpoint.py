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
import pandas as pd
import xcover as co
import matplotlib.pyplot as plt


# %%
def vecteur(lettre, s_m, case, carte): #s_m pour sous-matrice
    n, m = carte.shape
    indices = list(carte.resize((1,n*m)))
    i, j =  case
    a, b = s_m.shape 
    M = carte[i:i+a:, :j:j+b]  #Sous matrice correspondnat dans le tableau
    P = (s_m-M)/2 #Position de la pièce (1) sans obstacles dans la sous matrice correspondante
    L1 = [0]*(i-1)*j #0 au dessus de la sm
    L2 = [0]*(n-(i+a)) #0 en dessous
    for k in range(b):
        L1 = L1 + [0]*(j-1) + list(s_m[:, k:k+1:]) + [0]*(m-(j+b))
    Lpos = L1 + L2 #Liste position de taille n*m (avec obstacles)
    for k in range (n*m) :
        if indices[k] == 1 :
                Lpos = Lpos[:k] + Lpos[k+1:]
    return num_lettres[lettre]+Lpos #Lpos a été nettoyée : c'est une liste de taille 60  

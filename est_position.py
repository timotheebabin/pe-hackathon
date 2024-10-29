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
def est_position (lettre, piece, case,sous_matrice):
    somme= (2*piece)+sous_matrice
    if np.any(somme > 2):
        return case
    else : 
        return somme, lettre, case

def test_toutes_positions (lettre,piece, carte, resultat):
    ens_sous_matrices=sous_matrices(carte, piece.shape).copy()
    print(ens_sous_matrices)
    for i in range(len(ens_sous_matrices[0])):
        for j in range(len(ens_sous_matrices[1])):
            resultat.append(est_position (lettre,piece, (i,j), ens_sous_matrices[i,j]))
    return resultat

# essai test_toutes_positions("f", np.array([[1,0],[1,0]]), np.array([[1,0,1],[0,0,1],[1,0,1],[0,1,1]]),[])
# -



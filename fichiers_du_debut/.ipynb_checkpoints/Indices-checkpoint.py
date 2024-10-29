# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
def indice(i, carte):
    n,m = carte.shape
    return i//m, i%m

def num_carte(carte):
    n,m = carte.shape
    N = n*m
    A = np.arange(1,N+1,1,dtype = 'uint64')
    for k in range(N) :
        i,j = indice(k,carte)
        if carte[i,j] == 1 :
            A[k] = 0
            modif = [0]*k + [-1]*(N-k) #On retire 1 à tous les suivants car l'emplacement i,j est un obstacle
            A = A + np.array(modif)
    return A.resize(n,m)

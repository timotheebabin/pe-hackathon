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
import xcover
import numpy as np
from xcover import covers
from xcover import covers_bool as cobo

# %%
# xcover?

# %%
solution = covers([[0,1],[3,4],[2],[2,3]])
print(list(solution))

# %%
solution = cobo(np.array([[1,0,1,0],[0,1,0,1],[1,1,1,1]]))
print(list(solution))

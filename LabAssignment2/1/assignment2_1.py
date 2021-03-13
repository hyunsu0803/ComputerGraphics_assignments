import numpy as np

M = np.arange(2, 27)
print(M)
print()

M = M.reshape(5,5)
print(M)
print()

M[1:-1, 1:-1] = 0
print(M)
print()

M = M@M
print(M)
print()

v = M[0, :]
mag = 0
for i in range(5):
    mag += v[i]**2
mag = np.sqrt(mag)
print(mag)

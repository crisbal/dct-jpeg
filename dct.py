from math import sqrt, cos, pi
from scipy.fftpack import dct as spfdct
from scipy.fftpack import idct as ispfdct


def fdct(values):
    values = values.copy()
    return spfdct(values, type=2, norm='ortho')


def ifdct(values):
    values = values.copy()
    return ispfdct(values, type=2, norm='ortho')


def dct(values):
  values = values.copy()
  c = []
  N = len(values)
  for k in range(N):
    if k == 0:
      alfa_k = sqrt(1/N)
    else:
      alfa_k = sqrt(2/N)
    partial_sum = 0
    for i in range(N):
      f_i = values[i]
      partial_sum += f_i * cos(pi * k * (2*i+1)/(2*N))
    c.append(alfa_k * partial_sum)
  return c


def dct2t(matrix):
  matrix = matrix.copy()
  for i, row in enumerate(matrix):
      matrix[i] = dct(row)

  # transpose matrix
  matrix = [*zip(*matrix)]

  for i, column in enumerate(matrix):
      matrix[i] = dct(list(column))

  # transpose matrix
  matrix = [*zip(*matrix)]
  return matrix


def fdct2t(matrix):
    matrix = matrix.copy()
    return spfdct(spfdct(matrix, type=2, norm="ortho").T, type=2, norm="ortho").T


def ifdct2t(matrix):
    matrix = matrix.copy()
    return ispfdct(ispfdct(matrix, type=2, norm="ortho").T, type=2, norm="ortho").T


def dct2(matrix):
  matrix = matrix.copy()
  N = len(matrix)
  M = len(matrix[0])
  c = [[0 for i in range(M)] for i in range(N)]
  for k in range(N):
    for l in range(M):
      if k == l == 0:
        alpha = sqrt(1/(N*M))
      elif k == 0 or l == 0:
        alpha = sqrt(2/(N*M))
      else:
        alpha = 2/sqrt(N*M)
      partial_sum = 0
      for i in range(N):
        for j in range(M):
          f_ij = matrix[i][j]
          partial_sum += f_ij * \
            cos(pi * k * (2*i+1)/(2*N)) * \
            cos(pi * l * (2*j+1)/(2*M))
      c[k][l] = alpha * partial_sum
  return c


def mdct(vector):
    vector = vector.copy()
    C = [cos(pi / 16 * i) for i in range(8)]
    S = [1 / (4 * val) for val in C]
    S[0] = 1 / (2 * sqrt(2))
    A = [
        None,
        C[4],
        C[2] - C[6],
        C[4],
        C[6] + C[2],
        C[6],
    ]
    v0 = vector[0] + vector[7]
    v1 = vector[1] + vector[6]
    v2 = vector[2] + vector[5]
    v3 = vector[3] + vector[4]
    v4 = vector[3] - vector[4]
    v5 = vector[2] - vector[5]
    v6 = vector[1] - vector[6]
    v7 = vector[0] - vector[7]

    v8 = v0 + v3
    v9 = v1 + v2
    v10 = v1 - v2
    v11 = v0 - v3
    v12 = -v4 - v5
    v13 = (v5 + v6) * A[3]
    v14 = v6 + v7

    v15 = v8 + v9
    v16 = v8 - v9
    v17 = (v10 + v11) * A[1]
    v18 = (v12 + v14) * A[5]

    v19 = -v12 * A[2] - v18
    v20 = v14 * A[4] - v18

    v21 = v17 + v11
    v22 = v11 - v17
    v23 = v13 + v7
    v24 = v7 - v13

    v25 = v19 + v24
    v26 = v23 + v20
    v27 = v23 - v20
    v28 = v24 - v19

    return [
        S[0] * v15,
        S[1] * v26,
        S[2] * v21,
        S[3] * v28,
        S[4] * v16,
        S[5] * v25,
        S[6] * v22,
        S[7] * v27,
    ]


def mdct2t(matrix):
    matrix = matrix.copy()
    for i, row in enumerate(matrix):
        matrix[i] = mdct(row)

    matrix = [*zip(*matrix)]

    for i, column in enumerate(matrix):
        matrix[i] = mdct(list(column))

    matrix = [*zip(*matrix)]
    return matrix

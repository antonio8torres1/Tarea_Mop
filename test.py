from numpy import array
from simplex_m import Simplex

matrix = [
        [-5, -6, 0, 0, 0, 0,0],
        [2, 3, 1, 0, -1, 0,12],
        [2, 1, 0, -1, 0, 1,14]
]

matrix2 = [
        [-4,-1,0,0,0,0,0],
        [3,1,1,0,0,0,3],
        [4,3,0,1,-1,0,6],
        [1,2,0,0,0,1,3]
]

header = ["X1","X2","A1","H2","H1","A2"]
ld = ["Z","A1","A2"]

table = Simplex(3,7,opts = 0)
table.initialize(matrix,header,ld)
print(table)

n = table.solve()
print(table)
print(f"# de Iteraciones: {n}")

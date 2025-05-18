import streamlit as st
from numpy import array
from simplex_m import Simplex

def main():
<<<<<<< HEAD
    
    matrix = [
        [-5, -6, 0, 0, 0, 0,0],
        [2, 3, -1, 0, 1, 0,12],
        [2, 1, 0, -1, 0, 1,14]
    ]

    matrix2 = [
        [-4,-1,0,0,0,0,0],
        [3,1,1,0,0,0,3],
        [4,3,0,1,-1,0,6],
        [1,2,0,0,0,1,3]
    ]

    header = ["X1","X2","H1","H2","A1","A2"]
    ld = ["Z","A1","A2","H3"]

    table = Simplex(3,7,opts = 0)
    table.initialize(matrix,header,ld)
    print(table)

    n = table.solve()

    print(table)
    print(f"# de Iteraciones: {n}")
=======
    z = array([-1.6, -1.4, 0, 0, 0], dtype=float)
    matrix = array([
        [10, 20, 1, 0, 0],
        [15, 10, 0, 1, 0],
        [18, 6, 0, 0, 1],
    ], dtype=float)

    ld = array([0, 8000, 6000, 6300], dtype=float)
    header = ["X1", "X2", "H1", "H2", "H3"]
    vb = ["Z ", "H1", "H2", "H3"]

    table = TableSimplex(z, matrix, ld, header, vb, 1)

    st.subheader("Tabla inicial")
    st.table(table.as_matrix())

    n = table.solve()

    st.subheader("Tabla final")
    st.table(table.as_matrix())

    st.subheader("Resultado óptimo")
    st.write("Iteraciones:", n)
>>>>>>> 67e52c71abc8c6119dcf77dc2c92de0d33b1ee4f

if __name__ == "__main__":
    main()
import streamlit as st
from tablesimplex import TableSimplex
from numpy import array


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

import streamlit as st
from streamlit import (
    session_state,
    container,
    expander,
    selectbox,
    button,
    write,
    title,
    columns,
)
from simplex_m import Simplex

st.set_page_config(layout="wide")

if "config" not in session_state:
    session_state.config = {
        "num_variables": 6,
        "num_equations": 4,
        "target": "",
        "options": ["Maximizar", "Minimizar"],
    }
if "config_table" not in session_state:
    session_state.config_table = {"state": False, "opts_equations": ["<", ">", "="]}

title("Calculadora Metodo Simplex")

with container():
    with expander("Configuracion del problema", expanded=True):
        session_state.config["target"] = selectbox(
            "Escoja una opcion:", session_state.config["options"]
        )
        variables = int(selectbox("Numero de Varibles: ", list(range(1, 20))))
        equations = int(selectbox("Numero de Restricciones: ", list(range(1, 20))))

        session_state.config["num_variables"] = variables
        session_state.config["num_equations"] = equations

    write("### Funcion Objetivo")
    cols = columns(session_state.config["num_variables"])
    for i, col in enumerate(cols):
        with col:
            st.text_input(f"X{i + 1}", key=f"z{i}")

    write("### Restricciones")
    for j in range(session_state.config["num_equations"]):
        cols = columns(session_state.config["num_variables"] + 2)
        for i, col in enumerate(cols):
            with col:
                if i == session_state.config["num_variables"]:
                    st.selectbox(
                        "", session_state.config_table["opts_equations"], key=f"op{j}"
                    )
                elif i == session_state.config["num_variables"] + 1:
                    st.text_input("LD", key=f"ld{j}")
                else:
                    st.text_input(f"X{i + 1}", key=f"r{i}_{j}")

    matrix_coef = []
    opt_list = []
    z_colum = []

    for j in range(session_state.config["num_equations"]):
        row = []

        for i in range(session_state.config["num_variables"] + 1):
            if i == session_state.config["num_variables"]:
                ld_key = f"ld{j}"
                val = session_state.get(ld_key, "")
                row.append(val)
            else:
                key = f"r{i}_{j}"
                val = session_state.get(key, "")
                row.append(val)

        matrix_coef.append(row)

        key_opt = f"op{j}"
        val = session_state.get(key_opt, "")
        opt_list.append(val)

    if button("Resolver"):
        session_state.config_table["state"] = True


with container():

    header = ["X1","X2","H1","H2","A1","A2"]
    ld = ["Z","A1","A2"]
    write("### Tabla inicial")
    
    write("### Solucion")

    write("### Iteracion final")

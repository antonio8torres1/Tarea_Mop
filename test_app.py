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
    session_state.config_table = {
        "state": False,
        "opts_equations": ["<", ">", "="],
        "table": [],
    }

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
    for i in range(session_state.config["num_equations"]):
        cols = columns(session_state.config["num_variables"] + 2)
        for j, col in enumerate(cols):
            with col:
                if j == session_state.config["num_variables"]:
                    st.selectbox(
                        "", session_state.config_table["opts_equations"], key=f"op{i}"
                    )
                elif j == session_state.config["num_variables"] + 1:
                    st.text_input("LD", key=f"ld{i}")
                else:
                    st.text_input(f"X{j + 1}", key=f"r{i}_{j}")

    if button("Resolver"):
        session_state.config_table["state"] = True


with container():
    if session_state.config_table["state"]:
        session_state.config_table["table"].clear()
        opt_list = []

        # Extraer datos
        for i in range(session_state.config["num_equations"] + 1):
            row = []

            for j in range(session_state.config["num_variables"] + 1):
                if i == 0:
                    if j == session_state.config["num_variables"]:
                        row.append(0)
                    else:
                        key = f"z{j}"
                        value = session_state.get(key, "")
                        row.append(value)
                else:
                    if j == session_state.config["num_variables"]:
                        key = f"ld{i - 1}"
                        value = session_state.get(key, "")
                        row.append(value)
                    else:
                        key = f"r{i - 1}_{j}"
                        value = session_state.get(key,"")
                        row.append(value)

            session_state.config_table["table"].append(row)

            key_opt = f"op{i}"
            val = session_state.get(key_opt, "")
            opt_list.append(val)

        write(opt_list)

    header = ["X1", "X2", "H1", "H2", "A1", "A2"]
    ld = ["Z", "A1", "A2"]

    row = session_state.config["num_equations"] + 1
    colum = session_state.config["num_variables"] + 1

    table = Simplex(row,colum,opts = 0)

    table.initialize(session_state.config_table["table"],header,ld)

    write("### Tabla inicial")
    data , tabl = table.table_pandas()
    st.dataframe(data)

    write("### Solucion")
    n = table.solve()
    write(f"Numero de iteraciones: {n}")
    

    write("### Iteracion final")
    data , tabl = table.table_pandas()
    st.dataframe(data)

    session_state.config_table["state"] = False

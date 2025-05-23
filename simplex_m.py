import enum
import numpy as np
from numpy import array, zeros, where, argmin, argmax, min, max, round, count_nonzero
import pandas as pd


class Simplex:
    def __init__(self, height: int, width: int, opts: int = 1) -> None:
        self.matrix = zeros((height, width, 2), dtype=float)
        self.header = zeros((width), dtype=str)
        self.basic_variables = zeros(height, dtype=str)
        self.opts = opts

    def __str__(self) -> str:
        table = ""
        table += "----------------------------------------\n"
        for i in self.matrix:
            table += "\n"
            for j in i:
                if j[0] == 0:
                    if j[1] >= 0:
                        table += "|      " + str(round(j[1], 1))
                    else:
                        table += "|     " + str(round(j[1], 1))

                elif j[0] > 0:
                    if j[1] > 0:
                        table += (
                            "| " + str(round(j[0], 1)) + "M" + "+" + str(round(j[1], 1))
                        )
                    if j[1] < 0:
                        table += "| " + str(round(j[0], 1)) + "M" + str(round(j[1], 1))
                    if j[1] == 0:
                        table += "|     " + str(round(j[0], 1)) + "M"

                elif j[0] < 0:
                    if j[1] > 0:
                        table += (
                            "|" + str(round(j[0], 1)) + "M" + "+" + str(round(j[1], 1))
                        )
                    if j[1] < 0:
                        table += "|" + str(round(j[0], 1)) + "M" + str(round(j[1], 1))
                    if j[1] == 0:
                        table += "|    " + str(round(j[0], 1)) + "M"

            table += "|"

        table += "\n----------------------------------------"

        return table

    def initialize(self, matrix, header, vb):
        """
        Iiniciliza la tabla para poder aplicar el metodo simplex
        """

        self.header = array(header)
        self.basic_variables = array(vb)

        # Llenar la matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[0]) - 1):
                if i == 0:
                    self.matrix[i, j, 1] = float(matrix[i][j]) * (-1)
                else:
                    self.matrix[i, j, 1] = float(matrix[i][j])
            self.matrix[i, -1, 1] = float(matrix[i][-1])

        # Obtener los indices de las filas con A y H
        a_colum = [i for i, p in enumerate(self.header) if "A" in p]
        h_colum = [i for i, p in enumerate(self.header) if "H" in p]

        # Obtener los indices de las columnas con A y H
        a_row = [i for i, p in enumerate(self.basic_variables) if "A" in p]
        h_row = [i for i, p in enumerate(self.basic_variables) if "H" in p]

        # Primera coincidiencia obligatoria donde A/A
        for i in a_row:
            for j in a_colum:
                if self.header[j] == self.basic_variables[i]:
                    self.matrix[i, j, 1] = 1

        # Asignacion don de H/A
        count_h = 0
        count_a = 0
        for i in h_colum:
            if count_h < len(h_row):
                self.matrix[h_row[count_h], i, 1] = 1
                count_h += 1
            else:
                self.matrix[a_row[count_a], i, 1] = -1
                count_a += 1

        # Asignacion de M primera fila(Z)
        if self.opts == 0:
            for i in a_colum:
                self.matrix[0, i, 0] = -1

    def solve(self):
        height = len(self.matrix)
        width = len(self.matrix[0])
        row_z = self.matrix[0, :, 1]
        iterations = 0

        # Iteracion previa
        # for i in range(1, height):
        #   for j in range(width):
        #       self.matrix[0, j, 0] += self.matrix[i, j, 1]
        a_row = [i for i, p in enumerate(self.basic_variables) if "A" in p]
        for i in a_row:
            self.matrix[0, :, 0] += self.matrix[i, :, 1]

        a = self.matrix[0, :-1, 0]
        b = self.matrix[0, :-1, 1]

        # return iterations
        while np.any(a > 0) or (np.all(a == 0) and np.any(b > 0)):
            # Variable de entrada
            values_m = self.matrix[0, :-1, 0]
            values_co = self.matrix[0, :-1, 1]

            index_min_colum = where(values_m[:-1] > 0)[0]
            index_min_colum_co = where(values_co[:-1] > 0)[0]

            if len(index_min_colum) == 0:
                if len(index_min_colum_co) == 1:
                    index_min_colum = index_min_colum_co[0]
                else:
                    index_min_colum = where(values_co > 0)[0][
                        values_co[values_co > 0].argmax()
                    ]
            else:
                if len(index_min_colum) == 1:
                    index_min_colum = index_min_colum[0]
                else:
                    index_min_colum = where(values_m > 0)[0][
                        values_m[values_m > 0].argmax()
                    ]

            # Variable de Salida
            values_divide = (
                self.matrix[1:, width - 1, 1] / self.matrix[1:, index_min_colum, 1]
            )

            index_min_row = where(values_divide > 0)[0][
                values_divide[values_divide > 0].argmin()
            ]

            # Correcion basic_variables
            self.basic_variables[index_min_row + 1] = self.header[index_min_colum]

            # Dividir la fila
            self.matrix[index_min_row + 1, :, 1] /= self.matrix[
                index_min_row + 1, index_min_colum, 1
            ]

            # Cero la columna
            for i in range(height):
                fm_pv = self.matrix[i, index_min_colum, 0] * (-1)
                fc_pv = self.matrix[i, index_min_colum, 1] * (-1)
                for j in range(width):
                    if i == index_min_row + 1:
                        continue
                    if i == 0:
                        self.matrix[i, j, 0] += self.matrix[index_min_row + 1, j, 0] + (
                            self.matrix[index_min_row + 1, j, 1] * fm_pv
                        )
                        self.matrix[i, j, 1] += (
                            self.matrix[index_min_row + 1, j, 1] * fc_pv
                        )
                    else:
                        self.matrix[i, j, 1] += (
                            self.matrix[index_min_row + 1, j, 1] * fc_pv
                        )

            iterations += 1

            if iterations >= 100:
                return iterations, ("", 0)

        index_x = [(i, p) for i, p in enumerate(self.basic_variables) if "X" in p]
        solutions = [(p, self.matrix[i, -1, 1]) for i, p in index_x]

        return iterations, solutions

    def table_pandas(self):
        """
        Representa en forma de un DataFrame de pandas los valores de la tabla sin el valor de M
        """
        height = len(self.matrix)
        width = len(self.matrix[0])
        table = zeros((height, width), dtype="U10")

        for i in range(height):
            for j in range(width):
                if i == 0:
                    if self.matrix[i, j, 0] == 0:
                        table[i, j] = str(self.matrix[i, j, 1])
                    else:
                        if self.matrix[i, j, 1] == 0:
                            table[i, j] = str(self.matrix[i, j, 0]) + "M"
                        elif self.matrix[i, j, 1] > 0:
                            table[i, j] = (
                                str(self.matrix[i, j, 0])
                                + "M"
                                + " + "
                                + str(self.matrix[i, j, 1])
                            )
                        else:
                            table[i, j] = (
                                str(self.matrix[i, j, 0])
                                + "M "
                                + str(self.matrix[i, j, 1])
                            )

                else:
                    table[i, j] = str(self.matrix[i, j, 1])

        header = list(self.header) + ["LD"]
        vb = list(self.basic_variables)
        df = pd.DataFrame(table)
        df.columns = header
        df.index = vb
        return df, table

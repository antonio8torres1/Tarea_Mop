import numpy as np

class TableSimplex:
    def __init__(self, z, restriccion, ld, header, vb, option):
        self.row_z = z
        self.matrix = restriccion
        self.ld = ld
        self.header = header
        self.vb = vb
        self.option = option

    def __str__(self):
        table = ""
        height = len(self.ld) + 1
        width = len(self.vb) + 1
        leap = (width + 6)*4
        num_row = 0

        table += "\t\t TABLE"
        table += "\n" + "-"*leap +"\n"

        for i in range(height):
            if i > 0:
                table += "| " + self.vb[i - 1] + " "
            else:
                table += "| " + "VB"

            for j in range(width):
                if i == 0:
                    table += " |  " + str(self.header[j])
                    if j == width - 1:
                        table += " | " + "LD"
                elif i == 1:
                    if self.row_z[j] >= 0:
                        table += "|  " + str(np.round(self.row_z[j],1)) + "  "
                    if self.row_z[j] < 0:
                        table += "| " + str(np.round(self.row_z[j],1)) + "  "
                else:
                    if self.matrix[num_row][j] >= 0:
                        table += "|  " + str(np.round(self.matrix[num_row,j],1)) + "  "
                    if self.matrix[num_row][j] < 0:
                        table += "| " + str(np.round(self.matrix[num_row,j],1)) + "  "

            if i > 1:
                num_row += 1
            if i > 0 and i < height:
                if i == 1:
                    table += "|  " + str(np.round(self.ld[i - 1],1))
                else:
                    table += "|  " + str(np.round(self.ld[i - 1],1))

            table += "\n"
        return table

    def as_matrix(self):
        """
        Devuelve la tabla simplex como una lista de listas para mostrar en Streamlit.
        """
        table = []
        # Primera fila: encabezados + LD
        table.append(self.header + ["LD"])
        # Fila Z
        row_z = [np.round(x, 2) for x in self.row_z] + [np.round(self.ld[0], 2)]
        table.append(row_z)
        # Restricciones
        for i in range(self.matrix.shape[0]):
            row = [np.round(x, 2) for x in self.matrix[i]] + [np.round(self.ld[i+1], 2)]
            table.append(row)
        return table

    def solve(self):
        height = len(self.ld)
        iterations = 0
        if self.option ==  1:

            while (min_value := self.row_z[np.argmin(self.row_z)])  < 0:

                index_colum_min = np.argmin(self.row_z) # indice minimo de la fila z
                colum_temp = self.matrix[:,index_colum_min]       
                colum_divide = self.ld[1:] / colum_temp
                
                index_row_min = np.where(colum_divide > 0)[0][colum_divide[colum_divide > 0].argmin()] # indicce de la fila de restricion
                self.ld[index_row_min + 1] /= self.matrix[index_row_min,index_colum_min]
                self.matrix[index_row_min] /= self.matrix[index_row_min,index_colum_min]
                

                for i in range(height):

                    if i != index_row_min + 1:
                        if i == 0:
                            self.ld[i] += self.ld[index_row_min + 1] * self.row_z[index_colum_min] * (-1)
                            self.row_z += self.matrix[index_row_min] * self.row_z[index_colum_min] * (-1)
                            
                        else:
                            self.ld[i] += self.ld[index_row_min + 1] * self.matrix[i - 1,index_colum_min] * (-1)
                            self.matrix[i - 1] += self.matrix[index_row_min] * self.matrix[i - 1,index_colum_min] * (-1)
                iterations+=1

            return iterations

    def tablepandas():
        pass
        

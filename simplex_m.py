import numpy as np
from numpy import array,zeros, where, argmin, argmax, min, max, round,count_nonzero
import pandas as pd

class Simplex:

    def __init__(self, height:int , width:int,opts:int = 1) -> None:
            self.matrix = zeros((height, width,2), dtype=float)
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
                        table += "|      " + str(round(j[1],1))
                    else:
                        table += "|     " + str(round(j[1],1))

                elif j[0] > 0:
                    if j[1] > 0:
                        table += "| " + str(round(j[0],1))+ "M" + "+" + str(round(j[1],1))
                    if j[1] < 0:
                        table += "| " + str(round(j[0],1))+ "M" + str(round(j[1],1))
                    if j[1] == 0:
                        table += "|     " + str(round(j[0],1)) + "M"

                elif j[0] < 0:
                    if j[1] > 0:
                        table += "|" + str(round(j[0],1))+ "M" + "+" + str(round(j[1],1))
                    if j[1] < 0:
                        table += "|" + str(round(j[0],1))+ "M" + str(round(j[1],1))
                    if j[1] == 0:
                        table += "|    " + str(round(j[0],1)) + "M"

            table += "|"

        table += "\n----------------------------------------"

        return table

        
    def initialize(self,matrix,header,vb):
        """
        Iiniciliza la tabla para poder aplicar el metodo simplex
        """
        
        self.header = array(header)
        self.basic_variables = array(vb)

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                self.matrix[i,j,1] = matrix[i][j]

        index_positions = [where(self.header == p) for p in self.header if "A" in p]
        
        if self.opts == 0:
            for i in index_positions:
                self.matrix[0,i,0] = -1
        else:
            for i in index_positions:
                self.matrix[0,i,0] = 1


    def solve(self):
        height = len(self.matrix)
        width = len(self.matrix[0])
        iterations = 0

        #Iteracion previa
        for i in range(1,height):
            for j in range(width):
                self.matrix[0,j,0] += self.matrix[i,j,1]

        a = self.matrix[0,:-1,0]
        b = self.matrix[0,:-1,1]
        
        while (np.any(a > 0) or (np.all(a == 0) and np.any(b > 0))):

            #Variable de salida
            values_m = self.matrix[0,:-1,0]
            values_co = self.matrix[0,:-1,1]
        
            index_min_colum = where(values_m[:-1] > 0)[0]

            if len(index_min_colum) > 1:
                index_min_colum = values_co[index_min_colum].argmax()

        
            #Variable de entrada
            values_divide = self.matrix[1:,width - 1,1] / self.matrix[1:,index_min_colum,1]

            index_min_row = where(values_divide > 0)[0][values_divide[values_divide > 0].argmin()]

            #Dividir la fila
            self.matrix[index_min_row + 1,:,1] /= self.matrix[index_min_row + 1,index_min_colum,1]
            
            #Cero la columna
            for i in range(height):
                fm_pv = self.matrix[i,index_min_colum,0] * (-1)
                fc_pv = self.matrix[i,index_min_colum,1] * (-1)
                for j in range(width):
                    if i == index_min_row + 1:
                        continue
                    if i == 0:
                        self.matrix[i,j,0] += self.matrix[index_min_row + 1,j,0] +( self.matrix[index_min_row + 1,j,1] * fm_pv)
                        self.matrix[i,j,1] += self.matrix[index_min_row + 1,j,1] * fc_pv
                    else:
                        self.matrix[i,j,1] += self.matrix[index_min_row + 1,j,1] * fc_pv
                        
            iterations += 1
            
        return iterations

    def table_pandas(self):
        """
        Representa en forma de un DataFrame de pandas los valores de la tabla sin el valor de M
        """
        return pd.DataFrame(self.matrix[:,:,1])

import numpy as np
from numpy import array, dtype , zeros, where, argmin, argmax, min, max, round
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
                        table += "| " + str(round(j[0],1))+ "M" + "-" + str(round(j[1],1))
                    if j[1] == 0:
                        table += "|     " + str(round(j[0],1)) + "M"

                elif j[0] < 0:
                    if j[1] > 0:
                        table += "|" + str(round(j[0],1))+ "M" + "+" + str(round(j[1],1))
                    if j[1] < 0:
                        table += "|" + str(round(j[0],1))+ "M" + "-" + str(round(j[1],1))
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

        for i in index_positions:
            self.matrix[0,i,0] = 1
                
    
    def table_pandas(self):
        """
        Representa en forma de un DataFrame de pandas los valores de la tabla sin el valor de M
        """
        return pd.DataFrame(self.matrix[:,:,1])

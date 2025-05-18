from numpy import array
from simplex_m import Simplex

def main():
    
    matrix = [
        [5, 6, 0, 0, 0, 0,0],
        [2, 3, -1, 0, 1, 0,12],
        [2, 1, 0, -1, 0, 1,14]
    ]
    header = ["X1","X2","H1","H2","A1","A2"]
    ld = ["Z","A1","A2"]

    table = Simplex(3,7)
    table.initialize(matrix,header,ld)
    print(table)

if __name__ == "__main__":
    main()

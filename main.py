


import itertools
class Solver:
    def __init__(self):
        self.grid = [
            [3, 0, 6, 5, 0, 8, 4, 0, 0],
            [5, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 7, 0, 0, 0, 0, 3, 1],
            [0, 0, 3, 0, 1, 0, 0, 8, 0],
            [9, 0, 0, 8, 6, 3, 0, 0, 5],
            [0, 5, 0, 0, 9, 0, 6, 0, 0],
            [1, 3, 0, 0, 0, 0, 2, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 7, 4],
            [0, 0, 5, 2, 0, 6, 3, 0, 0]
        ]
        self.val = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.order = []
    
    def find_possibilities(self, i, j):
        # sourcery skip: merge-nested-ifs, use-itertools-product
        self.number_of_possibilities = 0
        self.verified = []

        # On trouve les possibilités dans la ligne
        for k in range(9):
            if self.grid[i][k] == 0 and k != j and (i, k) not in self.verified:
                self.verified.append((i, k))
                self.number_of_possibilities += 1

        # On trouve les possibilités dans la colonne
        for k in range(9):
            if self.grid[k][j] == 0 and k != i and (k, j) not in self.verified:
                self.verified.append((k, j))
                self.number_of_possibilities += 1

        # On trouve les possibilités dans le bloc
        i0 = (i // 3) * 3
        j0 = (j // 3) * 3
        for k in range(i0, i0 + 3):
            for l in range(j0, j0 + 3):
                if self.grid[k][l] == 0 and (k, l) != (i, j):
                    if (k, l) not in self.verified:
                        self.verified.append((k, l))
                        self.number_of_possibilities += 1
    
    def mrv(self):
        for i, j in itertools.product(range(9), range(9)):
            if self.grid[i][j] == 0:
                self.possibilities = self.find_possibilities(i, j)
                   
                    
G = Solver()
G.mrv()
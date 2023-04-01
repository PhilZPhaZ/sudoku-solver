import itertools
import sys

sys.setrecursionlimit(100000000)
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
        self.idx = 0
    
    def find_possibilities(self, i, j):
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
        for k, l in itertools.product(range(i0, i0 + 3), range(j0, j0 + 3)):
            if (
                self.grid[k][l] == 0
                and (k, l) != (i, j)
                and (k, l) not in self.verified
            ):
                self.verified.append((k, l))
                self.number_of_possibilities += 1
                
        self.order.append([i, j, self.number_of_possibilities])
    
    # Methode permettant de creer une liste des cases à parcourir pour remplir le sudoku
    def mrv(self):
        for i, j in itertools.product(range(9), range(9)):
            if self.grid[i][j] == 0:
                self.possibilities = self.find_possibilities(i, j)
        
        self.order.sort(key=lambda tup: tup[2])
        self.order = [tuple(x[:-1]) for x in self.order]
    
    def find_neigboor(self, i, j):
        self.neighboors = []
        
        # On trouve les cases remplies dans la ligne
        for k in range(9):
            if self.grid[i][k] != 0 and k != j:
                self.neighboors.append(self.grid[i][k])

        # On trouve les cases remplies dans la colonne
        for k in range(9):
            if self.grid[k][j] != 0 and k != i:
                self.neighboors.append(self.grid[k][j])
        
        # On trouve les possibilités dans le bloc
        i0 = (i // 3) * 3
        j0 = (j // 3) * 3
        for k, l in itertools.product(range(i0, i0 + 3), range(j0, j0 + 3)):
            if (
                self.grid[k][l] != 0
                and (k, l) != (i, j)
            ):
                self.neighboors.append(self.grid[k][l])
        
        return self.neighboors
     
    # Backtracking algorithme
    def backtrack(self):
        # On récupère la case à remplir en utilisant l'ordre trié par Degree
        if len(self.order) == 0:
            return True  # Toutes les cases sont remplies, on a trouvé une solution
        i, j = self.order.pop(0)[:2]


        # On cherche les valeurs possibles pour cette case
        for val in self.val:
            # On vérifie si la valeur est valide dans cette case
            if self.is_valid(i, j, val):
                # On remplit la case avec la valeur
                self.grid[i][j] = val

                # On passe à la case suivante
                if self.backtrack():
                    return True

                # Si on n'a pas trouvé de solution, on enlève la valeur
                self.grid[i][j] = 0

        # Si aucune valeur n'est valide, on revient en arrière
        self.order.insert(0, [i, j])
        return False
    
    def is_valid(self, i, j, val):
        # On vérifie que la valeur n'est pas déjà présente dans la ligne
        if val in self.grid[i]:
            return False

        # On vérifie que la valeur n'est pas déjà présente dans la colonne
        if val in [self.grid[k][j] for k in range(9)]:
            return False

        # On vérifie que la valeur n'est pas déjà présente dans le bloc
        i0 = (i // 3) * 3
        j0 = (j // 3) * 3
        return val not in [
            self.grid[k][l]
            for k, l in itertools.product(range(i0, i0 + 3), range(j0, j0 + 3))
        ]
    
    
    def solve(self):
        self.mrv()
        
        if self.backtrack():
            for line in self.grid:
                print(line)
        
G = Solver()
G.solve()
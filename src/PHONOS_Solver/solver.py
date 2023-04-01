import itertools
import sys
import tkinter as tk

sys.setrecursionlimit(100000000)


class Solver:
    def __init__(self, grid):
        self.grid = grid
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
            return self.grid


class SudokuGrid(tk.Frame):
    def __init__(self, master=tk.Tk()):
        super().__init__(master, bg='white')
        self.master = master
        self.create_puzzle()
        self.values = {}
        self.button_frame = tk.Frame(self.master)
        self.resolve = tk.Button(
            self.button_frame, text="Resoudre", command=self.resolve)
        self.resolve.pack(side=tk.LEFT, padx=10)
        self.delete = tk.Button(
            self.button_frame, text="Reset", command=self.reset)
        self.delete.pack(side=tk.LEFT, padx=10)
        self.button_frame.pack(pady=10)
        self.pack()
        self.master.mainloop()

    def resolve(self):
        self.grid = []
        for x in range(9):
            self.line = []

            for y in range(9):
                if (x, y) in self.values:
                    self.line.append(self.values[(x, y)])
                else:
                    self.line.append(0)
            self.grid.append(self.line)
        self.solution = Solver(self.grid)
        self.solution = self.solution.solve()

        self.update_cells()

    def create_puzzle(self):
        # Add the 3 * 3 big blocks
        self.blocks = []
        for r in range(3):  # `r` like `row`
            row = []
            for c in range(3):  # `c` like `column`
                frame = tk.Frame(self, bd=1, highlightbackground='light blue',
                                 highlightcolor='light blue', highlightthickness=1)
                frame.grid(row=r, column=c, sticky='nsew')
                row.append(frame)
            self.blocks.append(row)

        # Add the 9 * 9 cells
        self.cells = [[None] * 9 for _ in range(9)]
        for i, j in itertools.product(range(9), range(9)):
            # Add cell to the block
            # Add a frame so that the cell can form a square
            frm_cell = tk.Frame(self.blocks[i // 3][j // 3])
            frm_cell.grid(row=(i % 3), column=(j % 3), sticky='nsew')
            frm_cell.rowconfigure(0, minsize=50, weight=1)
            frm_cell.columnconfigure(0, minsize=50, weight=1)

            # Use an Entry widget to allow for text input
            cell = tk.Entry(frm_cell, justify='center')
            cell.grid(sticky='nsew')
            cell.bind('<Return>', self.handle_keypress)
            self.cells[i][j] = cell

    def handle_keypress(self, event):
        # When the "Return" key is pressed, focus goes to the next cell
        current_cell = self.master.focus_get()
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                if cell == current_cell:
                    if value := cell.get():
                        self.values[(i, j)] = int(value)
                    else:
                        self.values.pop((i, j), None)
                    if i == 8 and j == 8:
                        # If the current cell is the last cell, focus goes to the first cell
                        self.cells[0][0].focus()
                    elif j == 8:
                        # If the current cell is the last cell in a row, focus goes to the first cell in the next row
                        self.cells[i+1][0].focus()
                    else:
                        # Otherwise, focus goes to the next cell in the same row
                        self.cells[i][j+1].focus()

    def update_cells(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                self.value = self.solution[i][j]
                cell.delete(0, tk.END)
                cell.insert(0, self.value)

    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.delete(0, tk.END)

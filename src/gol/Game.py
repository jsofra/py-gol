class Cell:
    dirs = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    
    def __init__(self, board, x, y, state):
        self.board = board
        self.x, self.y = (x, y)
        self.state = state
        self.next_state = None
        
        if self.state:
            for (nx, ny) in self.get_neigbour_coords():
                if (nx, ny) not in self.board:
                    board[(nx, ny)] = Cell(self.board, nx, ny, False)
    
    def get_neigbour_coords(self):
        return [(self.x + u, self.y + v) for (u, v) in Cell.dirs]
    
    def live_neighbours(self):
        return len([self.board[coord] for coord in self.get_neigbour_coords()
                    if coord in self.board and self.board[coord].state])
    
    def update_next_state(self):
        live = self.live_neighbours()
        self.next_state = live == 3 or (live == 2 and self.state)
              
    def cycle(self):
        if self.next_state:
            self.board[(self.x, self.y)] = Cell(self.board, self.x, self.y, True)
        else:
            del self.board[(self.x, self.y)]

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)
    
class Board:
    def __init__(self, cell_coords):
        self.cell_dict = {}
        for (x, y) in cell_coords:
            self.cell_dict[(x, y)] = Cell(self.cell_dict, x, y, True)
    
    def cycle(self):
        for cell in self.cell_dict.values():
            cell.update_next_state()
        for cell in self.cell_dict.values():
            cell.cycle()
    
    def get_live_cells(self):
        return [cell for cell in self.cell_dict.values() if cell.state]
        
if __name__ == '__main__':
    # create a glider
    board = Board(((1, 0), (1, 1), (1, 2)))
    print board.get_live_cells()
    board.cycle()
    print board.get_live_cells()
    board.cycle()
    print board.get_live_cells()
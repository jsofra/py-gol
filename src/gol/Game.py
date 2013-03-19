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
    
    def get_neighbours(self):
        return [self.board[coord] for coord in self.get_neigbour_coords() if coord in self.board]
    
    def live_neighbours(self):
        return [neighbour for neighbour in self.get_neighbours() if neighbour.state]
    
    def update_next_state(self):
        live = len(self.live_neighbours())
        self.next_state = live == 3 or (live == 2 and self.state)
              
    def cycle(self):
        if self.next_state:
            self.board[(self.x, self.y)] = Cell(self.board, self.x, self.y, True)
        else:
            del self.board[(self.x, self.y)]
    
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
    board = Board(((1, 0), (1, 1), (1, 2)))
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
    board.cycle()
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
    board.cycle()
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
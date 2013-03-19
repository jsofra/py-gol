class Cell:
    dirs = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    
    def __init__(self, board, x, y):
        self.board = board
        self.x, self.y = (x, y)
        self.next_state = self

    def get_neigbour_coords(self):
        return [(self.x + u, self.y + v) for (u, v) in Cell.dirs]
    
    def live_neighbours(self):
        return len([self.board[coord] for coord in self.get_neigbour_coords()
                    if coord in self.board and self.board[coord].is_live()])

    def cycle(self):
        if self.next_state:
            self.board[(self.x, self.y)] = LiveCell(self.board, self.x, self.y)
        else:
            del self.board[(self.x, self.y)]

class LiveCell(Cell):
    def __init__(self, board, x, y):
        Cell.__init__(self, board, x, y)
        for (nx, ny) in self.get_neigbour_coords():
            if (nx, ny) not in self.board:
                board[(nx, ny)] = DeadCell(self.board, nx, ny) 

    def is_live(self):
        return True
    
    def update_next_state(self):
        self.next_state = 2 <= self.live_neighbours() <= 3

class DeadCell(Cell):
    def __init__(self, board, x, y):
        Cell.__init__(self, board, x, y)
        
    def is_live(self):
        return False
    
    def update_next_state(self):
        self.next_state = self.live_neighbours() == 3

class Board:
    def __init__(self, cell_coords):
        self.cell_dict = {}
        for (x, y) in cell_coords:
            self.cell_dict[(x, y)] = LiveCell(self.cell_dict, x, y)
    
    def cycle(self):
        for cell in self.cell_dict.values():
            cell.update_next_state()
        for cell in self.cell_dict.values():
            cell.cycle()
    
    def get_live_cells(self):
        return [cell for cell in self.cell_dict.values() if cell.is_live()]
        
if __name__ == '__main__':
    board = Board(((1, 0), (1, 1), (1, 2)))
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
    board.cycle()
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
    board.cycle()
    print [(cell.x, cell.y) for cell in board.get_live_cells()]
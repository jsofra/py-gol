class Cell:    
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.next_state = self

    def get_next_state(self):
        return self.next_state

    def get_neigbour_coords(self):
        return [(self.x + u, self.y + v) 
            for u in (-1, 0, 1) 
            for v in (-1, 0, 1) if (u, v) != (0, 0)]
            
    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

class LiveCell(Cell):
    def __init__(self, x, y):
        Cell.__init__(self, x, y)

    def is_live(self):
        return True
    
    def update_next_state(self, live_neighbours):
        if live_neighbours < 2 or live_neighbours > 3:
            self.next_state = DeadCell(self.x, self.y)

class DeadCell(Cell):
    def __init__(self, x, y):
        Cell.__init__(self, x, y)
        
    def is_live(self):
        return False
    
    def update_next_state(self, live_neighbours):
        if live_neighbours == 3:
            self.next_state = LiveCell(self.x, self.y)

class Board:
    def __init__(self, cell_coords):
        self.cell_dict = {}
        for (x, y) in cell_coords:
            cell = LiveCell(x, y)
            self.cell_dict[(x, y)] = cell
            self.create_dead_buffer(cell)
    
    def live_neighbours(self, cell):
        return len([self.cell_dict[coord] for coord in cell.get_neigbour_coords()
                    if coord in self.cell_dict and self.cell_dict[coord].is_live()])
    
    def create_dead_buffer(self, cell):
        # if it is a new live cell create dead cells around it so that
        # they can potentially become live cells in the next generation
        for (x, y) in cell.get_neigbour_coords():
            if (x, y) not in self.cell_dict:
                self.cell_dict[(x, y)] = DeadCell(x, y) 
    
    def cycle(self):
        cells = self.cell_dict.values()
        for cell in cells:
            cell.update_next_state(self.live_neighbours(cell))
        for cell in self.cell_dict.values():
            if (not cell.is_live()) and (not cell.get_next_state().is_live()):
                # delete dead cells
                del self.cell_dict[(cell.x, cell.y)]
        for cell in self.cell_dict.values():   
            if cell.get_next_state().is_live():
                # maintain dead buffer
                self.create_dead_buffer(cell)
        for cell in self.cell_dict.values():
            # swap state
            self.cell_dict[(cell.x, cell.y)] = cell.get_next_state()
    
    def get_live_cells(self):
        return [cell for cell in self.cell_dict.values() if cell.is_live()]
        
if __name__ == '__main__':
    # create a glider
    board = Board(((1, 0), (1, 1), (1, 2)))
    print board.get_live_cells()
    board.cycle()
    print board.get_live_cells()
    board.cycle()
    print board.get_live_cells()
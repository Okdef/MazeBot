from tkinter import Tk, BOTH, Canvas
from time import sleep
import random


############# Window Class ##########
#              This class creates the GUI window amnd controls it
class Window:
    def __init__(self,width,height, Title = "Notitle"):
        self.root_widget = Tk()
        self.root_widget.title("NoTitle")
        self.canvas = Canvas(self.root_widget, bg = "white")
        self.canvas.pack(fill=BOTH)
        self.is_running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root_widget.update()
        self.root_widget.update_idletasks()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

##this stores the coordinates of a point##
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

########## Line Class #############
class Line:
    def __init__(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.y
        self.x2 = point2.x
        self.y2 = point2.y

    def draw(self, canvas, fill_color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=fill_color, width=2)
        canvas.pack(fill=BOTH)

# Cell Class
# this class is responsible fot the cells of the maze
class Cell:
    def __init__(self, point1, point2, _win = None, left_wall = True ,right_wall = True,top_wall = True,bottom_wall = True):
        self._win = _win
        #walls stores the existance of a wall in each direction. This allows the use of loops and helps make the code more readable
        self.walls = {"left":left_wall, "right":right_wall, "up":top_wall, "down":bottom_wall}
        self.x1 = point1.x
        self.x2 = point2.x
        self.y1 = point1.y
        self.y2 = point2.y
        #adj is the adjacent cell in the respective direction. This may be more elegantly implemented with a dictionary as is seen with the walls dict
        self.adj_left = None
        self.adj_right = None
        self.adj_top = None
        self.adj_bottom = None
        #visited stores wether a cell has been interacted with by a method, this needs to be reset to function correctly between method executions
        self.visited = False


        ##Points##
        self.tl = Point(self.x1,self.y1)
        self.tr = Point(self.x2,self.y1)
        self.bl = Point(self.x1,self.y2)
        self.br = Point(self.x2,self.y2)
        self.mid = Point(((self.x1+self.x2)/2), ((self.y1+self.y2)/2))
        
        ##Lines##
        self.left = Line(self.tl, self.bl)
        self.right = Line(self.tr, self.br)
        self.top = Line(self.tl, self.tr)
        self.bottom = Line(self.bl, self.br)
    
    #draw visualizes the cell
    def draw(self):#
        if self._win is not None:
            if self.walls["left"]:
                self.left.draw(self._win.canvas, "black")
            if self.walls["right"]:
                self.right.draw(self._win.canvas, "black")
            if self.walls["up"]:
                self.top.draw(self._win.canvas, "black")
            if self.walls["down"]:
                self.bottom.draw(self._win.canvas, "black")
            
            #NOTS
            #these check if the walls are not present, if not, they are "deleted" by drawing in white overtop of the black lines.
            if not self.walls["left"]:
                self.left.draw(self._win.canvas, "white")
            if  not self.walls["right"]:
                self.right.draw(self._win.canvas, "white")
            if not self.walls["up"]:
                self.top.draw(self._win.canvas, "white")
            if not self.walls["down"]:
                self.bottom.draw(self._win.canvas, "white")

    #draw_move visualizes the movement of the "solve" function
    def draw_move(self,to_cell, undo=False):
        move_line = Line(self.mid, to_cell.mid)
        if undo == False:
            move_line.draw(self._win.canvas, fill_color = "red")
        else:
            move_line.draw(self._win.canvas, fill_color = "blue")

    def has_path(self, adjacent_cell):  
        if adjacent_cell == self.adj_right:
            return self.walls["right"] == False and adjacent_cell.walls["left"] == False
        elif adjacent_cell == self.adj_left:
            return self.walls["left"] == False and adjacent_cell.walls["right"] == False
        elif adjacent_cell == self.adj_top:
            return self.walls["up"] == False and adjacent_cell.walls["down"] == False
        elif adjacent_cell == self.adj_bottom:
            return self.walls["down"] == False and adjacent_cell.walls["up"] == False

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        #seed is the seed used to generate the maze
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self._create_cells()
        self._break_walls_r(self._cells[0][0])
        self._reset_cells_visited()
        #solved allows us to access the status on the maze solution
        self.solved = self._solve()
        #I reset this to check the testcase for reset, this serves no practical function
        self._reset_cells_visited()
        
    #this creates a grid and then breaks the grid into a maze before building the adjacencies for each cell
    def _create_cells(self):
        self._cells = [[[None] for _  in range(self.num_rows)] for _ in range(self.num_cols)]
        start = self.x1
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self.node_p1 = Point(self.x1,self.y1)
                self.node_p2 = Point(self.x1+self.cell_size_x, self.y1+self.cell_size_y)
                cell_node = Cell(self.node_p1, self.node_p2, self.win)
                cell_node.draw()
                self.x1 += self.cell_size_x
                self._cells[i][j] = cell_node
            self.x1 = start
            self.y1 += self.cell_size_y
        self._break_enterance_and_exit()
        self._adjacency_builder()
        self._animate()

    def _animate(self):
        if self.win is not None:
            self.win.redraw()
            sleep(0.05)

    #this creates the openings for the maze
    def _break_enterance_and_exit(self):
        top_cell = self._cells[0][0]
        bottom_cell = self._cells[-1][-1]
        top_cell.walls["up"] = False
        bottom_cell.walls["down"] = False
        top_cell.draw()
        bottom_cell.draw()

    #this "breaks" the walls to turn the generated grid into a maze
    def _break_walls_r(self, i=None, j=None):
        current = i
        current.visited = True
        while current:
            can_visit = [i,j]
            unvisited = {}
            if current.adj_left is not None:
                if current.adj_left.visited == False:
                    unvisited["left"] = (current.adj_left)
            if current.adj_right is not None:
                if current.adj_right.visited == False:
                    unvisited["right"] = (current.adj_right)
            if current.adj_top is not None:
                if current.adj_top.visited == False:
                    unvisited["up"] = (current.adj_top)
            if current.adj_bottom is not None:
                if current.adj_bottom.visited == False:
                    unvisited["down"] = (current.adj_bottom)
            
            if unvisited == {}:
                current.draw()
                return
            else:
                selected = random.choice(list(unvisited.keys()))#this selects a random direction and breaks the selected wall
                current.walls[selected] = False
                unvisited[selected].walls[self.opposite(selected)] = False
                self._break_walls_r(unvisited[selected])
            
    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False
            
    #this allows the adjacent cells to a cell to be checked
    def _adjacency_builder(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                cell_node = self._cells[i][j]
                if j-1 >= 0:
                    cell_node.adj_left = self._cells[i][j-1]
                if j+1  < len(self._cells[i]):
                    cell_node.adj_right = self._cells[i][j+1]
                if i-1 >= 0:
                    cell_node.adj_top = self._cells[i-1][j]
                if i+1  < len(self._cells):
                    cell_node.adj_bottom = self._cells[i+1][j]
                #print(self._cells[i][j].adj_bottom)
    
    def _solve(self):
        return self._solve_r(self._cells[0][0])

    #this actually does the solving
    def _solve_r(self,current):
        current.visited = True
        if current == self._cells[-1][-1]:
            return True
        for direction in ['adj_left', 'adj_right', 'adj_top', 'adj_bottom']:
            next_cell = getattr(current, direction)
            if next_cell is not None and not next_cell.visited and current.has_path(next_cell):
                if self.win is not None: current.draw_move(next_cell)
                if self._solve_r(next_cell):
                    return True
                if self.win is not None: current.draw_move(next_cell, undo=True)
        return False
    
    def opposite(self,direction):
        if direction == "left":
            return "right"
        if direction == "right":
            return "left"
        if direction == "up":
            return "down"
        if direction == "down":
            return "up"
        else:
            print(f"opposite OOB{direction}")

   
        
def main():
    win = Window(800, 600)
    mz = Maze(10,10,3,2,100,100,win)
    win.wait_for_close()
    return mz.solved

    

if __name__ == "__main__":
    main()

##
#O
#K
##
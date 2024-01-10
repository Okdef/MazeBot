from tkinter import Tk, BOTH, Canvas
from time import sleep
import random


############# Window Class ##########
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

class Cell:
    def __init__(self, point1, point2, _win = None, left_wall = True ,right_wall = True,top_wall = True,bottom_wall = True):
        self._win = _win
        self.left_wall = left_wall
        self.right_wall = right_wall
        self.top_wall = top_wall
        self.bottom_wall = bottom_wall
        self.x1 = point1.x
        self.x2 = point2.x
        self.y1 = point1.y
        self.y2 = point2.y
        self.adj_left = None
        self.adj_right = None
        self.adj_top = None
        self.adj_bottom = None
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
    
    def draw(self):
        if self._win is not None:
            if self.left_wall:
                self.left.draw(self._win.canvas, "black")
            if self.right_wall:
                self.right.draw(self._win.canvas, "black")
            if self.top_wall:
                self.top.draw(self._win.canvas, "black")
            if self.bottom_wall:
                self.bottom.draw(self._win.canvas, "black")
            
            #NOTS
            if not self.left_wall:
                self.left.draw(self._win.canvas, "white")
            if  not self.right_wall:
                self.right.draw(self._win.canvas, "white")
            if not self.top_wall:
                self.top.draw(self._win.canvas, "white")
            if not self.bottom_wall:
                self.bottom.draw(self._win.canvas, "white")

    def draw_move(self,to_cell, undo=False):
        move_line = Line(self.mid, to_cell.mid)
        if undo == False:
            move_line.draw(self._win.canvas, fill_color = "red")
        else:
            move_line.draw(self._win.canvas, fill_color = "blue")

    def has_path(self, adjacent_cell):  
        if adjacent_cell == self.adj_right:
            return self.right_wall == False and adjacent_cell.left_wall == False
        elif adjacent_cell == self.adj_left:
            return self.left_wall == False and adjacent_cell.right_wall == False
        elif adjacent_cell == self.adj_top:
            return self.top_wall == False and adjacent_cell.bottom_wall == False
        elif adjacent_cell == self.adj_bottom:
            return self.bottom_wall == False and adjacent_cell.top_wall == False

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)
        self._create_cells()
        self._break_walls_r(self._cells[0][0])
        self._reset_cells_visited()
        self._solve()
        

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

    def _break_enterance_and_exit(self):
        top_cell = self._cells[0][0]
        bottom_cell = self._cells[-1][-1]
        top_cell.top_wall = False
        bottom_cell.bottom_wall = False
        top_cell.draw()
        bottom_cell.draw()

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
                    unvisited["top"] = (current.adj_top)
            if current.adj_bottom is not None:
                if current.adj_bottom.visited == False:
                    unvisited["bottom"] = (current.adj_bottom)
            
            if unvisited == {}:
                current.draw()
                return
            else:
                selected = random.choice(list(unvisited.keys()))
                if selected == "left":
                    current.left_wall = False
                    unvisited[selected].right_wall = False
                if selected == "right":
                    current.right_wall = False
                    unvisited[selected].left_wall = False
                if selected == "top":
                    current.top_wall = False
                    unvisited[selected].bottom_wall = False
                if selected == "bottom":
                    current.bottom_wall = False
                    unvisited[selected].top_wall = False
                self._break_walls_r(unvisited[selected])
            
    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False
            

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
                print(self._cells[i][j].adj_bottom)
    
    def _solve(self):
        return self._solve_r(self._cells[0][0])


    def _solve_r(self,current):
        current.visited = True
        if current == self._cells[-1][-1]:
            return True
        for direction in ['adj_left', 'adj_right', 'adj_top', 'adj_bottom']:
            next_cell = getattr(current, direction)
            if next_cell is not None and not next_cell.visited and current.has_path(next_cell):
                current.draw_move(next_cell)
                if self._solve_r(next_cell):
                    return True
                current.draw_move(next_cell, undo=True)
        return False
   
        
def main():
    win = Window(800, 600)
    mz = Maze(10,10,3,2,100,100,win)
    win.wait_for_close()

    

if __name__ == "__main__":
    main()

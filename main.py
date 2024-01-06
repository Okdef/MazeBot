from tkinter import Tk, BOTH, Canvas
from time import sleep

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

    def draw_move(self,to_cell, undo=False):
        move_line = Line(self.mid, to_cell.mid)
        if undo == False:
            move_line.draw(self._win.canvas, fill_color = "red")
        else:
            move_line.draw(self._win.canvas, fill_color = "grey")

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

    def _create_cells(self):
        self._cells = [[None] * self.num_rows] * self.num_cols
        start = self.x1
        for i in self._cells:
            for j in i:
                self.node_p1 = Point(self.x1,self.y1)
                self.node_p2 = Point(self.x1+self.cell_size_x, self.y1+self.cell_size_y)
                cell_node = Cell(self.node_p1, self.node_p2, self.win)
                j = cell_node
                cell_node.draw()
                self.x1 += self.cell_size_x
            self.x1 = start
            self.y1 += self.cell_size_y
        self._animate()

    def _animate(self):
        if self.win is not None:
            self.win.redraw()
            sleep(0.05)

        
def main():
    win = Window(800, 600)
    mz = Maze(10,10,3,2,100,100,win)
    win.wait_for_close()

    

if __name__ == "__main__":
    main()

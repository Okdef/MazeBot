from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self,width,height):
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
        is_running = True
        while is_running:
            self.redraw()

    def close(self):
        is_running = False

def main(self):
    win = Window(800, 600)
    win.wait_for_close()
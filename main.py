from tkinter import Tk, BOTH, Canvas

class Window:
    root_widget = Tk()
    root_widget.title = "NoTitle"
    canvas = Canvas(root_widget, {"bg" : "white"})
    canvas.pack()
    is_running = False

    def redraw():
        root_widget.update()
        root_widget.update_idletasks()
        
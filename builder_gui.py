import tkinter as tk
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent.absolute()))

# six grids or 'faces' of three rows each, each row with three columns
sticker_width = 60

facelets = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]
face_names = ('U', 'F', 'R', 'B', 'L', 'D')

curcolour = None
colours = ('white', 'green', 'red', 'blue', 'orange', 'yellow')
colourpickers = [0 for i in range(6)]

cubedefinition = ''


def create_facelets(width):
    """create facelets on canvas, param: width refers to width of individual faces"""
    global canvas, facelets, face_names, tk
    # (x, y) offset for each face, 1 = 1 face
    offset = ((1, 0), (1, 1), (2, 1), (3, 1), (0, 1), (1, 2))

    for face in range(6):
        for row in range(3):
            y = offset[face][1] * 3 * width + row * width
            for col in range(3):
                x = offset[face][0] * 3 * width + col * width
                facelets[face][row][col] = canvas.create_rectangle(x, y, x + width, y + width, fill='grey')
                if row == 1 and col == 1:
                    canvas.create_text(x + width // 2, y + width // 2, text=face_names[face], state=tk.DISABLED)

    for face in range(6):
        canvas.itemconfig(facelets[face][1][1], fill=colours[face])


def create_colourpickers(width):
    """ create the colour picker pallette on canvas, param: width refers to size of each colour's box"""
    global curcolour
    global colours, colourpickers
    global canvas

    for i in range(6):
        x = (i % 3) * (width + 5) + 7 * width
        y = (i // 3) * (width + 5) + 7 * width
        colourpickers[i] = canvas.create_rectangle(x, y, x + width, y + width, fill=colours[i])
        canvas.itemconfig(colourpickers[0], width=4)
        curcolour = colours[0]


def click(event):
    """on left mouse-clicks, change current colour if clicked colour picker, else configure the colour of the clicked"""
    global curcolour
    global canvas
    idlist = canvas.find_withtag("current")
    if len(idlist) > 0:
        if idlist[0] in colourpickers:
            curcolour = canvas.itemcget("current", "fill")
            for i in range(6):
                canvas.itemconfig(colourpickers[i], width=1)

            canvas.itemconfig('current', width=5)

        else:
            canvas.itemconfig('current', fill=curcolour)


def clean():
    global canvas
    for face in range(6):
        for row in range(3):
            for col in range(3):
                canvas.itemconfig(facelets[face][row][col], fill=canvas.itemcget(facelets[face][1][1], "fill"))


def empty():
    global canvas
    for face in range(6):
        for row in range(3):
            for col in range(3):
                if row != 1 or col != 1:
                    canvas.itemconfig(facelets[face][row][col], fill='grey')


def build():
    import rubiks.cube, cube
    global canvas, root
    definition = ''
    for face in range(6):
        for row in range(3):
            for col in range(3):
                definition += canvas.itemcget(facelets[face][row][col], "fill")[0]

    rubiks.cube.cubedefinition = definition
    cube.cubedefinition = definition
    root.destroy()


# mainloop
if 'cube' in __name__ or __name__ == '__main__':
    root = tk.Tk()
    root.title('Cube Builder')
    canvas = tk.Canvas(root, width=12 * sticker_width + 50, height=9 * sticker_width + 50)
    canvas.pack()

    # buttons
    bbuild = tk.Button(text='Build', height=2, width=10, relief=tk.RAISED, command=build)
    bbuild_window = canvas.create_window(10 + 10.5 * sticker_width, 10 + 6.5 * sticker_width, anchor=tk.NW,
                                         window=bbuild)

    bclean = tk.Button(text='Clean', height=2, width=10, relief=tk.RAISED, command=clean)
    bclean_window = canvas.create_window(10 + 10.5 * sticker_width, 10 + 7.5 * sticker_width, anchor=tk.NW,
                                         window=bclean)

    bempty = tk.Button(text='Empty', height=2, width=10, relief=tk.RAISED, command=empty)
    bempty_window = canvas.create_window(10 + 10.5 * sticker_width, 10 + 8.5 * sticker_width, anchor=tk.NW,
                                         window=bempty)

    # bind left mouse clicks to click()
    canvas.bind("<Button-1>", click)
    create_facelets(sticker_width)
    create_colourpickers(sticker_width)

    root.mainloop()

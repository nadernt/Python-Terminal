from tkinter import StringVar, Tk, Radiobutton, W, mainloop

MODES = [
    ("Monochrome", "1"),
    ("Grayscale", "L"),
    ("True color", "RGB"),
    ("Color separation", "CMYK"),
]
master = Tk()

v = StringVar()
v.set("L")  # initialize
b = list()
for text, mode in MODES:
    b = Radiobutton(master, text=text,
                    variable=v, value=mode)
print(b)
b[0].pack(anchor=W)
mainloop()

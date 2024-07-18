
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/man44/Documents/imager/landing/assets1/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def center_window(window,height=600,width=500):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def open_page2():
    uname=entry_1.get()
    password=entry_2.get()
    if (uname=="admin" and password=="admin"):
        global window_position
        window_position = (window.winfo_x(), window.winfo_y())
        window.destroy()
        import sys
        # sys.path.append("build")
        import gui2
    else:
        messagebox.showwarning("Warning", "Inavlid Username Password!")


window = Tk()
window.title("IYD")
center_window(window)
window.geometry("600x500")
window.configure(bg = "#F2F2F2")


canvas = Canvas(
    window,
    bg = "#F2F2F2",
    height = 500,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    280.0,
    600.0,
    505.0,
    fill="#535151",
    outline="")

canvas.create_rectangle(
    127.0,
    326.0,
    412.0,
    479.0,
    fill="#F2F2F2",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    474.0,
    157.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    182.0,
    168.0,
    image=image_image_2
)

canvas.create_rectangle(
    152.0,
    360.0,
    384.0,
    395.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    152.0,
    416.0,
    384.0,
    451.0,
    fill="#D9D9D9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: print("button_1 clicked"),
    command=open_page2,
    relief="flat"
)
button_1.place(
    x=441.0,
    y=387.0,
    width=41.0,
    height=37.0
)

canvas.create_rectangle(
    188.0,
    361.0,
    384.0,
    394.0,
    fill="#A7A5A5",
    outline="")

canvas.create_rectangle(
    188.0,
    417.0,
    384.0,
    450.0,
    fill="#A7A5A5",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    290.5,
    377.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#A7A5A5",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=197.0,
    y=362.0,
    width=187.0,
    height=28.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    290.5,
    433.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#A7A5A5",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=197.0,
    y=418.0,
    width=187.0,
    height=28.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    169.0,
    376.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    168.0,
    435.0,
    image=image_image_4
)
window.resizable(False, False)
window.mainloop()
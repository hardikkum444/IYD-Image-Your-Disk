from pathlib import Path

# from tkinter import *
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
window.configure(bg = "#C4C4C4")
center_window(window)
window.geometry("600x500")



canvas = Canvas(
    window,
    bg = "#C4C4C4",
    height = 500,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    170.0,
    142.0,
    image=image_image_1
)

canvas.create_rectangle(
    325.0,
    0.0,
    600.0,
    500.0,
    fill="#222222",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    463.0,
    172.0,
    image=image_image_2
)

canvas.create_rectangle(
    347.0,
    237.0,
    579.0,
    272.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    383.0,
    238.0,
    579.0,
    271.0,
    fill="#A7A5A5",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    483.5,
    255.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#A7A5A5",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=390.0,
    y=240.0,
    width=187.0,
    height=28.0
)

canvas.create_rectangle(
    347.0,
    301.0,
    579.0,
    336.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    383.0,
    302.0,
    579.0,
    335.0,
    fill="#A7A5A5",
    outline="")

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    483.5,
    319.0,
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
    x=390.0,
    y=304.0,
    width=187.0,
    height=28.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    365.0,
    322.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    365.0,
    255.0,
    image=image_image_4
)

next_button = Button(window, text="Login", command=open_page2, width=8, bg="#333333", fg="white")
next_button.place(x=424, y=377)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    158.0,
    371.0,
    image=image_image_5
)
window.resizable(False, False)
window.mainloop()

from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import font as tkfont

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/man44/Documents/imager/landing/assets2/frame0")

def create_image():
    window.destroy()
    import sys
    # sys.path.append("build")
    import gui3

def gen_report():
    window.destroy()
    import sys
    import gui5

def center_window(window,height=600,width=500):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("IYD")

window.configure(bg = "#202020")
center_window(window)
window.geometry("600x500")




canvas = Canvas(
    window,
    bg = "#202020",
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
    130.0,
    261.0,
    image=image_image_1
)

canvas.create_rectangle(
    267.0,
    0.0,
    600.0,
    500.0,
    fill="#545252",
    outline="")

large_font = tkfont.Font(family="JetBrains Mono", size=16, weight="bold")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,
    text="CREATE IMAGE",
    font=large_font,
    # image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    highlightbackground="#6C6C6C",
    command=create_image,
    relief="flat",
    bg="#6C6C6C",
    fg="white"
)
button_1.place(
    x=300.0,
    y=51.0,
    width=257.0,
    height=75.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    # image=button_image_2,
    borderwidth=0,
    text="DECRYPT RAW IMAGE",
    highlightthickness=0,
    highlightbackground="#6C6C6C",
    relief="flat",
    font=large_font,
    bg="#6C6C6C",
    fg="white"
)
button_2.place(
    x=300.0,
    y=159.0,
    width=257.0,
    height=75.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    # image=button_image_3,
    borderwidth=0,
    text="MOUNT IMAGE",
    highlightthickness=0,
    highlightbackground="#6C6C6C",
    relief="flat",
    font=large_font,
    bg="#6C6C6C",
    fg="white"
)
button_3.place(
    x=300.0,
    y=268.0,
    width=257.0,
    height=75.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    # image=button_image_4,
    borderwidth=0,
    text="GET DRIVE REPORT",
    highlightthickness=0,
    highlightbackground="#6C6C6C",
    relief="flat",
    command=gen_report,
    font=large_font,
    bg="#6C6C6C",
    fg="white"
)
button_4.place(
    x=300.0,
    y=374.0,
    width=257.0,
    height=75.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    130.0,
    385.0,
    image=image_image_2
)
window.resizable(False, False)
window.mainloop()

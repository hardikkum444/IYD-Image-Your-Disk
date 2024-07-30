from pathlib import Path
import subprocess, os
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label, messagebox, Checkbutton, simpledialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets7/frame0")

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
window.title("IYD Mounting Image File")
center_window(window)
window.geometry("600x500")
window.configure(bg = "#545252")

canvas = Canvas(
    window,
    bg = "#545252",
    height = 500,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    271.0,
    500.0,
    fill="#212121",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    135.0,
    226.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=304.0,
    y=43.0,
    width=259.3500061035156,
    height=72.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_2.place(
    x=291.0,
    y=171.0,
    width=289.0,
    height=212.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    427.0,
    236.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=327.0,
    y=219.0,
    width=200.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    349.5,
    328.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=314.0,
    y=311.0,
    width=71.0,
    height=32.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    135.0,
    390.0,
    image=image_image_2
)

def on_next_click1():
    path = entry_1.get()
    rd_only = read_only.get()
    offset = entry_2.get()
    try:
        offset = int(offset)
    except ValueError:
        messagebox.showwarning("Warning", "Offset must be a valid integer.")
        return

    if rd_only == 1:
        command = ["sudo", "mount", "-o", f"loop,ro,offset={offset}", path, "/mnt"]
    else:
        command = ["sudo", "mount", "-o", f"loop,offset={offset}", path, "/mnt"]

    try:
        subprocess.run(command, check=True)
        print("Mount successful.")
        messagebox.showinfo("Mounted successfully, please check /mnt")
        window.destroy()
    except subprocess.CalledProcessError as e:
        print(f"Error mounting: {e}")
        messagebox.showwarning("Warning", "Error mounting")



def on_back_click():
    window.destroy()
    import sys
    subprocess.run(["python3", "gui2.py"])


def on_checkbox_click1():
    if read_only.get() == 1:
        print("read only")

    else:
        print("not read only")



read_only = IntVar()
checkbutton_encr = Checkbutton(
    window,
    text="Mount-Read Only",
    variable=read_only,
    onvalue=1,
    offvalue=0,
    width=13,
    command=on_checkbox_click1,
    bg="#545252",
    font=("Arial", 12),
    relief="raised",
    padx=10,
    pady=5,

)
checkbutton_encr.place(x=291, y=395)


mount_button = Button(window, text="Mount", command=on_next_click1, width=10, bg="#333333", fg="white")
mount_button.place(x=452, y=445)

back_button = Button(window, text="Back", command=on_back_click, width=10, bg="#333333", fg="white")
back_button.place(x=291, y=445)

def browse_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_1.insert(0, file_path)


browse_button = Button(window, text="BF",fg="white",width=1,bg="#333333", command=browse_file1)
browse_button.pack(pady=10)
browse_button.place(x=540, y=220)

window.resizable(False, False)
window.mainloop()

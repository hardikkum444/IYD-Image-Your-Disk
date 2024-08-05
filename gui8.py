from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label, messagebox, Checkbutton, simpledialog
import subprocess
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets8/frame0")

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
center_window(window)
window.wm_iconname("Image your disk")
window.title("IYD Decrypting Image")
im = Image.open('assets0/favicon.ico')
photo = ImageTk.PhotoImage(im)
window.wm_iconphoto(True, photo)
window.wm_iconname("IYD")
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
    274.0,
    500.0,
    fill="#212121",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=307.0,
    y=40.0,
    width=259.3500061035156,
    height=72.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    135.0,
    227.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    135.0,
    396.0,
    image=image_image_2
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=283.0,
    y=179.0,
    width=310.0229797363281,
    height=213.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    434.0,
    346.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_1.place(
    x=334.0,
    y=329.0,
    width=200.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    434.0,
    242.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,

)
entry_2.place(
    x=334.0,
    y=225.0,
    width=200.0,
    height=32.0
)

entry_2.place(
    x=334.0,
    y=225.0,
    width=200.0,
    height=32.0
)

entry_3 = Entry(
    bd=0,
    bg="#9F9F9F",
    # fg="#000716",
    highlightthickness=0,
    font=("Helvetica", 9)

)

# entry_3.place(
#     x=314.0,
#     y=270.0,
#     width=200.0,
#     height=32.0
# )

# entry_3.insert(-1, "*No Passphrase -> Leave Empty")

def on_next_click1():
    print()
    key = entry_1.get()
    loc = entry_2.get()
    directory = loc.rsplit('/', 1)[0]
    final = directory+'/decrypted_image'
    print(final)

    command = [
        'gpg',
        '--batch',
        '--yes',
        '--passphrase', key,
        '-o', final,
        '-d', loc
    ]


    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)

        print("Output:", result.stdout)
        print("Error:", result.stderr)
        finish()

    except subprocess.CalledProcessError as e:
        print("An error occurred while running the command.")
        print("Return code:", e.returncode)
        print("Output:", e.output)
        print("Error:", e.stderr)


def on_back_click():
    window.destroy()
    import sys
    # subprocess.run(["python3", "gui2.py"])
    subprocess.run(["sudo", "myenv/bin/python3", "gui2.py"])

def finish():
    window.destroy()

gen_button = Button(window, text="Decrypt", command=on_next_click1, width=10, bg="#333333", fg="white")
gen_button.place(x=457, y=431)

back_button = Button(window, text="Back", command=on_back_click, width=10, bg="#333333", fg="white")
back_button.place(x=310, y=431)

def browse_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_2.insert(0, file_path)

browse_button = Button(window, text="BF",fg="white",width=1,bg="#333333", command=browse_file1)
browse_button.pack(pady=10)
browse_button.place(x=554, y=227)

window.resizable(False, False)
window.mainloop()

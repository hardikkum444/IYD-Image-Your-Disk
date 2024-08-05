from pathlib import Path
from tkinter import *
import json
from tkinter import messagebox
import genrep
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets6/frame0")


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
window.title("IYD Imaging Process")
im = Image.open('assets0/favicon.ico')
photo = ImageTk.PhotoImage(im)
window.wm_iconphoto(True, photo)
window.wm_iconname("IYD")
window.geometry("600x500")
window.configure(bg = "#545252")

with open("results.json","r") as file:
    results = json.load(file)

    image_start = results['image_start']
    image_end = results['image_end']
    image_md5 = results['image_md5']
    image_sha1 = results['image_sha1']
    volume_loc = results['volume_loc']
    image_loc = results['image_loc']
    saving_loc = results['saving_loc']
    drive_md5 = results['drive_md5']
    drive_sha1 = results['drive_sha1']

print(image_start, image_end, image_md5, image_sha1, drive_md5, drive_sha1, volume_loc, image_loc, saving_loc)

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
    395.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    130.0,
    238.0,
    image=image_image_2
)

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
    x=285.0,
    y=0.0,
    width=301.0,
    height=500.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    434.0,
    131.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=315.0,
    y=114.0,
    width=238.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    434.0,
    205.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=315.0,
    y=188.0,
    width=238.0,
    height=33.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    434.0,
    279.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=315.0,
    y=262.0,
    width=238.0,
    height=33.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    434.0,
    356.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=315.0,
    y=339.0,
    width=238.0,
    height=32.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    434.0,
    431.5,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=315.0,
    y=414.0,
    width=238.0,
    height=33.0
)

def on_next_click():
    print("Next clicked")

def exit_win():
    window.destroy()


def generate():

    html_file_path = saving_loc + "/disk_imaging_report.html"
    print(html_file_path)
    physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes, partition_table = genrep.get_info(volume_loc)
    print(image_start, image_end, image_md5, image_sha1, drive_md5, drive_sha1, volume_loc, image_loc, saving_loc)
    extension = image_loc.split('.')[-1]
    case_no = entry_1.get() or "NA"
    evd_no = entry_2.get() or "NA"
    desc = entry_3.get() or "NA"
    examiner = entry_4.get() or "NA"
    notes = entry_5.get() or "NA"

    if(image_md5==drive_md5 and image_sha1==drive_sha1):
        verf = "Verified"
    else:
        verf = "Not verified"

    print(verf)

    genrep.generate_html_report(html_file_path,image_loc,image_start, image_end,extension, case_no, evd_no, desc, examiner, notes, physical_block_size, logical_block_size, total_sectors,"-", partition_information, model, serial_number,partition_table,total_used_bytes,total_sectors, drive_md5, drive_sha1,"NA","NA",image_start, verf,image_md5,image_sha1)

    finish()


next_button = Button(window, text="Next", command=generate, width=10, bg="#333333", fg="white")
next_button.place(x=461, y=462)

back_button = Button(window, text="Exit", command=exit_win, width=10, bg="#333333", fg="white")
back_button.place(x=297, y=462)

def finish():
    messagebox.showinfo("Imaging process completed successfully please check "+image_loc)
    window.destroy()

window.resizable(False, False)
window.mainloop()

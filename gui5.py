from pathlib import Path
import subprocess, os

from jinja2.nodes import Output
import genrep
import webbrowser
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/man44/Documents/imager/landing/assets5/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def center_window(window,height=600,width=500):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


window = Tk()

window.geometry("600x500")
window.configure(bg = "#545252")
window.title("IYD")
center_window(window)
window.geometry("600x500")


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
    fill="#545252",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=291.0,
    y=171.0,
    width=289.0,
    height=216.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    271.0,
    500.0,
    fill="#212121",
    outline="")

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    # command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=300.0,
    y=31.0,
    width=259.3500061035156,
    height=72.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    135.0,
    218.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    120.0,
    397.0,
    image=image_image_2
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    427.0,
    331.0,
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
    y=314.0,
    width=200.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    427.0,
    235.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=327.0,
    y=218.0,
    width=200.0,
    height=32.0
)



def browse_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        # entry_1.delete(0, Tk.END)  # Clear any existing text
        entry_2.insert(0, file_path)  # Insert the selected file path

def browse_file3():
    file_path = filedialog.askdirectory()
    if file_path:
        # entry_1.delete(0, Tk.END)  # Clear any existing text
        entry_1.insert(0, file_path)  # Insert the selected file path



def on_gen_click():
    vol_loc = entry_2.get()
    save_loc = entry_1.get()
    physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes, partition_table = genrep.get_info(vol_loc)
    print("Generating hash")
    drive_md5, drive_sha1 = genrep.calculate_hash(vol_loc)
    html_file_path = save_loc + "/disk_imaging_report.html"
    genrep.generate_html_report(html_file_path,"NA","NA", "NA","NA", "NA", "NA", "NA", "NA", "NA", physical_block_size, logical_block_size, total_sectors,"", partition_information, model, serial_number,partition_table,total_used_bytes,total_sectors, drive_md5, drive_sha1,"NA","NA","","","NA","NA")
    # try:
    #     webbrowser.open(save_loc+"/disk_imaging_report.html")
    # except Exception as e:
    #     print(f"Error opening HTML file: {e}")

    fire_command = 'sudo -u $USER firefox '+html_file_path
    os.system(fire_command)
    window.destroy()

def on_back_click():
    window.destroy()
    import sys
    # sys.path.append("build")
    # import gui2
    subprocess.run(["python3", "gui2.py"])


browse_button = Button(window, text="BF",fg="white",width=1,bg="#333333", command=browse_file1)
browse_button.pack(pady=10)
browse_button.place(x=539, y=219)

browse_button2 = Button(window, text="BF",fg="white",width=1,bg="#333333", command=browse_file3)
browse_button2.pack(pady=10)
browse_button2.place(x=539, y=316)


gen_button = Button(window, text="Generate Report", command=on_gen_click, width=13, bg="#333333", fg="white")
gen_button.place(x=435, y=431)

back_button = Button(window, text="Back", command=on_back_click, width=10, bg="#333333", fg="white")
back_button.place(x=295, y=431)



window.resizable(False, False)
window.mainloop()

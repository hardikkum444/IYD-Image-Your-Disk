from pathlib import Path
from queue import Queue
import threading
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, Label, messagebox, Checkbutton, simpledialog
import subprocess
import createim
import tkinter as tk
from tkinter import ttk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/man44/Documents/imager/landing/assets4/frame0")

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
window.title("IYD Imaging Process")
center_window(window)
window.geometry("600x500")
window.configure(bg = "#545252")

result_queue1 = Queue()
result_queue2 = Queue()

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
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
button_1.place(
    x=271.0,
    y=43.0,
    width=329.0,
    height=319.0
)

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
    128.0,
    249.0,
    image=image_image_1
)

canvas.create_rectangle(
    302.0,
    83.0,
    528.0,
    118.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    302.0,
    268.0,
    529.0,
    303.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    302.0,
    173.0,
    528.0,
    208.0,
    fill="#D9D9D9",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    428.0,
    100.0,
    image=entry_image_1
)

def browse_file1():
    file_path = filedialog.askopenfilename()
    if file_path:
        # entry_1.delete(0, Tk.END)
        entry_1.insert(0, file_path)

def browse_file3():
    file_path = filedialog.askdirectory()
    if file_path:
        # entry_1.delete(0, Tk.END)
        entry_3.insert(0, file_path)



browse_button = Button(window, text="BF",fg="white",width=2,bg="#333333", command=browse_file1)
browse_button.pack(pady=10)
browse_button.place(x=546, y=85)



browse_button2 = Button(window, text="BF",fg="white",width=2,bg="#333333", command=browse_file3)
browse_button2.pack(pady=10)
browse_button2.place(x=546, y=269)




entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=328.0,
    y=83.0,
    width=200.0,
    height=32.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    428.0,
    190.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=328.0,
    y=173.0,
    width=200.0,
    height=32.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    427.0,
    284.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=328.0,
    y=268.0,
    width=198.0,
    height=31.0
)

selected_format = StringVar()
# global comp = False
# global encr = False
# passkey = ""
encr = False
passkey = ""
comp = False  # Initialize comp as False

def on_checkbox_click1():
    global encr, passkey
    if encr_var.get() == 1:
        result = simpledialog.askstring("Encrypt using GPG", "Set Passphrase:", show='*')
        if result is None or result.strip() == "":
            messagebox.showwarning("Warning", "Please enter valid passphrase!")
            encr_var.set(0)
        else:
            encr = True
            passkey = result

    else:
        print("Encryption not applied")


def on_checkbox_click2():
    global comp
    if comp_var.get() == 1:
        comp = True
        messagebox.showwarning("Warning", "Compression may cause data hindernace!")
        print("compression applied")
    else:
        print("compression not applied")


encr_var = IntVar()
comp_var = IntVar()

checkbutton_encr = Checkbutton(
    window,
    text="Encrypt (GPG)",
    variable=encr_var,
    onvalue=1,
    offvalue=0,
    width=12,
    command=on_checkbox_click1,
    bg="#545252",
    font=("Arial", 12),
    relief="raised",
    padx=10,
    pady=5,

)
checkbutton_encr.place(x=439, y=375)


checkbutton_comp = Checkbutton(
    window,
    text="Compress (gzip)",
    variable=comp_var,
    onvalue=1,
    width=12,
    offvalue=0,
    command=on_checkbox_click2,
    bg="#545252",
    font=("Arial", 12),
    relief="raised",
    padx=10,
    pady=5,
)
checkbutton_comp.place(x=276, y=375)

def main_win():

    global encr
    global passkey
    global comp

    task1_completed = threading.Event()
    task2_completed = threading.Event()

    def update_progress_label(text):
        progress_label.config(text=text)

    def update_progress_bar():
        progress_bar_1.start(20)

    def stop_progress_bar():
        progress_bar_1.stop()

    def create_image_task():
        window.after(0, update_progress_bar)
        final_name = entry_3.get()+"/"+entry_2.get()
        image_start, image_end = createim.create_image(entry_1.get(), final_name)
        window.after(0, lambda: update_progress_label("image created..."))
        window.after(0, lambda: update_progress_label("Computing Image..."))
        image_md5, image_sha1 = createim.image_hash(entry_3.get()+"/"+entry_2.get())
        is_comp = False
        if comp:
            window.after(0, lambda: update_progress_label("Compressing please wait..."))
            createim.compress_disk_image3(entry_3.get() + "/" + entry_2.get())
            window.after(0, lambda: update_progress_label("Compression completed..."))
            is_comp = True

        if encr:
            window.after(0, lambda: update_progress_label("Encrypting please wait..."))
            if is_comp:
                final_name = entry_3.get() + "/" + entry_2.get()+".gz"
                print(final_name)
            else:
                final_name = entry_3.get() + "/" + entry_2.get()
                print(final_name)
            output_file_name = final_name + "GPG"
            print(output_file_name)
            print("passkey"+passkey)
            createim.encrypt_with_gpg(final_name, output_file_name , passkey)
            window.after(0, lambda: update_progress_label("encryption completed..."))

        # return image_start, image_end, image_md5, image_sha1
        result_queue1.put((image_start, image_end, image_md5, image_sha1, entry_3.get()))
        task1_completed.set()

    def gen_hash():
        window.after(0, update_progress_bar)
        print("Generating hash")
        drive_md5, drive_sha1 = createim.compute_drive_hash(entry_1.get())
        window.after(0, lambda: update_progress_label("hashes generated..."))
        # return drive_md5, drive_sha1
        result_queue2.put((drive_md5, drive_sha1))
        task2_completed.set()

    def check_tasks():
        if task1_completed.is_set() and task2_completed.is_set():
            stop_progress_bar()
            progress_label.config(text="Tasks completed. Close the window.")
            on_next_click2()
            window.destroy()

        else:
            window.after(100, check_tasks)

    # def get_1(image_start, image_end, image_md5, image_sha1):
    #     return image_start, image_end, image_md5, image_sha1

    # def get_2(drive_md5, drive_sha1):
    #     return drive_md5, drive_sha1

    window = tk.Tk()
    window.title("IYD-Creating Image")
    center_window(window)
    window.geometry("300x150")

    style = ttk.Style()
    style.configure("TProgressbar", thickness=20)

    progress_label = Label(window, text="Progressing...", font=("Arial", 12))
    progress_label.pack(pady=10)

    progress_bar_1 = ttk.Progressbar(window, style="TProgressbar", orient="horizontal", length=250, mode="indeterminate")
    progress_bar_1.pack(pady=20)

    t1 = threading.Thread(target=create_image_task)
    t2 = threading.Thread(target=gen_hash)

    t1.start()
    t2.start()

    window.after(100, check_tasks)

    window.mainloop()

def on_next_click1():

    if len(entry_1.get()) == 0 or len(entry_2.get()) == 0 or len(entry_3.get()) == 0:
        messagebox.showwarning("Warning", "Please enter all the fields!")

    else:
        main_win()



def on_next_click2():
    import sys
    image_start, image_end, image_md5, image_sha1 = result_queue1.get()
    drive_md5, drive_sha1 = result_queue2.get()
    print(image_start, image_end, image_md5, image_sha1, drive_md5, drive_sha1)
    window.destroy()
    import gui6


def on_back_click():
    window.destroy()
    import sys
    subprocess.run(["python3", "gui3.py"])



done = 00
next_button = Button(window, text="Next", command=on_next_click1, width=10, bg="#333333", fg="white")
next_button.place(x=452, y=455)

back_button = Button(window, text="Back", command=on_back_click, width=10, bg="#333333", fg="white")
back_button.place(x=312, y=455)

window.resizable(False, False)
window.mainloop()

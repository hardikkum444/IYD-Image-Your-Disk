import pytsk3
import os
import sys
from tqdm import tqdm
import hashlib
import subprocess
import datetime
from jinja2 import Template
import re
import getpass
import tkinter as tk
from tkinter import ttk

def create_image(volume_loc, output_file, block_size=1024):

    print("Computing drive hashes for Verification")
    print("This Process may take a while")
    drive_md5 = hashlib.md5()
    drive_sha1 = hashlib.sha1()
    with open(volume_loc,"rb") as f:
        for part in iter(lambda: f.read(1024), b""):
            drive_md5.update(part)
            drive_sha1.update(part)
    print("Drive md5 hash (Computed Just Before Imaging): "+drive_md5.hexdigest())
    print("Drive sha1 hash (Computed Just Before Imaging): "+drive_sha1.hexdigest())


    start_time = datetime.datetime.now()
    print("Disk imaging started at: ", start_time)

    try:
        with open(volume_loc, 'rb') as src, open(output_file, 'wb') as dest:
            total_size = os.path.getsize(volume_loc)
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Processing") as pbar:
                while True:
                    block = src.read(block_size)
                    if not block:
                        break
                    dest.write(block)
                    pbar.update(len(block))

    finally:
        # output_file.close()
        print("Disk image created")

    end_time = datetime.datetime.now()
    print("Disk imaging ended at: ",end_time)

    return start_time, end_time, drive_md5.hexdigest(), drive_sha1.hexdigest()

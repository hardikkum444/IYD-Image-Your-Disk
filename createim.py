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
import gzip

def create_image(volume_loc, output_file, block_size=1024):

    print("Generating Image of selected disk")
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

    return start_time, end_time

def compute_drive_hash(volume_loc):
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

    return drive_md5.hexdigest(), drive_sha1.hexdigest()


def compress_disk_image3(dd_file):
    print("Compressing, please wait")

    compressed_file = dd_file + ".gz"
    try:
        with open(dd_file, 'rb') as f_in, gzip.open(compressed_file, 'wb') as f_out:
            while True:
                chunk = f_in.read(1024)
                if not chunk:
                    break
                f_out.write(chunk)
    except Exception as e:
        print("An error occurred during compression:", e)
        return

    try:
        os.remove(dd_file)
        print("Disk image compressed")
    except Exception as e:
        print("An error occurred while removing the original file:", e)



# def encrypt_with_gpg(input_file, output_file, key):

#     encrypt_command = [
#         "gpg",
#         "--output", output_file,
#         "--symmetric",
#         "--cipher-algo", "AES256",
#         "--no-symkey-cache",
#         "--passphrase", key,
#         input_file
#     ]

#     subprocess.run(encrypt_command)


def encrypt_with_gpg(input_file, output_file, key):

    encrypt_command = [
        "gpg",
        "--passphrase", "'"+key+"'",
        "--batch",
        "--yes",
        "-c",
        "-o", output_file,
        input_file
    ]

    subprocess.run(encrypt_command)

# gpg --passphrase 'your_passphrase_here' --batch --yes -c -o output input
# gpg --batch --yes --passphrase '1234' -o done -d mandom

def image_hash(image_loc):

    md5_command = [
        "md5sum", image_loc
    ]

    sha1_command = [
        "sha1sum", image_loc
    ]

    md5_output = subprocess.check_output(md5_command).decode('utf-8').split()[0]
    sha1_output = subprocess.check_output(sha1_command).decode('utf-8').split()[0]

    return md5_output, sha1_output

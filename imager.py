
import pytsk3
import os
import gzip
import itertools
import threading
import time
import sys
from tqdm import tqdm
import hashlib
import subprocess


def create_image(volume_loc, output_file, block_size=4096):
    img_info = pytsk3.Img_Info(volume_loc)
    print(img_info)

    target_file = open(output_file,'wb')
    offset = 0

    try:
        with tqdm(total=img_info.get_size(), unit='B', unit_scale=True, desc="Processing") as pbar:
            while(offset < img_info.get_size()):
                data_available = min(block_size, img_info.get_size() - offset)
                data = img_info.read(offset, data_available)
                target_file.write(data)
                offset += len(data)
                pbar.update(len(data))

    finally:
        target_file.close()
        print("Disk image created")


def compress_disk_image(dd_file):
    print("Compressing please wait")

    compressed_file = dd_file + ".gz"
    with open(dd_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            f_out.writelines(f_in)

    os.remove(dd_file)
    print("Disk image compressed")


def loading():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')


def encrypt_with_gpg(input_file, output_file):

    encrypt_command = [
        "gpg",
        "--output", output_file,
        "--symmetric",
        "--cipher-algo", "AES256",
        input_file
    ]

    subprocess.run(encrypt_command)

# def decrypt_with_gpg(input_file, output_file):
#     passphrase = "your_passphrase"
#
#     decrypt_command = [
#         "gpg",
#         "--output", output_file,
#         "--decrypt",
#         input_file
#     ]
#
#     subprocess.run(decrypt_command)
#
# def decrypt_with_gpg(input_file, output_file):
#     passphrase = input("Enter decryption passphrase: ")

def decrypt_with_gpg(input_file, output_file):
    passphrase = input("Enter decryption passphrase: ")

    decrypt_command = [
        "gpg",
        "--output", output_file,
        "--decrypt",
        "--batch",
        "--passphrase", passphrase,
        input_file
    ]

    try:
        subprocess.run(decrypt_command, check=True)
        print(f"Decryption successful. Decrypted file saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print("Error: Failed to decrypt")
        exit(0)


def calculate_hash(filename, dir_name):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(filename,"rb") as f:
        for part in iter(lambda: f.read(4096), b""):
            md5.update(part)
            sha1.update(part)
    print(md5.hexdigest())
    print(sha1.hexdigest())

    with open(dir_name+'/data.txt', 'w') as f:
        data = f"Image-your-disk -- Disk Imaging tool but in Python!\nAuto-Generated Report:\n-------------------------------------------------------------------------------\n\nCalculated md5 hash: {md5.hexdigest()}\nCalculated SHA1 hash: {sha1.hexdigest()}\n"
        f.write(data)


    ch = input("Would you like to add case information? (y/n) ")

    if(ch.lower() == "y"):
        case_no = input("Case Number: ")
        evd_no = input("Evidence Number: ")
        unq_desc = input("Unique Description: ")
        examiner = input("Examiner: ")
        notes = input("Notes: ")
        with open(dir_name+'/data.txt', 'a') as f:
            data = f"\nCase Number: {case_no}\nEvidence Number: {evd_no}\nUnique Description: {unq_desc}\nExaminer: {examiner}\nNotes: {notes}\n"
            f.write(data)


if __name__ == "__main__":

    ch0 = input("Would you like to decrypt encrypted RAW file? (y/n) ")

    if (ch0.lower() == "y"):
        e_file_name = input("Enter encrypted file name (ex: dir/encrypted_file.gpg) ")
        d_file_name = input("What would you like decrypted file to be saved as? ")

        if ".raw.gz" in d_file_name:
            decrypt_with_gpg(e_file_name, d_file_name)
        else:
            decrypt_with_gpg(e_file_name, d_file_name+".raw.gz")

        print("De-compressing ...")
        decomp = f"gzip -d {d_file_name}.raw.gz"
        try:
            subprocess.run(decomp, shell=True, check=True)
            print("successfully decompressed")
        except subprocess.CalledProcessError as e:
            print("decompression issue please check if gzip is installed")


    chn = input("Would you like to mount RAW file to view contents? (y/n) ")

    if(chn.lower() == "y"):

        offset = input("Enter offset ")
        image_file = input("Enter location of image file (ex: /dir/image.raw) ")
        mount_point = "/mnt"

        ro = input("Would you like to mount as read only? (y/n) ")
        if(ro.lower() == "y"):
            mount_command = f"sudo mount -o loop,offset={offset} {image_file} {mount_point}"
        if(ro.lower() == "n"):
            mount_command = f"sudo mount -o loop,offset={offset},ro {image_file} {mount_point}"

        try:
            subprocess.run(mount_command, shell=True, check=True)
            print("Mounted successfully, please check at /mnt")
        except subprocess.CalledProcessError as e:
            print("Error: Failed to mount")

    IYD = input("Would you like to create a fresh image? (y/n)")
    if(IYD.lower() == "y"):
        print("Welcome to the Imaging process")

        volume_loc = input("Enter location of drive (/dev/sdx): ")
        name = input("What name would you like the image to be saved under? ")
        file_name = input("Enter directory name to store in ")
        if not os.path.exists(file_name):
            os.makedirs(file_name, mode=0o755)
            os.chmod(file_name, 0o777)
        output_file = file_name+"/"+name+".raw"
        create_image(volume_loc, output_file)
        calculate_hash(output_file,file_name)
        compress_disk_image(output_file)

        ch2 = input("Would you like encryption through GPG? (y/n) ")

        if(ch2.lower() == "y"):
            print("WARNING! Encryption may cause data integrity hinderance")
            encrypt_with_gpg(output_file+".gz", file_name+"/encrypted_image.gpg")
            ch3 = input("Would you like the not-encrypted file to be deleted? (y/n) ")
            if(ch3.lower() == "y"):
                os.remove(output_file+".gz")
            print("Encryption successful")

    else:
        print("Thank you for using IYD!")

#sudo mount -o loop,offset=491520 disk_image.raw /mnt

import pytsk3
import os
import gzip
import itertools
import threading
import time
import sys
from tqdm import tqdm
import hashlib

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
        data = f"Image-your-disk -- Disk Imaging tool but in Python!\nAuto-Generated Report:\n-------------------------------------------------------------------------------\n\nCalculated md5 hash: {md5.hexdigest()}\nCalculated SHA1 hash: {sha1.hexdigest()}"
        f.write(data)


    ch = input("Would you like to add case information (y/n)")

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
    volume_loc = input("Enter location: ")
    file_name = input("Enter file name to store in ")
    if not os.path.exists(file_name):
        os.makedirs(file_name, mode=0o755)
        os.chmod(file_name, 0o777)
    output_file = file_name+"/disk_image.raw"
    create_image(volume_loc, output_file)
    calculate_hash(output_file,file_name)
    compress_disk_image(output_file)

    #sudo mount -o loop,offset=491520 disk_image.raw /mnt

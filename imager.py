import pytsk3
import os
import gzip
import itertools
import threading
import time
import sys
from tqdm import tqdm

def create_image(volume_loc, output_file, block_size=4096):
    img_info = pytsk3.Img_Info(volume_loc)
    # print(img_info)

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


# def compress_disk_image(di_file):
#     compressed_file = di_file+".gz"
#     with open(di_file,'rb') as f_in:
#         with gzip.open(compressed_file,'wb') as f_out:
#             file_size = os.path.getsize(di_file)
#             with tqdm(total=file_size, unit='B', unit_scale=True, desc="Compressing") as pbar:
#                 while True:
#                     data = f_in.read(4096)
#                     if not data:
#                         break
#                         f_out.write(data)
#                         pbar.update(len(data))
#     os.remove(di_file)
#     print("Disk image compressed")


def compress_disk_image(dd_file):
    print("Compressing please wait")
    while(True):

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


# if __name__== "__main__":
#     volume_loc = input("Enter location ")
#     output_file = "disk_image.dd"
#
#
#     spinner_thread = threading.Thread(target=loading)
#     spinner_thread.start()
#
#     try:
#
#         create_image(volume_loc,output_file)
#         spinner_thread.join()
#         print("\nDisk imaging completed!")
#         compress_disk_image(output_file)
#         print("Compression completed!")
#
#     except Exception as e:
#         print(f"Error: {e}")


# def create_image(volume_loc, output_file, block_size=4096):
#     img_info = pytsk3.Img_Info(volume_loc)
#     print(img_info)
#
#     target_file = open(output_file, 'wb')
#     offset = 0
#
#     try:
#         with tqdm(total=img_info.get_size(), unit='B', unit_scale=True) as pbar:
#             while offset < img_info.get_size():
#                 data_available = min(block_size, img_info.get_size() - offset)
#                 data = img_info.read(offset, data_available)
#                 target_file.write(data)
#                 offset += len(data)
#                 pbar.update(len(data))
#     finally:
#         target_file.close()

if __name__ == "__main__":
    volume_loc = input("Enter location: ")
    output_file = "disk_image.raw"
    create_image(volume_loc, output_file)
    # compress_disk_image(output_file)

    spinner_thread = threading.Thread(target=loading)
    spinner_thread.start()

    try:
        compress_disk_image(output_file)
        spinner_thread.join()
        print("Compression completed!")

    except Exception as e:
        print(f"Error: {e}")

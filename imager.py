# import pytsk3
# import os
# import gzip
# import itertools
# import threading
# import time
# import sys
# from tqdm import tqdm
# import hashlib
# import subprocess
# import datetime
# from jinja2 import Template
#
#
# def create_image(volume_loc, output_file, block_size=4096):
#     img_info = pytsk3.Img_Info(volume_loc)
#     print(img_info)
#
#     target_file = open(output_file,'wb')
#     offset = 0
#
#     start_time = datetime.datetime.now()
#     print("Disk imaging started at: ",start_time)
#
#     try:
#         with tqdm(total=img_info.get_size(), unit='B', unit_scale=True, desc="Processing") as pbar:
#             while(offset < img_info.get_size()):
#                 data_available = min(block_size, img_info.get_size() - offset)
#                 data = img_info.read(offset, data_available)
#                 target_file.write(data)
#                 offset += len(data)
#                 pbar.update(len(data))
#
#     finally:
#         target_file.close()
#         print("Disk image created")
#
#     end_time = datetime.datetime.now()
#     print("Disk imaging ended at: ",end_time)
#
#     with open("IYD-results"+'/data.txt', 'w') as f:
#         data = f"Image-your-disk\nAuto-Generated Report:\n-------------------------------------------------------------------------------\n\nImage name: {output_file}\nImaging start time: {start_time}\n Imaging end time: {end_time}\n\n"
#         f.write(data)
#
#     return start_time, end_time
#
#
#
# def compress_disk_image(dd_file):
#     print("Compressing please wait")
#
#     compressed_file = dd_file + ".gz"
#     with open(dd_file, 'rb') as f_in:
#         with gzip.open(compressed_file, 'wb') as f_out:
#             f_out.writelines(f_in)
#
#     os.remove(dd_file)
#     print("Disk image compressed")
#
#
# def loading():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     ')
#
#
# def encrypt_with_gpg(input_file, output_file):
#
#     encrypt_command = [
#         "gpg",
#         "--output", output_file,
#         "--symmetric",
#         "--cipher-algo", "AES256",
#         "--no-symkey-cache",
#         input_file
#     ]
#
#     subprocess.run(encrypt_command)
#
#
# def decrypt_with_gpg(input_file, output_file):
#     passphrase = input("Enter decryption passphrase: ")
#
#     decrypt_command = [
#         "gpg",
#         "--output", output_file,
#         "--decrypt",
#         "--batch",
#         "--passphrase", passphrase,
#         input_file
#     ]
#
#     try:
#         subprocess.run(decrypt_command, check=True)
#         print(f"Decryption successful. Decrypted file saved as {output_file}")
#     except subprocess.CalledProcessError as e:
#         print("Error: Failed to decrypt")
#         exit(0)
#
#
# def calculate_hash(filename, dir_name):
#     md5 = hashlib.md5()
#     sha1 = hashlib.sha1()
#     with open(filename,"rb") as f:
#         for part in iter(lambda: f.read(4096), b""):
#             md5.update(part)
#             sha1.update(part)
#     print(md5.hexdigest())
#     print(sha1.hexdigest())
#
#
#
#     ch = input("Would you like to add case information? (y/n) ")
#
#     if(ch.lower() == "y"):
#         case_no = input("Case Number: ")
#         evd_no = input("Evidence Number: ")
#         unq_desc = input("Unique Description: ")
#         examiner = input("Examiner: ")
#         notes = input("Notes: ")
#         with open(dir_name+'/data.txt', 'a') as f:
#             data = f"\nCase Number: {case_no}\nEvidence Number: {evd_no}\nUnique Description: {unq_desc}\nExaminer: {examiner}\nNotes: {notes}\n"
#             f.write(data)
#
#     return md5.hexdigest(),sha1.hexdigest(),case_no,evd_no,unq_desc,examiner,notes
#
#
#
# def generate_html_report(image_name, start_time, end_time, md5_hash, sha1_hash, case_no, evd_no, desc, examiner, notes):
#     with open('report_template.html') as file:
#         template = Template(file.read())
#
#     rendered_report = template.render(image_name=image_name, start_time=start_time, end_time=end_time, md5_hash=md5_hash, sha1_hash=sha1_hash, case_no=case_no, evd_no=evd_no, desc=desc, examiner=examiner, notes=notes)
#
#     with open('disk_imaging_report.html', 'w') as output_file:
#         output_file.write(rendered_report)
#
# # generate_html_report("10:46", "10:50", "09skdjid09020930", "lkahsdljhajflh82873jknsdn", ["Additional info 1", "Additional info 2"])
#
#
# if __name__ == "__main__":
#
#     ch0 = input("Would you like to decrypt encrypted RAW file? (y/n) ")
#
#     if (ch0.lower() == "y"):
#         e_file_name = input("Enter encrypted file name (ex: dir/encrypted_file.gpg) ")
#         d_file_name = input("What would you like decrypted file to be saved as? ")
#
#         if ".raw.gz" in d_file_name:
#             decrypt_with_gpg(e_file_name, d_file_name)
#         else:
#             decrypt_with_gpg(e_file_name, d_file_name+".raw.gz")
#
#         print("De-compressing ...")
#         decomp = f"gzip -d {d_file_name}.raw.gz"
#         try:
#             subprocess.run(decomp, shell=True, check=True)
#             print("successfully decompressed")
#         except subprocess.CalledProcessError as e:
#             print("decompression issue please check if gzip is installed")
#
#
#     chn = input("Would you like to mount RAW file to view contents? (y/n) ")
#
#     if(chn.lower() == "y"):
#
#         offset = input("Enter offset ")
#         image_file = input("Enter location of image file (ex: /dir/image.raw) ")
#         mount_point = "/mnt"
#
#         ro = input("Would you like to mount as read only? (y/n) ")
#         if(ro.lower() == "y"):
#             mount_command = f"sudo mount -o loop,offset={offset} {image_file} {mount_point}"
#         if(ro.lower() == "n"):
#             mount_command = f"sudo mount -o loop,offset={offset},ro {image_file} {mount_point}"
#
#         try:
#             subprocess.run(mount_command, shell=True, check=True)
#             print("Mounted successfully, please check at /mnt")
#         except subprocess.CalledProcessError as e:
#             print("Error: Failed to mount")
#
#     IYD = input("Would you like to create a fresh image? (y/n)")
#     if(IYD.lower() == "y"):
#         print("Welcome to the Imaging process")
#
#         volume_loc = input("Enter location of drive (/dev/sdx): ")
#         name = input("What name would you like the image to be saved under? ")
#         file_name = "IYD-results"
#         if not os.path.exists(file_name):
#             os.makedirs(file_name, mode=0o755)
#             os.chmod(file_name, 0o777)
#         output_file = file_name+"/"+name+".raw"
#         start_time, end_time = create_image(volume_loc, output_file)
#         md5,sha1,det_casno,det_evdno,det_desc,det_examiner,det_notes = calculate_hash(output_file,file_name)
#         compress_disk_image(output_file)
#
#         print("Generating HTML report")
#         generate_html_report(name+".raw",start_time, end_time, md5, sha1, det_casno, det_evdno, det_desc, det_examiner, det_notes)
#
#
#         ch2 = input("Would you like encryption through GPG? (y/n) ")
#
#         if(ch2.lower() == "y"):
#             print("WARNING! Encryption may cause data integrity hinderance")
#             encrypt_with_gpg(output_file+".gz", file_name+"/encrypted_image.gpg")
#             ch3 = input("Would you like the not-encrypted file to be deleted? (y/n) ")
#             if(ch3.lower() == "y"):
#                 os.remove(output_file+".gz")
#             print("Encryption successful")
#
#     else:
#         print("Thank you for using IYD!")
#
# #sudo mount -o loop,offset=491520 disk_image.raw /mnt






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
import datetime
from jinja2 import Template
import re
import getpass

# def create_image(volume_loc, output_file, block_size=1024):
#     img_info = pytsk3.Img_Info(volume_loc)
#     print(img_info)
#
#     target_file = open(output_file,'wb')
#     offset = 0
#
#     start_time = datetime.datetime.now()
#     print("Disk imaging started at: ",start_time)
#
#     try:
#         with tqdm(total=img_info.get_size(), unit='B', unit_scale=True, desc="Processing") as pbar:
#             while(offset < img_info.get_size()):
#                 data_available = min(block_size, img_info.get_size() - offset)
#                 data = img_info.read(offset, data_available)
#                 target_file.write(data)
#                 offset += len(data)
#                 pbar.update(len(data))

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

    # with open("IYD-results"+'/data.txt', 'w') as f:
    #     data = f"Image-your-disk\nAuto-Generated Report:\n-------------------------------------------------------------------------------\n\nImage name: {output_file}\nImaging start time: {start_time}\n Imaging end time: {end_time}\n\n"
    #     f.write(data)



    return start_time, end_time, drive_md5.hexdigest(), drive_sha1.hexdigest()



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
        "--no-symkey-cache",
        input_file
    ]

    subprocess.run(encrypt_command)


def get_info(volume_loc):

    disk = volume_loc
    parted_command = ['sudo', 'parted', disk, 'print']
    grep_command = ['grep', 'Partition Table']
    awk_command = ['awk', '{print $3}']


    parted_output = subprocess.run(parted_command, capture_output=True, text=True, check=True).stdout
    grep_output = subprocess.run(grep_command, input=parted_output, capture_output=True, text=True, check=True).stdout
    partition_table = subprocess.run(awk_command, input=grep_output, capture_output=True, text=True, check=True).stdout.strip()
    print(partition_table)
    if(partition_table == "mbr" or partition_table =="msdos"):

        output = subprocess.run(['sudo', 'fdisk', '-l', disk], capture_output=True, text=True).stdout

        total_used_bytes = 0
        pattern = r'^/dev/(\S+)\s+\*?\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+\w?)\s+([a-zA-Z0-9]*)\s+(.*?)\s*$'


        partitions = []


        lines = output.splitlines()
        for line in lines:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                start = int(match.group(2))
                end = int(match.group(3))
                sectors = int(match.group(4))
                size = match.group(5)
                id = match.group(6)
                type = match.group(7)
                partitions.append({
                    'name': name,
                    'start': start,
                    'end': end,
                    'sectors': sectors,
                    'size': size,
                    'id': id,
                    'type': type
                })


        partition_information = []
        for part in partitions:
            partition_information.append(f'<b>Partition {part["name"]}:</b><br>')
            partition_information.append(f'<b>Start:</b> {part["start"]}<br>')
            partition_information.append(f'<b>End:</b> {part["end"]}<br>')
            partition_information.append(f'<b>Sectors:</b> {part["sectors"]}<br>')
            partition_information.append(f'<b>Size:</b> {part["size"]}<br>')
            partition_information.append(f'<b>ID:</b> {part["id"]}<br>')
            partition_information.append(f'<b>Type:</b> {part["type"]}<br>')
            partition_information.append('<br>')

            # nname = String(["name"])
            nname = part["name"]

            if not nname.startswith("/dev/"):
                nname = "/dev/"+nname
                print(nname)

            df_output = subprocess.run(['df', '-B1', nname], capture_output=True, text=True).stdout.strip()

            used_amount = df_output.splitlines()[1].split()[2]
            partition_information.append(f'<b>Memory Used (in bytes):</b><br>{used_amount}<br><br>')

            total_used_bytes += int(used_amount)

        partition_information = '\n'.join(partition_information)


    else:


        total_used_bytes=0
        # disk = '/dev/nvme0n1'
        output = subprocess.run(['sudo', 'fdisk', '-l', disk], capture_output=True, text=True).stdout


        pattern = r'^(/dev/.*?p\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+\w?)\s+(.*?)$'


        partitions = []


        lines = output.splitlines()
        for line in lines:
            match = re.match(pattern, line)
            if match:
                name = match.group(1)
                start = int(match.group(2))
                end = int(match.group(3))
                sectors = int(match.group(4))
                size = match.group(5)
                type = match.group(6)
                partitions.append({
                    'name': name,
                    'start': start,
                    'end': end,
                    'sectors': sectors,
                    'size': size,
                    'type': type
                })


        partition_information = []
        for part in partitions:
            partition_information.append(f'<b>Partition {part["name"]}:</b><br>')
            partition_information.append(f'<b>Start:</b> {part["start"]}<br>')
            partition_information.append(f'<b>End:</b> {part["end"]}<br>')
            partition_information.append(f'<b>Sectors:</b> {part["sectors"]}<br>')
            partition_information.append(f'<b>Size:</b> {part["size"]}<br>')
            partition_information.append(f'<b>Type:</b> {part["type"]}<br>')
            partition_information.append('<br>')

            nname = part["name"]

            if not nname.startswith("/dev/"):
                nname = "/dev/"+nname
                print(nname)

            df_output = subprocess.run(['df', '-B1', nname], capture_output=True, text=True).stdout.strip()
            used_amount = df_output.splitlines()[1].split()[2]
            partition_information.append(f'<b>Partition Size:</b><br>{used_amount}<br><br>')

            total_used_bytes += int(used_amount)

        partition_information = '\n'.join(partition_information)



    cmd_vendor_name = ['cat', f'/sys/block/{disk.split("/")[-1]}/device/vendor']
    vendor_name = subprocess.run(cmd_vendor_name, capture_output=True, text=True).stdout.strip()

    cmd_model = ['cat', f'/sys/block/{disk.split("/")[-1]}/device/model']
    model = subprocess.run(cmd_model, capture_output=True, text=True).stdout.strip()

    cmd_serial = ['lsblk', '-no', 'SERIAL', disk]
    serial_number = subprocess.run(cmd_serial, capture_output=True, text=True).stdout.strip()

    cmd_total_sectors = ['cat', f'/sys/class/block/{disk.split("/")[-1]}/size']
    total_sectors = subprocess.run(cmd_total_sectors, capture_output=True, text=True).stdout.strip()

    cmd_physical_block_size = ['cat', f'/sys/block/{disk.split("/")[-1]}/queue/physical_block_size']
    physical_block_size = subprocess.run(cmd_physical_block_size, capture_output=True, text=True).stdout.strip()

    cmd_logical_block_size = ['cat', f'/sys/block/{disk.split("/")[-1]}/queue/logical_block_size']
    logical_block_size = subprocess.run(cmd_logical_block_size, capture_output=True, text=True).stdout.strip()

    return physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes, partition_table



def decrypt_with_gpg(input_file, output_file):

    passphrase = getpass.getpass(prompt='Enter GPG passphrase: ')

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
    print("Image md5 hash: "+md5.hexdigest())
    print("Image sha1 hash: "+sha1.hexdigest())



    ch = input("Would you like to add case information? (y/n) ")

    if(ch.lower() == "y"):
        case_no = input("Case Number: ")
        evd_no = input("Evidence Number: ")
        unq_desc = input("Unique Description: ")
        examiner = input("Examiner: ")
        notes = input("Notes: ")
        # with open(dir_name+'/data.txt', 'a') as f:
        #     data = f"\nCase Number: {case_no}\nEvidence Number: {evd_no}\nUnique Description: {unq_desc}\nExaminer: {examiner}\nNotes: {notes}\n"
        #     f.write(data)

    return md5.hexdigest(),sha1.hexdigest(),case_no,evd_no,unq_desc,examiner,notes



def generate_html_report(image_name, start_time, end_time, image_type, case_no, evd_no, desc, examiner, notes, physical_block_size, logical_block_size, total_sectors, bytes_per_sector, partition_information, drive_model, drive_serial_number, partition_table, source_data_size, sector_count, drive_md5, drive_sha1, aq_started, aq_ended, ve_started, ve_ended, md5, sha1):
    with open('report_template.html') as file:
        template = Template(file.read())

    rendered_report = template.render(image_name=image_name, start_time=start_time, end_time=end_time, image_type=image_type, case_no=case_no, evd_no=evd_no, desc=desc, examiner=examiner, notes=notes, physical_block_size=physical_block_size, logical_block_size=logical_block_size, total_sectors=total_sectors, bytes_per_sector=bytes_per_sector, partition_information=partition_information, drive_model=drive_model, drive_serial_number=drive_serial_number, partition_table=partition_table, source_data_size=source_data_size, sector_count=sector_count, md5_hash=drive_md5, sha1_hash=drive_sha1, aq_started=aq_started, aq_ended=aq_ended, ve_started=ve_started, ve_ended=ve_ended, img_md5_hash=md5, img_sha1_hash=sha1)

    with open('disk_imaging_report.html', 'w') as output_file:
        output_file.write(rendered_report)

# generate_html_report("10:46", "10:50", "09skdjid09020930", "lkahsdljhajflh82873jknsdn", ["Additional info 1", "Additional info 2"])


if __name__ == "__main__":

    aq_start_time = datetime.datetime.now()
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

    IYD = input("Would you like to create a fresh image? (y/n) ")
    if(IYD.lower() == "y"):
        print("Welcome to the Imaging process")

        volume_loc = input("Enter location of drive (/dev/sdx): ")
        name = input("What name would you like the image to be saved under? ")
        file_name = "IYD-results"
        if not os.path.exists(file_name):
            os.makedirs(file_name, mode=0o755)
            os.chmod(file_name, 0o777)


        output_file = file_name+"/"+name+".raw"
        start_time, end_time, drive_md5, drive_sha1 = create_image(volume_loc, output_file)
        md5,sha1,det_casno,det_evdno,det_desc,det_examiner,det_notes = calculate_hash(output_file,file_name)
        compress_disk_image(output_file)


        physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes,partition_table = get_info(volume_loc)



        ch2 = input("Would you like encryption through GPG? (y/n) ")

        if(ch2.lower() == "y"):
            print("WARNING! Encryption may cause data integrity hinderance")
            encrypt_with_gpg(output_file+".gz", file_name+"/encrypted_image.gpg")
            ch3 = input("Would you like the not-encrypted file to be deleted? (y/n) ")
            if(ch3.lower() == "y"):
                os.remove(output_file+".gz")
            print("Encryption successful")

        aq_end_time = datetime.datetime.now()

        print("Generating HTML report")
        generate_html_report(name+".raw",start_time, end_time,"RAW", det_casno, det_evdno, det_desc, det_examiner, det_notes, physical_block_size, logical_block_size, total_sectors,"", partition_information, model, serial_number,partition_table,total_used_bytes,total_sectors, drive_md5, drive_sha1,aq_start_time,aq_end_time,"","",md5,sha1)

        print("Html Report Generated")

    else:
        print("Thank you for using IYD!")

#sudo mount -o loop,offset=491520 disk_image.raw /mnt

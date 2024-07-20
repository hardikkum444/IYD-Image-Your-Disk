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


def get_info(volume_loc):

    print("started")
    disk = volume_loc
    print("started")

    parted_command = ['sudo','parted', disk, 'print']
    grep_command = ['grep', 'Partition Table']
    awk_command = ['awk', '{print $3}']

    print("start command parted")
    parted_output = subprocess.run(parted_command, capture_output=True, text=True, check=True).stdout
    print("end command parted")
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
    print("done")

    return physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes, partition_table


def calculate_hash(filename):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(filename,"rb") as f:
        for part in iter(lambda: f.read(4096), b""):
            md5.update(part)
            sha1.update(part)
    print("Image md5 hash: "+md5.hexdigest())
    print("Image sha1 hash: "+sha1.hexdigest())

    return md5.hexdigest(),sha1.hexdigest()





def generate_html_report(output,image_name, start_time, end_time, image_type, case_no, evd_no, desc, examiner, notes, physical_block_size, logical_block_size, total_sectors, bytes_per_sector, partition_information, drive_model, drive_serial_number, partition_table, source_data_size, sector_count, drive_md5, drive_sha1, aq_started, aq_ended, ve_started, ve_ended, md5, sha1):
    with open('report_template.html') as file:
        template = Template(file.read())

    rendered_report = template.render(image_name=image_name, start_time=start_time, end_time=end_time, image_type=image_type, case_no=case_no, evd_no=evd_no, desc=desc, examiner=examiner, notes=notes, physical_block_size=physical_block_size, logical_block_size=logical_block_size, total_sectors=total_sectors, bytes_per_sector=bytes_per_sector, partition_information=partition_information, drive_model=drive_model, drive_serial_number=drive_serial_number, partition_table=partition_table, source_data_size=source_data_size, sector_count=sector_count, md5_hash=drive_md5, sha1_hash=drive_sha1, aq_started=aq_started, aq_ended=aq_ended, ve_started=ve_started, ve_ended=ve_ended, img_md5_hash=md5, img_sha1_hash=sha1)

    with open(output, 'w') as output_file:
        output_file.write(rendered_report)

# if __name__ == "__main__":
#     vol_loc="/dev/sda"
#     save_loc = "/home/man44/Documents/"
#     physical_block_size, logical_block_size, total_sectors, partition_information, model, serial_number, total_used_bytes, partition_table = get_info(vol_loc)
#     print("Generating hash")
#     drive_md5, drive_sha1 = calculate_hash(vol_loc)
#     generate_html_report(save_loc+"disk_imaging_report.html","NA","NA", "NA","NA", "NA", "NA", "NA", "NA", "NA", physical_block_size, logical_block_size, total_sectors,"", partition_information, model, serial_number,partition_table,total_used_bytes,total_sectors, drive_md5, drive_sha1,"NA","NA","","","NA","NA")

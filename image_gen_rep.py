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

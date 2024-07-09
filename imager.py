import pytsk3
import os

def create_image(volume_loc, output_file, block_size=4096):
    img_info = pytsk3.Img_Info(volume_loc)
    print(img_info)

    target_file = open(output_file,'wb')
    offset = 0

    try:
        while(offset < img_info.get_size()):
            data_available = min(block_size, img_info.get_size() - offset)
            data = img_info.read(offset, data_available)
            target_file.write(data)
            offset += len(data)

    finally:
        target_file.close()


def compress_disk_image(di_file):
    compressed_file = di_file+".gz"
    with open(di_file,'rb') as f_in:
        with gzip.open(compressed_file,'wb') as f_out:
            f_out.writelines(f_in)




if __name__== "__main__":
    volume_loc = input("Enter location ")
    output_file = "disk_image.dd"
    create_image(volume_loc,output_file)
    compress_disk_image(output_file)

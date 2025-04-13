import zipfile

def unzip_kmz(kmz_path, output_path="storage/temp_kmz"):
    with zipfile.ZipFile(kmz_path, 'r') as kmz:
        kmz.extractall(output_path)
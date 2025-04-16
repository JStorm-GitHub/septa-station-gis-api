import zipfile

def unzip_kmz(kmz_path, output_path):
    with zipfile.ZipFile(kmz_path, 'r') as kmz:
        kmz.extractall(output_path)
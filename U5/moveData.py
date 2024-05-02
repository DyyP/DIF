import shutil

quelle = "/home/kali/Desktop/Data"
ziel = "/home/kali/Desktop/mount_point"

shutil.copytree(quelle, ziel, dirs_exist_ok=True)

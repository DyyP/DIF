import os
import subprocess
import shutil

# Pfad zum virtuellen Laufwerk
disk_file = "/home/kali/Desktop/DIF/virtual_disk.img"

# Pfad zum Mount-Punkt
mount_point = "/home/kali/Desktop/DIF/mount_point"

# Create a 1GB virtual disk
disk_size = 1024 * 1024 * 1024 # 1 GB
disk_file = "virtual_disk.img"
with open(disk_file, "wb") as f:
    f.seek(disk_size - 1)
    f.write(b"\0")

# Format the virtual disk with FAT32
format_command = f"mkfs.fat -F 32 {disk_file}"
subprocess.run(format_command.split(" "))
print(f"Virtual disk created: {disk_file}")
print("Formatted with FAT32")

# Create a mount point
mount_point = "./mount_point"
if os.path.exists(mount_point):
    # If the mount point exists, delete it
    os.rmdir(mount_point)
os.mkdir(mount_point)

# Erstellen eines Loop-Geräts für das virtuelle Laufwerk
loop_device = subprocess.check_output(["losetup", "-f"]).decode().strip()
subprocess.run(["losetup", "-P", "--show", disk_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(f"Loop-Gerät erstellt: {loop_device}")

# Montieren des virtuellen Laufwerks
mount_command = f"mount {loop_device} {mount_point}"
subprocess.run(mount_command.split(" "))
print(f"Virtuelles Laufwerk an: {mount_point} gemountet.")

# Kopieren des Verzeichnisses in das virtuelle Laufwerk
source_directory = "/home/kali/Desktop/DIF/data"
destination_path = os.path.join(mount_point, os.path.basename(source_directory))
shutil.copytree(source_directory, destination_path)

print(f"Das Verzeichnis '{source_directory}' wurde erfolgreich in das virtuelle Laufwerk kopiert.")

 # Unmounten des Laufwerks
unmount_command = f"umount {mount_point}"
subprocess.run(unmount_command.split(" "))
print(f"Virtuelles Laufwerk von: {mount_point} entmontet.")

 # Löschen des Loop-Geräts
subprocess.run(["losetup", "-d", loop_device])
print(f"Loop-Gerät {loop_device} gelöscht.")

# Löschen des Mount-Punkts und aller darin enthaltenen Unterverzeichnisse
if os.path.exists(mount_point):
    shutil.rmtree(mount_point)
    print(f"Mount-Punkt '{mount_point}' und alle darin enthaltenen Unterverzeichnisse wurden gelöscht.")
else:
    print(f"Mount-Punkt '{mount_point}' existiert nicht mehr.")


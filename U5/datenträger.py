import os
import subprocess

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

# Mount the virtual disk
mount_command = f"sudo mount -o loop {disk_file} {mount_point}"
subprocess.run(mount_command.split(" "))
print(f"Virtual disk mounted at: {mount_point}")

# Unmount the disk (optional)
# unmount_command = f"umount {mount_point}"
# subprocess.run(unmount_command.split(" "))
# print(f"Virtual disk unmounted from: {mount_point}")

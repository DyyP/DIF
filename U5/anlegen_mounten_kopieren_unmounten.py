import os
import subprocess
import shutil
import time

# Pfad zum Verzeichnis, in dem der virtuelle Datenträger erstellt wird
disk_directory = "/home/kali/Desktop/DIF"

# Pfad zum Mount-Punkt
mount_point = os.path.join(disk_directory, "mount_point")

# Funktion zum Erstellen und Mounten eines virtuellen Datenträgers mit einer angegebenen Größe (in MB)
def create_and_mount_virtual_disk(disk_size_mb):
    disk_file_path = os.path.join(disk_directory, "virtual_disk.img")

    # Erstellen des virtuellen Datenträgers
    with open(disk_file_path, "wb") as f:
        f.seek(disk_size_mb * 1024 * 1024 - 1)
        f.write(b"\0")

    # Formatieren des virtuellen Datenträgers mit FAT32
    format_command = f"mkfs.fat -F 32 {disk_file_path}"
    subprocess.run(format_command.split(), check=True)

    print(f"Virtueller Datenträger erstellt: {disk_file_path}")
    print("Formatiert mit FAT32")

    # Erstellen des Mount-Punkts, falls noch nicht vorhanden
    if not os.path.exists(mount_point):
        os.makedirs(mount_point)
        print(f"Mount-Punkt erstellt: {mount_point}")

    # Suche nach einem verfügbaren Loop-Gerät
    loop_device_output = subprocess.run(["losetup", "-f"], capture_output=True, text=True, check=True)
    loop_device = loop_device_output.stdout.strip()

    # Anschließen des virtuellen Datenträgers am Loop-Gerät
    subprocess.run(["losetup", "-P", loop_device, disk_file_path], check=True)
    print(f"Virtueller Datenträger an Loop-Gerät angeschlossen: {loop_device}")

    # Mounten des virtuellen Datenträgers am Mount-Punkt
    mount_command = f"sudo mount {loop_device} {mount_point}"
    subprocess.run(mount_command.split(), check=True)
    print(f"Virtueller Datenträger montiert an: {mount_point}")

    # Rückgabe des Loop-Geräts und des Datenträgerpfads für das späterige Unmounten
    return loop_device, disk_file_path

try:
    # Erstellen und Mounten eines einzelnen 3GB virtuellen Datenträgers
    disk_size_mb = 3 * 1024  # 3GB in MB
    loop_device, disk_file_path = create_and_mount_virtual_disk(disk_size_mb)

    # Durchführen von Operationen auf dem gemounteten Datenträger (z.B. Kopieren von Dateien, etc.)
    source_directory = "/home/kali/Desktop/DIF/data"
    destination_path = os.path.join(mount_point, os.path.basename(source_directory))

    shutil.copytree(source_directory, destination_path)
    print(f"Verzeichnis '{source_directory}' kopiert auf virtuellen Datenträger an '{destination_path}'")

    # Zusätzliche Print-Anweisung nach erfolgreicher Abschluss der Aufgaben
    print("Alle Aufgaben erfolgreich abgeschlossen.")

finally:
    # Warten, bis der Mount-Punkt nicht mehr beschäftigt ist
    while True:
        check_open_files = subprocess.run(["lsof", "|", "grep", mount_point], capture_output=True, text=True, shell=True)
        if "open" not in check_open_files.stdout.lower():
            break
        print("Warte, bis der Mount-Punkt nicht mehr beschäftigt ist...")
        time.sleep(5)  # Warte 5 Sekunden, bevor die Überprüfung erneut durchgeführt wird

    # Leeren des Mount-Punkts, bevor er unmounted wird
    shutil.rmtree(mount_point)
    print(f"Mount-Punkt '{mount_point}' geleert.")

    # Unmounten des virtuellen Datenträgers
    unmount_command = f"sudo umount {mount_point}"
    subprocess.run(unmount_command.split(), check=True)
    print(f"Virtueller Datenträger vom: {mount_point} entmontiert")

    # Trennen des Loop-Geräts
    subprocess.run(["losetup", "-d", loop_device], check=True)
    print(f"Loop-Gerät {loop_device} getrennt")

    # Zwangsweise Löschen des Mount-Punkts
    try:
        subprocess.run(["sudo", "umount", "-l", mount_point], check=True)
        print(f"Zwangsweise entmontiert: {mount_point}")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Zwangsentfernen: {e}")

    try:
        os.rmdir(mount_point)
        print(f"Mount-Punkt '{mount_point}' gelöscht")
    except Exception as e:
        print(f"Fehler beim Löschen des Mount-Punkts: {e}")

# Reinigung des virtuellen Datenträger-Dateisystems
#if os.path.exists(disk_file_path):
    #os.remove(disk_file_path)
    #print(f"Virtueller Datenträger-Datei '{disk_file_path}' gelöscht")


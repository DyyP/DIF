import os
import shutil

# Pfad zum Mount-Punkt
mount_point = "./mount_point"

# Überprüfen, ob der Mount-Punkt existiert
if os.path.exists(mount_point):
    # Überprüfen, ob der Mount-Punkt leer ist
    if os.path.isdir(mount_point) and len(os.listdir(mount_point)) == 0:
        # Wenn der Mount-Punkt leer ist, löschen Sie ihn
        os.rmdir(mount_point)
        print(f"Mount-Punkt '{mount_point}' wurde erfolgreich entfernt.")
    else:
        # Wenn der Mount-Punkt nicht leer ist, entfernen Sie ihn vollständig
        shutil.rmtree(mount_point)
        print(f"Mount-Punkt '{mount_point}' wurde erfolgreich entfernt.")
else:
    print(f"Mount-Punkt '{mount_point}' existiert nicht.")

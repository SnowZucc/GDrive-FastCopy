import os
import zipfile
import shutil

# Paramètres
source_dirs = [
    #"C:/Users/Example/Example",
    #"C:/Users/Example/Example"

]

ignore_dirs = [
    #"C:/Users/Example/Example",
    #"C:/Users/Example/Example"
]

destination_root = "C:/Users/Example/Example"
cache_dir = "C:/Users/Example/Example"
copied_files_log = "C:/Users/Example/Example/copied_files.txt"

def create_zip(source_path, zip_path):
    if check_file_exists(zip_path):
        return "Déjà zippé"
    else: 
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_STORED) as zf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zf.write(file_path, os.path.relpath(file_path, source_path))
        print ("Je retourne", source_path)
        return source_path

def check_file_exists(source_path):
    with open(copied_files_log, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if source_path in line.strip():
                print(f"Le fichier {source_path} a déjà été copié.")
                return True
    return False

def count_files(directory):
    return sum([len(files) for r, d, files in os.walk(directory)])

def send_to_destination(source, real_source, dest):
    if check_file_exists(source):
        return
    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(source, dest)
        with open(copied_files_log, "a", encoding="utf-8") as f:
            f.write(f"{real_source}\n")
            print ("J'écris", real_source)
        print(f"Copié : {real_source} vers {dest}")
    except Exception as e:
        print(f"Erreur lors de la copie : {e}")

def process_directory(dir_path, base_dest, depth=0):
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        
        if item_path in ignore_dirs:
            print(f"Ignoré : {item_path}")
            continue

        relative_dest = os.path.join(base_dest, item)
        full_dest_path = os.path.join(destination_root, relative_dest)
        
        if os.path.isdir(item_path):
            if depth == 1:
                num_files = count_files(item_path)
                if num_files > 50:
                    zip_name = f"{item}.zip"
                    zip_path = os.path.join(cache_dir, zip_name)
                    print(f"Compression de {item_path} ({num_files} éléments)...")
                    zip_status = create_zip(item_path, zip_path)
                    if zip_status != "Déjà zippé":
                        print(f"Envoi du fichier zippé {zip_name}...")
                        print ("Chemin source du zip :", zip_status)
                        send_to_destination(zip_path, zip_status, os.path.join(destination_root, os.path.dirname(relative_dest), zip_name))
                        os.remove(zip_path)
                    continue

            process_directory(item_path, relative_dest, depth + 1)
        else:
            send_to_destination(item_path, item_path, full_dest_path)

def main():
    os.makedirs(cache_dir, exist_ok=True)
    if not os.path.exists(copied_files_log):
        open(copied_files_log, 'w').close()
    
    for source_dir_path in source_dirs:
        print(f"Traitement du dossier {source_dir_path}")
        base_name = os.path.basename(source_dir_path)
        process_directory(source_dir_path, base_name)

if __name__ == "__main__":
    main()
import os

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size):
    # Convert size in bytes to a more human-readable format (e.g., KB, MB, GB)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_subfolder_sizes(parent_folder):
    second_level_subfolders = []
    first_level_subfolders = [f.path for f in os.scandir(parent_folder) if f.is_dir()]
    
    for first_level_subfolder in first_level_subfolders:
        second_level_subfolders.extend([f.path for f in os.scandir(first_level_subfolder) if f.is_dir()])
    
    folder_sizes = {}
    for subfolder in second_level_subfolders:
        folder_size = get_folder_size(subfolder)
        folder_sizes[subfolder] = folder_size
    return folder_sizes

if __name__ == "__main__":
    parent_folder = "X:\\1 - Projects\\1168 - Oosterdam"  # Dont forget to double \\ in the path
    if not os.path.isdir(parent_folder):
        print("Invalid directory path")
    else:
        folder_sizes = get_subfolder_sizes(parent_folder)
        for folder, size in folder_sizes.items():
            print(f"{folder}: {format_size(size)}")

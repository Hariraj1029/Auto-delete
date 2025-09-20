import os
import json
import fnmatch
import shutil
from datetime import datetime

def matches_criteria(file_path, criteria):
    """
    Check if the file at file_path meets all specified criteria.
    Supported criteria:
      - fileNamePattern, fileNameContains, fileNameEndsWith, fileExtensions, containsString
      - fileSizeLessThan, fileSizeGreaterThan, fileSizeBetween
      - createdAgeDays, modifiedAgeDays, modifiedBetweenDays (all relative to now)
    """
    try:
        stat = os.stat(file_path)
        file_size = stat.st_size
        modified_time = datetime.fromtimestamp(stat.st_mtime)
        created_time = datetime.fromtimestamp(stat.st_ctime)
        file_name = os.path.basename(file_path)
        now = datetime.now()
    except Exception as e:
        print(f"Error accessing file stats for {file_path}: {e}")
        return False

    # File name criteria
    if "fileNamePattern" in criteria:
        if not fnmatch.fnmatch(file_name, criteria["fileNamePattern"]):
            return False

    if "fileNameContains" in criteria:
        if not any(file_name.contains(name) for name in criteria["fileNameContains"]):
        if criteria["fileNameContains"] not in file_name:
            return False

    if "fileNameEndsWith" in criteria:
        if not file_name.endswith(criteria["fileNameEndsWith"]):
            return False

    # File extension criteria
    if "fileExtensions" in criteria:
        if not any(file_name.endswith(ext) for ext in criteria["fileExtensions"]):
            return False

    # File content criteria
    if "containsString" in criteria:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                if criteria["containsString"] not in content:
                    return False
        except Exception as e:
            # Skip files that cannot be read as text
            return False

    # File size criteria
    if "fileSizeLessThan" in criteria:
        if file_size >= criteria["fileSizeLessThan"]:
            return False

    if "fileSizeGreaterThan" in criteria:
        if file_size <= criteria["fileSizeGreaterThan"]:
            return False

    if "fileSizeBetween" in criteria:
        size_range = criteria["fileSizeBetween"]
        min_size = size_range.get("min", 0)
        max_size = size_range.get("max", float('inf'))
        if not (min_size <= file_size <= max_size):
            return False

    # Relative age criteria (in days)
    now = datetime.now()

    if "createdAgeDays" in criteria:
        age_days = (now - created_time).days
        if age_days < criteria["createdAgeDays"]:
            return False

    if "modifiedAgeDays" in criteria:
        age_days = (now - modified_time).days
        if age_days < criteria["modifiedAgeDays"]:
            return False

    if "modifiedBetweenDays" in criteria:
        mod_range = criteria["modifiedBetweenDays"]
        age_days = (now - modified_time).days
        start = mod_range.get("start", 0)
        end = mod_range.get("end", float('inf'))
        if not (start <= age_days <= end):
            return False

    return True

def remove_empty_folders(root_path):
    """
    Recursively remove empty folders and subfolders starting from root_path.
    This function walks the directory tree in bottom-up order, deleting any directory that is empty.
    """
    for current_path, dirs, files in os.walk(root_path, topdown=False):
        # If the directory is empty, remove it
        if not os.listdir(current_path):
            try:
                os.rmdir(current_path)
                print(f"Deleted empty folder: {current_path}")
            except Exception as e:
                print(f"Failed to delete folder {current_path}: {e}")

def process_folder(folder_config):
    """
    Process a single folder as specified in the configuration.
    - If 'deleteEntireFolder' is True, the script deletes the entire folder (optionally based on folderAgeDays).
    - Otherwise, it scans files (recursively or not) and deletes those matching the criteria,
      then removes any empty folders and subfolders.
    """
    path = folder_config.get("path")
    if not path:
        print("Folder path not specified.")
        return

    now = datetime.now()
    delete_entire = folder_config.get("deleteEntireFolder", False)
    criteria = folder_config.get("criteria", {})

    if delete_entire:
        folder_age_ok = True
        if "folderAgeDays" in criteria:
            try:
                stat = os.stat(path)
                folder_mod_time = datetime.fromtimestamp(stat.st_mtime)
                folder_age = (now - folder_mod_time).days
                if folder_age < criteria["folderAgeDays"]:
                    folder_age_ok = False
                    folder_age_days = criteria['folderAgeDays']
                    print(f"Folder {path} is not older than {folder_age_days} days (age: {folder_age} days). Skipping deletion.")
            except Exception as e:
                print(f"Error accessing folder stats for {path}: {e}")
                folder_age_ok = False

        if folder_age_ok:
            try:
                shutil.rmtree(path)
                print(f"Deleted entire folder: {path}")
            except Exception as e:
                print(f"Failed to delete folder {path}: {e}")
        return

    recursive = folder_config.get("recursive", False)
    if recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if matches_criteria(file_path, criteria):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete file {file_path}: {e}")
    else:
        try:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path) and matches_criteria(file_path, criteria):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing directory {path}: {e}")

    # After file deletion, remove any empty folders and subfolders
    remove_empty_folders(path)

def main():
    # Load configuration from JSON file.
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading Config.json: {e}")
        return

    folders = config.get("folders", [])
    for folder_config in folders:
        process_folder(folder_config)

if __name__ == "__main__":
    main()

import os
import shutil

def copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies all contents (files and subdirectories) from a source
    directory to a destination directory. It first deletes the destination
    directory if it exists to ensure a clean copy. Includes enhanced logging
    and error handling.

    Args:
        source_dir (str): The path to the source directory.
        dest_dir (str): The path to the destination directory.
    """
    print(f"Starting recursive copy from '{source_dir}' to '{dest_dir}'")

    # Validate source directory existence
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist. Aborting copy.")
        return
    if not os.path.isdir(source_dir):
        print(f"Error: Source path '{source_dir}' is not a directory. Aborting copy.")
        return

    # 1. Delete all contents of the destination directory to ensure a clean copy
    if os.path.exists(dest_dir):
        print(f"Attempting to delete existing destination directory: {dest_dir}")
        try:
            shutil.rmtree(dest_dir)
            print(f"Successfully deleted: {dest_dir}")
        except OSError as e:
            print(f"Error deleting destination directory '{dest_dir}': {e}. Please check permissions.")
            return

    # 2. Recreate the destination directory
    print(f"Attempting to create new destination directory: {dest_dir}")
    try:
        os.mkdir(dest_dir)
        print(f"Successfully created: {dest_dir}")
    except OSError as e:
        print(f"Error creating destination directory '{dest_dir}': {e}. Please check permissions.")
        return

    # 3. Iterate through all items in the source directory and copy them
    copied_files_count = 0
    copied_dirs_count = 0

    try:
        items = os.listdir(source_dir)
    except OSError as e:
        print(f"Error listing contents of source directory '{source_dir}': {e}. Please check permissions.")
        return

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            # If it's a file, copy it directly
            try:
                print(f"Copying file: '{source_path}' to '{dest_path}'")
                shutil.copy(source_path, dest_path)
                copied_files_count += 1
            except IOError as e:
                print(f"Error copying file '{source_path}' to '{dest_path}': {e}. Skipping file.")
            except Exception as e:
                print(f"An unexpected error occurred while copying file '{source_path}': {e}. Skipping file.")
        elif os.path.isdir(source_path):
            # If it's a directory, recursively call the function
            print(f"Entering subdirectory for recursive copy: '{source_path}'")
            # The recursive call itself handles the creation and copying
            copy_directory_contents(source_path, dest_path)
            copied_dirs_count += 1 # Increment only after successful recursive call
        else:
            print(f"Skipping unknown item type or special file: '{source_path}'")

    print(f"Finished copying contents from '{source_dir}' to '{dest_dir}'")
    print(f"Summary for '{dest_dir}': Copied {copied_files_count} files and {copied_dirs_count} subdirectories.")

# Example usage (will be called from main.py)
if __name__ == "__main__":
    # This block is for testing this module directly, not needed when imported by main.py
    # You might create dummy directories here for quick local testing if needed.
    pass

import os
import zipfile
import argparse
import shutil  # For copying files

def is_apk(filepath):
    """Checks if a file ends with the .apk extension."""
    return filepath.lower().endswith(".apk")

def is_xapk(filepath):
    """Checks if a file ends with the .xapk extension."""
    return filepath.lower().endswith(".xapk")

def select_apks_xapks(directory, keywords=None, min_size_mb=None, max_size_mb=None):
    """
    Selects APK and XAPK files within a directory based on optional criteria.

    Args:
        directory (str): The path to the directory to search.
        keywords (list, optional): A list of keywords that must be present in the filename (case-insensitive). Defaults to None.
        min_size_mb (float, optional): The minimum file size in megabytes. Defaults to None.
        max_size_mb (float, optional): The maximum file size in megabytes. Defaults to None.

    Returns:
        list: A list of absolute paths to the selected APK and XAPK files.
    """
    selected_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if is_apk(filepath) or is_xapk(filepath):
                # Keyword filtering
                if keywords:
                    filename_lower = filename.lower()
                    if not all(keyword.lower() in filename_lower for keyword in keywords):
                        continue

                # Size filtering
                file_size_mb = os.path.getsize(filepath) / (1024 * 1024)  # Convert bytes to MB
                if min_size_mb is not None and file_size_mb < min_size_mb:
                    continue
                if max_size_mb is not None and file_size_mb > max_size_mb:
                    continue

                selected_files.append(filepath)
    return selected_files

def create_zip_archive(output_zip_path, file_paths, delete_originals=False):
    """
    Creates a ZIP archive containing the specified files.

    Args:
        output_zip_path (str): The path to the output ZIP file.
        file_paths (list): A list of file paths to include in the ZIP.
        delete_originals (bool, optional): Whether to delete the original files after zipping. Defaults to False.
    """
    try:
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                zipf.write(file_path, os.path.basename(file_path))  # Store with original filename
        print(f"Successfully created ZIP archive: {output_zip_path}")
        if delete_originals:
            for file_path in file_paths:
                os.remove(file_path)
            print("Original files deleted.")
    except Exception as e:
        print(f"Error creating ZIP archive: {e}")

def main():
    parser = argparse.ArgumentParser(description="Select and ZIP APK/XAPK files.")
    parser.add_argument("directory", help="The directory to search for APK/XAPK files.")
    parser.add_argument("-o", "--output", default="selected_apks.zip", help="The name of the output ZIP file.")
    parser.add_argument("-k", "--keywords", nargs='+', help="Keywords that must be present in the filenames.")
    parser.add_argument("--min_size", type=float, help="Minimum file size in MB.")
    parser.add_argument("--max_size", type=float, help="Maximum file size in MB.")
    parser.add_argument("--delete", action="store_true", help="Delete original files after zipping.")
    args = parser.parse_args()

    selected_files = select_apks_xapks(args.directory, args.keywords, args.min_size, args.max_size)

    if selected_files:
        print("Selected files:")
        for file in selected_files:
            print(f"- {file}")
        create_zip_archive(args.output, selected_files, args.delete)
    else:
        print("No APK or XAPK files found matching the criteria.")

if __name__ == "__main__":
    main()

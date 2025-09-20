import os
import re

def get_files_from_folder(folder_name):
  """
  Testing 1234
  
  Gets a list of all files in a specified folder.

  Args:
    folder_name (str): The name of the folder to search.

  Returns:
    list: A list of full file paths found in the folder.
  """
  try:
    # Use os.listdir() to get all entries (files and directories)
    # We return full paths for easier manipulation.
    files = [os.path.join(folder_name, f) for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
    return files
  except FileNotFoundError:
    print(f"Error: The folder '{folder_name}' was not found. Please ensure it exists.")
    return []
  except Exception as e:
    print(f"An unexpected error occurred while listing files: {e}")
    return []

def rename_hdf5_files_sequentially(folder_name, prefix_var, file_ext_var):
  """
  Iterates through files in a folder, extracts the ID from filenames matching
  '{prefix}{id}.{file_ext}', and renames them to be sequentially numbered from 0.

  Args:
    folder_name (str): The path to the folder containing the files.
    prefix_var (str): The expected prefix of the filenames (e.g., "episode").
    file_ext_var (str): The expected file extension (e.g., "hdf5").
  """
  all_files_in_folder = get_files_from_folder(folder_name)

  if not all_files_in_folder:
    print("No files found or the specified folder does not exist. Exiting renaming process.")
    return

  target_files_with_ids = []
  expected_full_ext = f".{file_ext_var.lower()}" # Ensure case-insensitivity for extension

  # First, filter and extract current IDs, and store them with their paths.
  for fpath in all_files_in_folder:
    base_name = os.path.basename(fpath) # e.g., "episode123.hdf5"
    name_without_ext, ext = os.path.splitext(base_name) # e.g., "episode123", ".hdf5"

    # Check if the file matches the defined prefix and extension
    if ext.lower() == expected_full_ext and name_without_ext.startswith(prefix_var):
      # Extract the ID part after the prefix
      id_str = name_without_ext[len(prefix_var):]

      if id_str.isdigit():
        try:
          current_id = int(id_str)
          target_files_with_ids.append((fpath, current_id)) # Store (full_path, current_id)
        except ValueError:
          print(f"Warning: Could not convert extracted ID '{id_str}' from '{base_name}' to an integer. Skipping this file.")
      else:
        print(f"Warning: Filename '{base_name}' matches prefix/extension but the ID part '{id_str}' is not purely numeric. Skipping this file.")
    # Files not matching the pattern are silently ignored

  if not target_files_with_ids:
    print(f"No files matching the pattern '{prefix_var}*.'{file_ext_var}' were found in '{folder_name}'.")
    return

  # Sort the list of (filepath, current_id) tuples by their current ID.
  # This ensures that when we apply sequential new IDs (0, 1, 2, ...),
  # the files are processed and re-numbered in their natural numerical order.
  target_files_with_ids.sort(key=lambda x: x[1])

  print(f"\nFound {len(target_files_with_ids)} files matching '{prefix_var}*.'{file_ext_var}' for sequential renaming in '{folder_name}'...")

  # Now, iterate with a sequential counter 'i'
  for i, (old_filepath, current_id) in enumerate(target_files_with_ids):
    base_name = os.path.basename(old_filepath)

    # Check if the current file's ID is already correct for its sequential position
    if current_id != i:
      new_file_name = f"{prefix_var}{i}.{file_ext_var}"
      new_filepath = os.path.join(folder_name, new_file_name)

      print(f"Renaming '{base_name}' to '{new_file_name}'...")
      try:
        os.rename(old_filepath, new_filepath)
        print(f"Successfully renamed '{base_name}' to '{new_file_name}'")
      except FileExistsError:
        print(f"Error: A file named '{new_file_name}' already exists. Skipping rename for '{base_name}'.")
      except Exception as e:
        print(f"An error occurred while renaming '{base_name}': {e}")
    else:
      print(f"File '{base_name}' already has the correct sequential ID ({current_id}). No rename needed.")

# --- Example Usage (for testing purposes) ---
if __name__ == "__main__":
  test_folder_name = "./data/place_shoe/demo_randomized/data/"
  # Define your variables here:
  my_prefix = "episode"
  my_file_ext = "hdf5"

  # Create a dummy folder and some dummy files for demonstration
  #os.makedirs(test_folder_name, exist_ok=True)

  # Create files with various IDs and formats
  #open(os.path.join(test_folder_name, "episode0.hdf5"), "w").close()  # Correctly named
  #open(os.path.join(test_folder_name, "episode3.hdf5"), "w").close()  # Will be renamed to episode1.hdf5
  #open(os.path.join(test_folder_name, "episode1.hdf5"), "w").close()  # Will be renamed to episode2.hdf5
  #open(os.path.join(test_folder_name, "episode5.hdf5"), "w").close()  # Will be renamed to episode3.hdf5
  #open(os.path.join(test_folder_name, "episode_10.hdf5"), "w").close() # Will be skipped (incorrect ID format)
  #open(os.path.join(test_folder_name, "not_an_episode.hdf5"), "w").close() # Will be skipped (incorrect prefix)
  #pen(os.path.join(test_folder_name, "episode4.txt"), "w").close() # Will be skipped (incorrect extension)

  print(f"Initial files in '{test_folder_name}': {sorted(os.listdir(test_folder_name))}")

  # Run the renaming function
  rename_hdf5_files_sequentially(test_folder_name, my_prefix, my_file_ext)

  print(f"\nFinal files in '{test_folder_name}': {sorted(os.listdir(test_folder_name))}")

  # To clean up the dummy folder and files after testing, uncomment the following:
  # import shutil
  # shutil.rmtree(test_folder_name)
  # print(f"\nCleaned up the '{test_folder_name}' folder.")
import os
from pathlib import Path
from typing import List, Union, Callable, Any, Generator, Tuple

def get_all_files(path: str, *, 
                  extension: Union[str, List[str], None] = None, 
                  abs_path: bool = False) -> List[str]:
    """Retrieves all files in the specified directory with optional filtering by extension.

    Args:
        path (str): The directory path where files are located.
        extension (Union[str, List[str], None], optional): File extension(s) to filter by.
            Can be a string (for a single extension), a list of strings (for multiple extensions),
            or None to include all files. Defaults to None.
        abs_path (bool, optional): Whether to return absolute file paths. Defaults to False.

    Returns:
        List[str]: A list of file paths matching the specified criteria.
    """
    # Get all files at path
    files = [os.path.join(path, file) for file in os.listdir(path)]

    # filter out directories
    files = [file for file in files if os.path.isfile(file)]

    # filter by extension
    if extension is not None:
        if isinstance(extension, str):
            extension = [ extension ]

        # Normalize extensions for case-insensitive matching
        extension = {ext.lower() for ext in extension}

        # filtering
        files = [file for file in files if os.path.splitext(file)[1].lower() in extension ]

    # Convert to absolute paths if required
    if abs_path:
        files = [os.path.abspath(file) for file in files]

    return files

def batch_file_loader(files: list, 
                         batch_size: int,
                         open_file_func: Callable[[str], Any]) -> Generator[List[Any], None, None]:
    """
    Generates batches of file contents by loading files in groups of a specified size.

    Args:
        files (List[str]): A list of file paths to be opened.
        batch_size (int): The number of files to load in each batch.
        open_file_func (Callable[[str], Any]): A function that takes a file path as input
                                               and returns the file's content.

    Yields:
        Generator[List[Any], None, None]: A generator yielding lists of file contents,
                                          where each list contains the contents of up to 
                                          `batch_size` files.
    """
    # calculate the number of batch to be opened
    files_length = len(files)
    num_batches = (files_length + batch_size - 1) // batch_size

    # generator
    for i in range(num_batches):
        start_index = i * batch_size
        batch = [open_file_func(files[j]) for j in range(start_index, min(start_index + batch_size, files_length))]
        yield batch


def _get_folder_structure(
    path: Path, 
    max_depth: int, 
    depth: int, 
    prefix: str,
    bypass: List[str]
) -> List[str]:
    """
    Recursively display the folder structure in a tree-like format.

    Args:
        path (Path): The current directory path.
        max_depth (int): The maximum depth to display in the tree.
        depth (int): The current depth level (used internally for recursion).
        prefix (str): The prefix for the current depth level, used to draw the tree structure.
        bypass (List[str]): List of directories/files to bypass.

    Returns:
        List[str]: A list representing the folder structure.
    """
    folder_structure = []

    try:
        entries = sorted([entry for entry in path.iterdir() if entry.name not in bypass])
    except PermissionError:
        folder_structure.append(f"{prefix}Permission denied: {path}")
        return folder_structure

    num_entries = len(entries)
    for i, entry in enumerate(entries):
        is_last = (i == num_entries - 1)

        connector = "└── " if is_last else "├── "
        new_prefix = prefix + ("    " if is_last else "│   ")

        folder_structure.append(f"{prefix}{connector}{entry.name}/" if entry.is_dir() else f"{prefix}{connector}{entry.name}")

        if entry.is_dir() and (max_depth == -1 or depth < max_depth):
            folder_structure.extend(_get_folder_structure(entry, max_depth, depth + 1, new_prefix, bypass))

    return folder_structure


def get_folder_structure(path: str = ".", max_depth: int = -1, bypass: List[str] = None) -> str:
    """
    Display the folder structure of a directory in a tree-like format.

    Args:
        path (str): The root directory path to start displaying the structure. Defaults to the current directory (".").
        max_depth (int): The maximum depth to display in the tree. Defaults to -1 (no limit).
        bypass (List[str]): List of directories/files to bypass.
    
    Returns:
        str: The folder structure formatted as a tree.
    """
    path_obj = Path(path)

    if not path_obj.exists():
        raise ValueError(f"Path '{path}' does not exist.")
    if not path_obj.is_dir():
        raise ValueError(f"Path '{path}' is not a directory.")
    
    if bypass is None:
        bypass = []

    # Initialize the folder structure with the base directory
    folder_structure = [f"{path_obj.resolve().name}/"]
    
    # Recursively build the folder structure
    folder_structure.extend(_get_folder_structure(path_obj, max_depth, 0, "", bypass))
    return '\n'.join(folder_structure)

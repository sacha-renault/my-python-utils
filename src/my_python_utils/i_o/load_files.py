import os
from typing import List, Union, Callable, Any, Generator

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
from typing import Callable, Optional
from os import scandir


def process_directory(
    dir: str,
    *,
    file_callable: Optional[Callable[[str], None]] = None,
    dir_callable: Optional[Callable[[str], None]] = None,
    symlink_callable: Optional[Callable[[str], None]] = None,
):
    """Apply the given callables to files, directories, and symlinks in the specified directory.

    Callables should accept one argument:  The path to the object:
        a_callable(str) -> None

    Args:
        dir (str): _description_
        file_callable (Optional[Callable[[str], None]], optional): _description_. Defaults to None.
        dir_callable (Optional[Callable[[str], None]], optional): _description_. Defaults to None.
        symlink_callable (Optional[Callable[[str], None]], optional): _description_. Defaults to None.
    """
    with scandir(dir) as files:
        for a_file in files:
            if a_file.is_file() and file_callable is not None:
                file_callable(a_file.path)
            if a_file.is_dir() and dir_callable is not None:
                dir_callable(a_file.path)
            if a_file.is_symlink() and symlink_callable is not None:
                symlink_callable(a_file.path)

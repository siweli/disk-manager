import os



def get_directory_size(path):
    """
    Recursively computes the total size (in bytes) of all files in `path`.
    Symlinks are not followed.
    """
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_directory_size(entry.path)
    except Exception as e:
        # print(f'Error: {e}')
        pass
    return total



def traverse_directories(root_path):
    """
    Walks the tree under `root_path`, computing and collecting the size
    of each folder it visits (including the root itself).
    Returns a list of (absolute_path, size_bytes).
    """
    # init vars
    results = {}
    ignore_paths = [
        # 'C:\Windows',
        # 'C:\Program Files',
        # 'C:\Program Files (x86)',
        # 'C:\ProgramData',
        # 'C:\Recovery',
        # 'C:\MSOCache',
        # 'C:\System Volume Information',
        # 'C:\$Recycle.Bin',
        # 'C:\PerfLogs'
    ]

    def _rec(path):
        # normalize the path
        key_name = os.path.normpath(path)

        print(key_name)

        # if the path is not an ignore path then proceed
        if key_name not in ignore_paths:
            # get the size of the path
            size = get_directory_size(path)
            results[key_name] = size

            # now recurse into immediate subdirectories
            try:
                for entry in os.scandir(path):
                    if entry.is_dir(follow_symlinks=False):
                        _rec(entry.path)
            except Exception as e:
                # print(f'Error: {e}')
                ignore_paths.append(path)

    _rec(os.path.abspath(root_path))
    return results
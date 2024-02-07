import os


def clear_folder(folder_path):
    '''
    Clears all files within a specified folder.

    Args:
        folder_path (str): Path to the folder to be cleared.

    Returns:
    - None
    '''
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print('Data folder cleared successfully.')
    else:
        print('Data folder does not exist.')

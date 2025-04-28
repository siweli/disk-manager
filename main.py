import json
from folder_traversal import traverse_directories
from file_explorer import create_file_explorer



if __name__ == '__main__':
    # get the data
    print('scanning pc')
    start_path = r'C:/'
    data = traverse_directories(start_path)
    print('done')

    # save the data
    with open(r'C:\Users\siwel\Desktop\computing\cool\folder manager\size_map.json', 'w') as f:
        json.dump(data, f)

    # display the file explorer
    create_file_explorer(start_path, data)



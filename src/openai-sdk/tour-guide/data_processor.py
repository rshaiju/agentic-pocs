
import os

GET_FILES_TOOLS_JSON = {
    "name": "get_files",
    "description": "Get a list of files in the specified directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The path to the directory."
            }
        },
        "required": ["path"]
    }
}

def get_files(path):
    """
    Get a list of files in the specified directory.

    Args:
        path (str): The path to the directory.

    Returns:
        list: A list of file paths in the directory.
    """
    script_dir= os.path.dirname(os.path.abspath(__file__))
    fully_qualified_path = script_dir + "/" + path

    return [os.path.join(fully_qualified_path, f) for f in os.listdir(fully_qualified_path) if os.path.isfile(os.path.join(fully_qualified_path, f))]  

GET_FILE_CONTENT_TOOLS_JSON = {
    "name": "get_file_content",
    "description": "Get the content of a specified file.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file."
            }
        },
        "required": ["file_path"]
    }
}

def get_file_content(file_path):
    """
    Get the content of a specified file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()  
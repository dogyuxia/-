import os

def get_project_root() -> str:

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    current_root = os.path.dirname(current_dir)

    return current_root

def get_abs_path(relative_path: str) -> str:
    return os.path.join(get_project_root(), relative_path)





if __name__ == "__main__":
   print(get_abs_path("data\\ata.csv"))
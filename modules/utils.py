import os


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def list_directories(directory):
    return [
        d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))
    ]

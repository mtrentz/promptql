# Function that reads the env file and loads the environment variables
import os


def load_env(path) -> None:
    """
    Load environment variables from a file if it exists.
    """
    # Check if the file exists
    if not os.path.exists(path):
        return

    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            k, v = line.split("=", 1)
            os.environ[k] = v

import sys
from pathlib import Path
from utils import get_file_bpm


if __name__ == "__main__":

    files = []

    if len(sys.argv) > 1:
        # Use this to test specific files
        files = [
            Path(file)
            for file in sys.argv[1::]
        ]
    else:
        # Without any arguments, it will test every
        # file in the subdirectory `test`
        files = [
            file
            for file in Path('test').iterdir()
            if file.is_file()
        ]

    for file in files:
        print(f"Testing {file}")
        tempo_found = get_file_bpm(str(file))
        print(f"tempo found = {tempo_found}\n")

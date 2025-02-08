from utils.reader import Reader
from sys import argv
import time

def main():
    start = time.time()
    if len(argv) < 2:
        print("Usage: python cdb.py [CSV filepath]")
    file_path = argv[1]
    reader = Reader(file_path)

    print(time.time() - start)


if __name__ == "__main__":
    main()
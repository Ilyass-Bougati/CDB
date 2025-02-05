from utils.reader import Reader
from sys import argv

def main():
    if len(argv) < 2:
        print("Usage: python cdb.py [CSV filepath]")
    file_path = argv[1]
    reader = Reader(file_path)


if __name__ == "__main__":
    main()
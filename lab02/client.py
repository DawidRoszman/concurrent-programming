import os
from time import sleep
import errno

def take_input_from_user():
 return input("Podaj linię tekstu albo znak końca '\\e':")

class FileLockException(Exception):
    pass


def write_to_file(data: str):
    with open("server-buffor", "w") as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, "r") as f:
        return f.readline()

def main():
    while True:
        try:
            fd = os.open("lockfile", os.O_CREAT|os.O_EXCL|os.O_RDWR)
            break;
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            print("Lockfile exists, waiting for it to be removed")
            sleep(3)
    user_input = ""
    input_line = ""
    while(input_line != "\\e"):
        user_input += f"{input_line}\n"
        input_line = take_input_from_user()
    write_to_file(f"{os.getpid()}\n" + user_input)
    result_file_exists = False
    while not result_file_exists:
        if os.path.exists(str(os.getpid())):
            result_file_exists = True
            result = read_from_file(str(os.getpid()))
            print(result)
            os.remove(str(os.getpid()))
            os.remove("lockfile")

if __name__ == "__main__":
    main()

import os
from time import sleep

def write_to_file(data: str, filename):
    with open(filename, "w") as f:
        f.write(data)
        print("Wpisano dane do pliku")

def read_from_file():
    with open("server-buffor", "r") as f:
        return f.readlines()

def main():
    running = True
    while running:
        file_exists = False
        while not file_exists:
            if os.path.exists("server-buffor"):
                file_exists = True
                result = read_from_file()
                print("Odczytano dane z pliku", result)
                os.remove("server-buffor")
                write_to_file(' '.join([x.strip() for x in result[1:]]), result[0].strip())
            sleep(1)


if __name__ == "__main__":
    main()

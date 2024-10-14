import os
from time import sleep
def take_input_from_user():
 return input("Podaj pojedynczą liczbę całkowitą: ")


def write_to_file(data: str):
    with open("dane", "w") as f:
        f.write(data)

def read_from_file():
    with open("wyniki", "r") as f:
        return f.readline()

def main():
    running = True
    while running:
        x = take_input_from_user()
        write_to_file(x)
        print("Wpisano dane do pliku", x)
        file_exists = False
        while not file_exists:
            if os.path.exists("wyniki"):
                file_exists = True
                result = read_from_file()
                os.remove("wyniki")
                print(result)
            sleep(1)


if __name__ == "__main__":
    main()

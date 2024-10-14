import os
from time import sleep

def write_to_file(data: str):
    with open("wyniki", "w") as f:
        f.write(data)
        print("Wpisano dane do pliku")

def read_from_file():
    with open("dane", "r") as f:
        return f.readline()

def calculate_equation(data: str):
    number = int(data)
    return number * 2


def main():
    running = True
    while running:
        file_exists = False
        while not file_exists:
            if os.path.exists("dane"):
                file_exists = True
                result = read_from_file()
                print("Odczytano dane z pliku", result)
                os.remove("dane")
                calculated_result = calculate_equation(result)
                write_to_file(str(calculated_result))
            sleep(1)


if __name__ == "__main__":
    main()

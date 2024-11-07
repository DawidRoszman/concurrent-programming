import os
import sys

INPUT="\\input"

def main():
    counter = 0
    args = sys.argv
    if len(args) != 3:
        print_help()
        return
    path_to_a_file = args[1]
    word = args[2]
    words = words_in_file(path_to_a_file)
    num_of_words = count_words_in_list(words, word)
    counter += num_of_words
    counter += handle_input(words, word)
    print(f"Number of words in files: {counter}")
def words_in_file(file):
    with open(file, "r") as f:
        lines = f.readlines()
        words = [x for xs in [x.strip().split(" ") for x in lines] for x in xs]
        return words
        

def extract_file_name_from_input(input_word):
    return input_word[len(INPUT)+1:-1]

def handle_input(list_of_words, input_word):
    total_count = 0
    forks = []
    for word in list_of_words:
        if word.startswith(INPUT):
            parameterForFork = extract_file_name_from_input(word)
            pid = os.fork()
            forks.append(pid)
            if pid == 0:
                words = words_in_file(parameterForFork)
                num_of_words = count_words_in_list(words, input_word)
                child_count = handle_input(words, input_word)
                os._exit(num_of_words + child_count)
    for pid in forks:
        pid, status = os.waitpid(pid, 0)
        if os.WIFEXITED(status):
            exit_code = os.WEXITSTATUS(status)
            total_count += exit_code

    return total_count 

def count_words_in_list(list_of_words, word):
    return sum(1 for w in list_of_words if w == word)


def print_help():
    print("python main.py <path_to_a_file> <word>")

if "__main__" == __name__:
    main()


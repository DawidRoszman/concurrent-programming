#include <iostream>
#include <sys/fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
  std::string userInput, path, stringid;
  int fd1, id;
  bool seenSeparator = false;
  std::cout << "Enter query (format: <id>:<path>)" << std::endl;
  std::cin >> userInput;
  for (int i = 0; i < sizeof(userInput); i++) {
    if (userInput[i] == ':') {
      seenSeparator = true;
      continue;
    }
    if (!seenSeparator) {
      stringid += userInput[i];
    } else {
      path += userInput[i];
    }
  }
  std::cout << path.c_str() << ' ' << id << std::endl;
  mkfifo(path.c_str(), 0666);
  const char *serverFifo = "serverFifo";
  fd1 = open(serverFifo, O_WRONLY);
  write(fd1, userInput.c_str(), userInput.length());
  close(fd1);
  fd1 = open(path.c_str(), O_RDONLY);
  char serverResponse[80];
  read(fd1, serverResponse, sizeof(serverResponse));
  std::cout << serverResponse << std::endl;

  return 0;
}

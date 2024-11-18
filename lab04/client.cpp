#include <iostream>
#include <sys/fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
  std::string userInput, path;
  int fd1;
  std::cout << "Enter query (format: <id>:<path>)" << std::endl;
  std::cin >> userInput;
  path = userInput.substr(userInput.find(':') + 1);
  std::cout << path << '\n';
  mkfifo(path.c_str(), 0666);
  const char *serverFifo = "serverFifo";
  fd1 = open(serverFifo, O_WRONLY);
  write(fd1, userInput.c_str(), userInput.length()+1);
  close(fd1);
  std::cout << "Waiting for response..." << '\n';
  fd1 = open(path.c_str(), O_RDONLY);
  char serverResponse[80];
  read(fd1, serverResponse, sizeof(serverResponse));
  remove(path.c_str());
  std::cout << "Server response: " << serverResponse << std::endl;

  return 0;
}

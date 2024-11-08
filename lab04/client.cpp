#include <iostream>
#include <sys/fcntl.h>
#include <unistd.h>
int main()
{
  char userInput[80];
  std::cout << "Enter query (format: <id>:<path>)" << std::endl;
  std::cin >> userInput;
  int fd1;
  const char *serverFifo = "serverFifo";
  fd1 = open(serverFifo, O_WRONLY);
  write(fd1, userInput, sizeof(userInput));
  close(fd1);

  
  return 0;
}

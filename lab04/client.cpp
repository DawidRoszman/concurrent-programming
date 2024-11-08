#include <iostream>
#include <sys/fcntl.h>
#include <unistd.h>

int main()
{
  char userInput[80], path[80], charid[80];
  int fd1, id, counter = 0;
  bool seenSeparator = false;
  std::cout << "Enter query (format: <id>:<path>)" << std::endl;
  std::cin >> userInput;
  for(int i = 0; i < sizeof(userInput); i++){
    if (userInput[i] == ':'){
      seenSeparator = true;
      continue;
    }
    if(!seenSeparator){
      counter++;
      charid[i] = userInput[i];
    }else {
      path[i-counter] = userInput[i];
    }
  }
  std::cout << path << ' ' << charid << std::endl;
  /*const char *serverFifo = "serverFifo";*/
  /*fd1 = open(serverFifo, O_WRONLY);*/
  /*write(fd1, userInput, sizeof(userInput));*/
  /*close(fd1);*/

  
  return 0;
}

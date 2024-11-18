#include <cctype>
#include <csignal>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>

static int currentId = 0;
const char *serverFifo = "serverFifo";

void handle_sighup(int signum) {
  std::cout << "Caught signal" << signum << '\n';
}

void handle_sigusr1(int signum) {
  std::cout << "Caught SIGUSR1. Exiting program..." << '\n';
  remove(serverFifo);
  exit(0);
}

class User {
private:
  int id;
  std::string lastName;

public:
  User(std::string lastName) {
    id = currentId;
    currentId++;
    setLastName(lastName);
  }
  void setLastName(std::string lastName) { this->lastName = lastName; }
  int getId() { return id; }
  std::string getLastName() { return lastName; }
};

void insertUsers(std::vector<User> *users);

int main() {

  signal(SIGHUP, handle_sighup);
  signal(SIGTERM, handle_sighup);
  signal(SIGUSR1, handle_sigusr1);

  std::vector<User> users;
  insertUsers(&users);
  int fd1, fd2;
  bool running = true;
  mkfifo(serverFifo, 0666);
  std::cout << "Fifo with name: " << serverFifo << " created" << '\n';
  std::cout << "Server started" << '\n';
  
  while (running) {
    char clientInput[80];
    int id = 0;
    std::string clientFifoPath, clientId;
    fd1 = open(serverFifo, O_RDONLY);
    read(fd1, clientInput, sizeof(clientInput));
    std::string clientInputStr = clientInput;
    if (clientInputStr == "") {
      std::cout << "Client input is empty" << '\n';
      continue;
    }
    std::cout << "Read client " << clientInputStr << '\n';
    close(fd1);
    sleep(3);
    clientId = clientInputStr.substr(0, clientInputStr.find(':'));
    clientFifoPath = clientInputStr.substr(clientInputStr.find(':') + 1);
    std::cout << clientId << ' ' << clientFifoPath << '\n';
    id = std::stoi(clientId);
    const char *clientFifo = clientFifoPath.c_str();
    fd2 = open(clientFifo, O_WRONLY);

    for (int i = 0; i < users.size(); i++) {
      if (users[i].getId() == id) {
        std::string userLastName = users[i].getLastName();
        std::cout << "User last name: " << userLastName << '\n';
        std::cout << "Writing to fifo: " << clientFifoPath.c_str() << ' '
                  << userLastName << '\n';
        write(fd2, userLastName.c_str(), userLastName.length()+1);
        close(fd2);
        break;
      }
    }
  }

  return 0;
}

void insertUsers(std::vector<User> *users) {
  users->push_back(User("User 1"));
  users->push_back(User("User 2"));
  users->push_back(User("User 3"));
  users->push_back(User("User 4"));
  users->push_back(User("User 5"));
}

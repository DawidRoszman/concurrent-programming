#include <cctype>
#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <string>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <vector>

static int currentId = 0;

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
  std::vector<User> users;
  insertUsers(&users);
  std::cout << users[0].getLastName() << std::endl;
  int fd1;
  bool running = true;
  const char *serverFifo = "serverfifo";
  mkfifo(serverFifo, 0666);
  char clientInput[80];
  while (running) {
    fd1 = open(serverFifo, O_RDONLY);
    read(fd1, clientInput, sizeof(clientInput));
    if (!isdigit(clientInput[0])) {
      std::cout << "Provided input had incorrect format" << std::endl;
      continue;
    }
    close(fd1);
    int id = clientInput[0] - '0';
    std::string clientFifoPath;
    for (int i = 2; i < sizeof(clientInput); i++){
      if(clientInput[i] == '\n'){
        break;
      }
      clientFifoPath += clientInput[i];
      std::cout << clientInput[i] << std::endl;
    }
    std::cout << clientFifoPath << std::endl;
    std::cout << id << std::endl;
    for (int i = 0; i < users.size(); i++) {
      std::cout << i << " " << users[i].getId() << std::endl;
      if (users[i].getId() == id) {
        std::string userLastName = users[i].getLastName();
        std::cout << "User last name: " <<  userLastName << std::endl;
        std::cout << "Creating FIFO with path: " << clientFifoPath << std::endl;
        const char *clientFifo = clientFifoPath.c_str();
        mkfifo(clientFifo, 0666);
        fd1 = open(clientFifo, O_WRONLY);
        std::cout << "Writing to fifo" << userLastName << std::endl;
        write(fd1, userLastName.c_str(), userLastName.length());
        close(fd1);
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

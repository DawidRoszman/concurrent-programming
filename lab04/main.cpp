#include <string>
#include <sys/types.h>
#include <sys/stat.h>

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

int main() {
  bool running = true;
  char *serverFifo = "serverfifo";
  mkfifo(serverFifo, 0666);
  char str1[21];
  while(running){



  }

  return 0;
}

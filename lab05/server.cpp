#include <cctype>
#include <csignal>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <map>
#include <string>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

struct mesg_buffer {
  long mesg_type;
  char mesg_text[100];
  int sender;
};

static int msgid_in, msgid_out;

static void handle_sighup(int signum) {
  std::cout << "Caught signal " << signum << '\n';
}

static void handle_exitsignal(int signum) {
  std::cout << "Caught exit signal. Exiting program..." << '\n';
  msgctl(msgid_in, IPC_RMID, 0);
  msgctl(msgid_out, IPC_RMID, 0);
  exit(0);
}
static std::map<std::string, std::string> translations{{"kot", "cat"},
                                                       {"pies", "dog"}};

int main() {

  signal(SIGHUP, handle_sighup);
  signal(SIGTERM, handle_sighup);
  signal(SIGUSR1, handle_exitsignal);
  signal(SIGINT, handle_exitsignal);

  key_t key_in, key_out;

  key_in = ftok("in", 65);
  key_out = ftok("out", 65);

  msgid_in = msgget(key_in, 0666 | IPC_CREAT);
  msgid_out = msgget(key_out, 0666 | IPC_CREAT);

  bool running = true;
  std::cout << "Server started" << '\n';

  while (running) {
    mesg_buffer message;
    msgrcv(msgid_in, &message, sizeof(message), 1, 0);

    std::cout << "Read client " << message.mesg_text << " from " << message.sender << '\n';
    sleep(3);

    auto result = translations.find(message.mesg_text);
    message.mesg_type = message.sender;
    if (result != translations.end()) {
      strcpy(message.mesg_text, result->second.c_str());
      message.mesg_text[sizeof(message.mesg_text) - 1] = '\0';  // Null-terminate
    } else {
      strcpy(message.mesg_text, "Word not found in dictionary");
      message.mesg_text[sizeof(message.mesg_text) - 1] = '\0';  // Null-terminate
    }
    msgsnd(msgid_out, &message, sizeof(message), 0);
  }

  return 0;
}

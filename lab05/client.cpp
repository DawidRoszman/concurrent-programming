#include <cstdio>
#include <iostream>
#include <sys/fcntl.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

struct mesg_buffer {
  long mesg_type;
  char mesg_text[100];
  int sender;
} message;

int main() {
  key_t key_in, key_out;
  int msgid_in, msgid_out;

  key_in = ftok("in", 65);
  key_out = ftok("out", 65);

  msgid_in = msgget(key_in, 0666 | IPC_CREAT);
  msgid_out = msgget(key_out, 0666 | IPC_CREAT);
  message.mesg_type = 1;

  std::cout << "Enter polish word" << std::endl;
  std::cin >> message.mesg_text;

  for (int i = 0; i < 5; i++) {
    pid_t pid = fork();
    if (pid == 0) {
      message.sender = getpid();
      msgsnd(msgid_in, &message, sizeof(message), 0);
      msgrcv(msgid_out, &message, sizeof(message), getpid(), 0);
      std::cout << "Server response: " << message.mesg_text << std::endl;
      return 0;
    }
  }

  for (int i = 0; i < 5; i++) {
    wait(NULL);
  }

  return 0;
}

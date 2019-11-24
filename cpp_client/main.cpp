#include <zmqpp/zmqpp.hpp>
#include <string>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]) {
  const string endpoint = "tcp://localhost:8080";

  // initialize the 0MQ context
  zmqpp::context context;

  // generate a push socket
  zmqpp::socket_type type = zmqpp::socket_type::subscribe;
  zmqpp::socket socket (context, type);

  socket.subscribe("42");

  // open the connection
  cout << "Opening connection to " << endpoint << "..." << endl;
  socket.connect(endpoint);
  while(true) {
    zmqpp::message message;
    socket.receive(message);

    // Read as a string
    string text;
    message >> text;

    cout << "[RECV] " <<  text << "\n" << endl;
  }
}

import socket
from contextlib import closing


class Connection:
    def __init__(self, port, bind_or_connect):
        self.port = port
        self.s = None
        self.bind_or_connect = bind_or_connect

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._bind_or_connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.s.close()

    def _bind_or_connect(self):
        if self.bind_or_connect == "bind":
            self.s.bind(("", self.port))
        elif self.bind_or_connect == "connect":
            self.s.connect(("", self.port))

    def wait_for_connections_and_receive_command_and_query(self, listen_number=1):
        self.s.listen(1)
        while True:
            con, addr = self.s.accept()
            command_and_query = con.recv(1024).decode().split(" ")
            command, query = command_and_query[0], " ".join(command_and_query[1:])
            yield command, query, con

    def recv(self, num=1024):
        return self.s.recv(num)

    def receive(self, num=1024):
        return self.s.recv(num).decode()

    def sendall(self, userinput):
        self.s.sendall(userinput.as_byte_string)

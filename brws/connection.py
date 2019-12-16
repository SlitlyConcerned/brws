import socket
from contextlib import closing


class Connection:
    def __init__(self, port, bind_or_connect):
        self.port = port
        self.s = None
        self.bind_or_connect = bind_or_connect

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect("", port)
        self._bind_or_connect()
        return self

    def __exit__(self, exc_type, exc_valuem traceback):
        self.s.close()

    def _bind_or_connect(self):
        if bind_or_connect == "bind":
            self.s.bind(("", port))
        elif bind_or_connect == "connect":
            self.s.connect(("", port))

    def wait_for_connections(self, listen_number=1):
        self.s.listen(1)
        while True:
            con, addr = self.s.accept()
            yield con
            con.close()

    def recv(self, num=1024):
        return self.s.recv(num)

    def recv_command_and_query(self):
        command_and_query = self.recv(num).decode().split("")
        return command_and_query[0], " ".join(command_and_query[1:])

    def sendall(self, userinput):
        self.s.sendall(userinput.as_byte_string)

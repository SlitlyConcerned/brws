import os
import socket
import sys
from contextlib import closing, contextmanager

from selenium import webdriver


@contextmanager
def start_browser(driver_name, wait=10):
    driver = getattr(webdriver, driver_name)()
    if driver is None:
        raise NameError(f"No driver called '{driver_name}'")
    yield driver
    driver.close()


def run_command_with_conn(conn, driver, commandlist, argv):
    with conn:
        while True:
            argv = conn.recv(1024).decode().split("%ws%")
            print(argv)
            if not argv or not argv[0]:
                break

            command_name = argv[0]
            args = argv[1:]

            print(f"Running command: {command_name}\n\twith aruments: {args}")
            try:
                commandlist[argv[0]](driver, *argv[1:])
            except Exception as e:
                print(e)


def br_serve(driver, commandlist, port):
    with start_browser(driver) as browser:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as ss:
            ss.bind(("", port))
            ss.listen(1)
            while True:
                conn, addr = ss.accept()
                run_command_with_conn(conn, browser, commandlist, port)


def bytesargv():
    return list(map(os.fsencode, sys.argv))


def br_command(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect(("", port))
        command = bytesargv()[1:]
        command_bytes = b"%ws%".join(command)
        print(command_bytes)
        s.sendall(command_bytes)


def br(driver, port, commands):
    print(sys.argv)
    if sys.argv[1] == "serve":
        br_serve(driver, commands, port)
    else:
        br_command(port)

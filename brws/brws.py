import os
import signal
import socket
import subprocess
import sys
from contextlib import closing, contextmanager
from pprint import pprint

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
            argv = conn.recv(1024).decode().split(" ")
            if not argv or not argv[0]:
                break

            command_name = argv[0]
            q = " ".join(argv[1:])

            print(f"Running command: {command_name}\n\twith query: {q}")
            try:
                result = commandlist[command_name](driver, q)
                return result
            except Exception as e:
                print(e)


def serve(driver, commandlist, port):
    with start_browser(driver) as browser:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as ss:
            ss.bind(("", port))
            ss.listen(1)
            while True:
                conn, addr = ss.accept()
                run_command_with_conn(conn, browser, commandlist, port)


def bytesargv():
    return list(map(os.fsencode, sys.argv))


def command(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect(("", port))
        command = bytesargv()[1:]
        command_bytes = b" ".join(command)
        s.sendall(command_bytes)


def run(driver, port, commands):
    if sys.argv[1] == "serve":
        serve(driver, commands, port)
        return
    if sys.argv[1] == "commands":
        pprint(commands)
    else:
        result = command(port)
        if result:
            print(result)

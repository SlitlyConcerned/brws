import os
import signal
import socket
import subprocess
import sys
from contextlib import closing, contextmanager
from pprint import pprint

from prompt_toolkit import PromptSession
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
        argv = conn.recv(1024).decode().split(" ")
        if not argv or not argv[0]:
            return

        command_name = argv[0]
        q = " ".join(argv[1:])

        print(f"Running command: {command_name}\n\twith query: {q}")
        try:
            return commandlist[command_name](driver, q)
        except Exception as e:
            print(e)


def serve(driver, commandlist, port):
    with start_browser(driver) as browser:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as ss:
            ss.bind(("", port))
            ss.listen(1)
            while True:
                conn, addr = ss.accept()
                result = run_command_with_conn(conn, browser, commandlist, port)
                if result:
                    if isinstance(result, str):
                        result = result.encode()
                    ss.sendall(result)


def list_to_bytes(los):
    return list(map(os.fsencode, los))


def command(port, args=None):
    if args is None:
        args = sys.argv[1:]
    if args == [""]:
        return
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.connect(("", port))
        command = list_to_bytes(args)
        command_bytes = b" ".join(command)
        s.sendall(command_bytes)
        result = s.recv(1024).decode()
        if result:
            print(result)


def run(driver, port, commands):
    if sys.argv[1] == "serve":
        serve(driver, commands, port)
        return
    if sys.argv[1] == "commands":
        pprint(commands)
    if sys.argv[1] == "shell":
        session = PromptSession()
        while True:
            command(port, session.prompt(":").split(" "))
    else:
        print("Waiting for the response...")
        command(port)
        print("Done.")

import os
import signal
import socket
import subprocess
import sys
from contextlib import closing, contextmanager
from pprint import pprint

from prompt_toolkit import PromptSession
from selenium import webdriver

import command
from connection import Connection
from userrinput import UserInput


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
        with Connection(port, "bind") as connection:
            for con in connection.wait_for_connections():
                command, query = con.recv_command_and_query()
                print(f"Running command: {command}\n\twith query: {query}")
                try:
                    return commandlist[command](driver, query)
                except Exception as e:
                    print(e)


def command(port, userinput=None):
    with Connection(port, "connect") as connection:
        connection.sendall(userinput)
        result = connection.receive()
        if result:
            print(result)


def run(driver, port, commands):
    if sys.argv[1] == "serve":
        serve(driver, commands, port)
        return
    if sys.argv[1] == "commands":
        command.print_commands(commands)
        return
    if sys.argv[1] == "shell":
        session = PromptSession()
        while True:
            userinput = UserInput(session.prompt(":"))
            command(port, userinput)
    else:
        print("Waiting for the response...")
        command(port, UserInput(sys.argv[1:]))
        print("Done.")

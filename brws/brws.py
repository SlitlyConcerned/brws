import os
import signal
import socket
import subprocess
import sys
from contextlib import closing, contextmanager
from pprint import pprint

from prompt_toolkit import PromptSession
from selenium import webdriver

from .command import print_commands
from .connection import Connection
from .userinput import UserInput


@contextmanager
def start_browser(driver_name, wait=10):
    driver = getattr(webdriver, driver_name)()
    if driver is None:
        raise NameError(f"No driver called '{driver_name}'")
    yield driver
    driver.close()


def serve(driver, commandlist, port):
    with start_browser(driver) as browser:
        with Connection(port, "bind") as connection:
            for command, query ,con in connection.wait_for_connections_and_receive_command_and_query():
                print(f"Running command: {command}\n\twith query: {query}")
                try:
                    result = commandlist[command](browser, query)
                    if result:
                        con.sendall(result.encode())
                except Exception as e:
                    print(e)
                con.close()


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

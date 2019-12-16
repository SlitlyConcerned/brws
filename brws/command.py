from . import doc


def print_command(command):
    command_name, function = command
    print(command_name + ": ", end="")
    doc.print_function(function, if_none="No Documentation")


def print_commands(commands):
    for command in commands:
        print(command)

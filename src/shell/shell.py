import socket
import getpass

from parser import parse_command


class Shell:
    def __init__(self) -> None:
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()

    def prompt(self) -> str:
        return f"{self.username}@{self.hostname}:~$ "

    def run(self) -> None:
        while True:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break

            command, args = parse_command(line)

            if not command:
                continue

            if command == "exit":
                break

            self.execute(command, args)

    def execute(self, command: str, args: list[str]) -> None:
        if command == "ls":
            self.command_ls(args)
        elif command == "cd":
            self.command_cd(args)
        else:
            print(f"Unknown command: {command}")

    def command_ls(self, args: list[str]) -> None:
        if args:
            print("ls: arguments are not implemented yet")
        else:
            print("ls: not implemented yet")

    def command_cd(self, args: list[str]) -> None:
        if len(args) > 1:
            print("cd: too many arguments")
        elif not args:
            print("cd: not implemented yet")
        else:
            print(f"cd: not implemented yet: {args[0]}")
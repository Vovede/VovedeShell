import socket
import getpass

from shell.parser import parse_command


class Shell:
    def __init__(self, vfs=None) -> None:
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs = vfs

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
        elif command == "vfs-init":
            self.command_vfs_init(args)
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

    def command_vfs_init(self, args: list[str]) -> None:
        """Initialize default virtual file system."""
        if args:
            print("vfs-init: arguments are not supported")
            return

        from shell.vfs import VFS

        self.vfs = VFS.create_default_vfs()
        print("VFS initialized")

    def run_script(self, path: str) -> None:
        """Execute commands from a script file."""
        from shell.script import read_script

        for command_line in read_script(path):
            print(f"$ {command_line}")
            command, args = parse_command(command_line)

            if command == "exit":
                break

            self.execute(command, args)
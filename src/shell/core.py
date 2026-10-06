import socket
import getpass
import time

from shell.parser import parse_command


class Shell:
    def __init__(self, vfs=None) -> None:
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs = vfs
        self.current_path = "/"
        self.start_time = time.monotonic()

    def prompt(self) -> str:
        return f"{self.username}@{self.hostname}:{self.current_path}$ "

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
        elif command == "whoami":
            self.command_whoami(args)
        elif command == "uptime":
            self.command_uptime(args)
        elif command == "vfs-init":
            self.command_vfs_init(args)
        else:
            print(f"Unknown command: {command}")

    def command_ls(self, args: list[str]) -> None:
        """List files and directories in a VFS directory."""
        if len(args) > 1:
            print("ls: too many arguments")
            return

        if self.vfs is None:
            print("ls: VFS is not loaded")
            return

        path = args[0] if args else self.current_path

        try:
            node = self.vfs.get_node(path)
        except ValueError as error:
            print(f"ls: {error}")
            return

        if node.get("type") != "directory":
            print("ls: VFS path is not a directory")
            return

        for name in node.get("children", {}):
            print(name)

    def get_parent_path(self, path: str) -> str:
        """Return parent directory path."""
        if path == "/":
            return "/"

        parent = path.rstrip("/").rsplit("/", 1)[0]

        return parent or "/"

    def command_cd(self, args: list[str]) -> None:
        """Change current VFS directory."""
        if len(args) > 1:
            print("cd: too many arguments")
            return

        if not args:
            print("cd: path is required")
            return

        if self.vfs is None:
            print("cd: VFS is not loaded")
            return

        path = args[0]

        if path == ".":
            return

        if path == "..":
            self.current_path = self.get_parent_path(
                self.current_path
            )
            return

        if not path.startswith("/"):
            if self.current_path == "/":
                path = "/" + path
            else:
                path = self.current_path.rstrip("/") + "/" + path

        try:
            node = self.vfs.get_node(path)
        except ValueError as error:
            print(f"cd: {error}")
            return

        if node.get("type") != "directory":
            print("cd: VFS path is not a directory")
            return

        self.current_path = path

    def command_whoami(self, args: list[str]) -> None:
        """Print current username."""
        if args:
            print("whoami: arguments are not supported")
            return

        print(self.username)

    def command_uptime(self, args: list[str]) -> None:
        """Show shell uptime."""
        if args:
            print("uptime: arguments are not supported")
            return

        elapsed = time.monotonic() - self.start_time
        print(f"up {int(elapsed)} seconds")

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
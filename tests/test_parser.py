from src.shell.parser import parse_command


def test_parse_command_without_arguments():
    command, args = parse_command("ls")

    assert command == "ls"
    assert args == []


def test_parse_command_with_arguments():
    command, args = parse_command("cd home")

    assert command == "cd"
    assert args == ["home"]


def test_parse_command_with_multiple_arguments():
    command, args = parse_command("ls -l /home")

    assert command == "ls"
    assert args == ["-l", "/home"]


def test_parse_command_ignores_extra_spaces():
    command, args = parse_command("  ls   -l   /home  ")

    assert command == "ls"
    assert args == ["-l", "/home"]


def test_parse_empty_command():
    command, args = parse_command("")

    assert command == ""
    assert args == []

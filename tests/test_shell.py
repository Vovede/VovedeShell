from shell.core import Shell


def test_shell_has_username():
    shell = Shell()

    assert shell.username


def test_shell_has_hostname():
    shell = Shell()

    assert shell.hostname


def test_prompt_contains_username_and_hostname():
    shell = Shell()

    prompt = shell.prompt()

    assert shell.username in prompt
    assert shell.hostname in prompt
    assert prompt.endswith(":~$ ")


def test_ls_stub(capsys):
    shell = Shell()

    shell.execute("ls", [])

    captured = capsys.readouterr()

    assert captured.out == "ls: not implemented yet\n"


def test_cd_stub(capsys):
    shell = Shell()

    shell.execute("cd", [])

    captured = capsys.readouterr()

    assert captured.out == "cd: not implemented yet\n"


def test_unknown_command(capsys):
    shell = Shell()

    shell.execute("unknown", [])

    captured = capsys.readouterr()

    assert captured.out == "Unknown command: unknown\n"


def test_cd_with_too_many_arguments(capsys):
    shell = Shell()

    shell.execute("cd", ["one", "two"])

    captured = capsys.readouterr()

    assert captured.out == "cd: too many arguments\n"

def test_run_script(capsys, tmp_path):
    script = tmp_path / "test.txt"

    script.write_text("ls\n"
                      "unknown",
                      encoding="utf-8")

    shell = Shell()
    shell.run_script(str(script))

    captured = capsys.readouterr()

    assert captured.out == (
        "$ ls\n"
        "ls: not implemented yet\n"
        "$ unknown\n"
        "Unknown command: unknown\n"
    )
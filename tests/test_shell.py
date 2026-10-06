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
    assert prompt.endswith(":/$ ")


def test_ls_without_vfs(capsys):
    shell = Shell()

    shell.execute("ls", [])

    captured = capsys.readouterr()

    assert captured.out == "ls: VFS is not loaded\n"


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
        "ls: VFS is not loaded\n"
        "$ unknown\n"
        "Unknown command: unknown\n"
    )

def test_whoami(capsys):
    shell = Shell()

    shell.execute("whoami", [])

    captured = capsys.readouterr()

    assert captured.out == f"{shell.username}\n"

def test_uptime(capsys):
    shell = Shell()

    shell.execute("uptime", [])

    captured = capsys.readouterr()

    assert captured.out.startswith("up ")
    assert captured.out.endswith(" seconds\n")

def test_cp_relative_destination(capsys):
    from shell.core import Shell
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "home": {
                "type": "directory",
                "children": {
                    "user.txt": {
                        "type": "file",
                        "content": "Hello",
                    },
                },
            },
        },
    })

    shell = Shell(vfs)
    shell.current_path = "/home"

    shell.execute(
        "cp",
        ["/home/user.txt", "copy.txt"],
    )

    shell.command_ls(["/home"])

    captured = capsys.readouterr()

    assert "user.txt\n" in captured.out
    assert "copy.txt\n" in captured.out


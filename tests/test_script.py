from shell.script import read_script


def test_read_script_ignores_comments_and_empty_lines(tmp_path):
    script = tmp_path / "test.txt"

    script.write_text(
        "# comment\n"
        "\n"
        "ls\n"
        "  \n"
        "# another comment\n"
        "cd home\n",
        encoding="utf-8",
    )

    commands = read_script(str(script))

    assert commands == ["ls", "cd home"]
from shell.vfs import VFS


def test_empty_vfs():
    vfs = VFS()

    assert vfs.data == {
        "type": "directory",
        "children": {},
    }


def test_load_vfs(tmp_path):
    vfs_file = tmp_path / "vfs.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test.txt": {"type": "file", "content": "Hello"}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    assert vfs.data["type"] == "directory"
    assert "test.txt" in vfs.data["children"]
    assert vfs.data["children"]["test.txt"]["content"] == "Hello"


def test_missing_vfs_file(tmp_path):
    vfs_file = tmp_path / "missing.json"

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS file not found"
    else:
        assert False


def test_invalid_vfs_json(tmp_path):
    vfs_file = tmp_path / "invalid.json"
    vfs_file.write_text("{invalid}", encoding="utf-8")

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "Invalid VFS JSON"
    else:
        assert False

def test_create_default_vfs():
    vfs = VFS.create_default_vfs()

    assert vfs.data["type"] == "directory"

    children = vfs.data["children"]

    assert "home" in children
    assert children["home"]["type"] == "directory"

    assert "readme.txt" in children
    assert children["readme.txt"]["type"] == "file"
    assert children["readme.txt"]["content"] == "VovedeShell VFS"

def test_vfs_init_replaces_vfs():
    from shell.core import Shell

    shell = Shell(
        VFS({
            "type": "directory",
            "children": {
                "old.txt": {
                    "type": "file",
                    "content": "old",
                },
            },
        })
    )

    shell.command_vfs_init([])

    children = shell.vfs.data["children"]

    assert "old.txt" not in children
    assert "home" in children
    assert "readme.txt" in children

def test_vfs_init_does_not_create_physical_files(tmp_path):
    from shell.core import Shell

    shell = Shell()
    shell.command_vfs_init([])

    assert list(tmp_path.iterdir()) == []

def test_invalid_vfs_root_type(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "file", "children": {}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS root must be a directory"
    else:
        assert False


def test_invalid_vfs_children(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": []}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS children must be an object"
    else:
        assert False

def test_invalid_vfs_node_type(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test": {"type": "unknown"}}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "Invalid VFS node type"
    else:
        assert False


def test_invalid_vfs_file_without_content(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test": {"type": "file"}}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS file must have content"
    else:
        assert False

def test_nested_vfs_structure(tmp_path):
    vfs_file = tmp_path / "nested.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"home": {"type": "directory", "children": {'
        '"docs": {"type": "directory", "children": {'
        '"test.txt": {"type": "file", "content": "Hello"}}}}}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    docs = vfs.data["children"]["home"]["children"]["docs"]
    file_node = docs["children"]["test.txt"]

    assert docs["type"] == "directory"
    assert file_node["type"] == "file"
    assert file_node["content"] == "Hello"

def test_invalid_vfs_node_object(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test": "invalid"}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS node must be an object"
    else:
        assert False

def test_invalid_vfs_directory_without_children(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"home": {"type": "directory"}}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS directory children must be an object"
    else:
        assert False

def test_invalid_vfs_file_content(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test.txt": {"type": "file", "content": {}}}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "VFS file content must be a string"
    else:
        assert False

def test_base64_file_content(tmp_path):
    vfs_file = tmp_path / "binary.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"image.bin": {'
        '"type": "file", '
        '"encoding": "base64", '
        '"content": "SGVsbG8="'
        '}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    file_node = vfs.data["children"]["image.bin"]

    assert file_node["encoding"] == "base64"
    assert file_node["content"] == "SGVsbG8="

def test_invalid_base64_content(tmp_path):
    vfs_file = tmp_path / "invalid.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"image.bin": {'
        '"type": "file", '
        '"encoding": "base64", '
        '"content": "not-base64!!!"'
        '}}}',
        encoding="utf-8",
    )

    try:
        VFS.from_json(str(vfs_file))
    except ValueError as error:
        assert str(error) == "Invalid Base64 content"
    else:
        assert False

def test_get_base64_file_content(tmp_path):
    vfs_file = tmp_path / "binary.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"image.bin": {'
        '"type": "file", '
        '"encoding": "base64", '
        '"content": "SGVsbG8="'
        '}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    assert vfs.get_file_content("/image.bin") == b"Hello"

def test_get_text_file_content(tmp_path):
    vfs_file = tmp_path / "text.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test.txt": {'
        '"type": "file", '
        '"content": "Hello from VFS!"'
        '}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    assert vfs.get_file_content("/test.txt") == b"Hello from VFS!"

def test_get_missing_file(tmp_path):
    vfs_file = tmp_path / "vfs.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    try:
        vfs.get_file_content("/missing.txt")
    except ValueError as error:
        assert str(error) == "VFS path not found"
    else:
        assert False

def test_get_directory_as_file(tmp_path):
    vfs_file = tmp_path / "vfs.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"home": {"type": "directory", "children": {}}}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    try:
        vfs.get_file_content("/home")
    except ValueError as error:
        assert str(error) == "VFS path is not a file"
    else:
        assert False

def test_get_root_as_file(tmp_path):
    vfs_file = tmp_path / "vfs.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {}}',
        encoding="utf-8",
    )

    vfs = VFS.from_json(str(vfs_file))

    try:
        vfs.get_file_content("/")
    except ValueError as error:
        assert str(error) == "VFS path is not a file"
    else:
        assert False

def test_load_vfs_does_not_create_files(tmp_path):
    vfs_file = tmp_path / "vfs.json"

    vfs_file.write_text(
        '{"type": "directory", "children": {'
        '"test.txt": {"type": "file", "content": "Hello"}}}',
        encoding="utf-8",
    )

    VFS.from_json(str(vfs_file))

    assert not (tmp_path / "test.txt").exists()

def test_vfs_init_rejects_arguments(capsys):
    from shell.core import Shell

    shell = Shell()

    shell.command_vfs_init(["test"])

    captured = capsys.readouterr()

    assert captured.out == (
        "vfs-init: arguments are not supported\n"
    )
    assert shell.vfs is None

def test_ls_root(capsys):
    from shell.core import Shell
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "home": {
                "type": "directory",
                "children": {},
            },
            "readme.txt": {
                "type": "file",
                "content": "Hello",
            },
        },
    })

    shell = Shell(vfs)
    shell.command_ls([])

    captured = capsys.readouterr()

    assert captured.out == "home\nreadme.txt\n"

def test_ls_directory(capsys):
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
                    "notes.txt": {
                        "type": "file",
                        "content": "Notes",
                    },
                },
            },
        },
    })

    shell = Shell(vfs)
    shell.command_ls(["/home"])

    captured = capsys.readouterr()

    assert captured.out == "user.txt\nnotes.txt\n"

def test_copy_file():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "source.txt": {
                "type": "file",
                "content": "Hello",
            },
        },
    })

    vfs.copy_file("/source.txt", "/copy.txt")

    assert vfs.get_file_content("/copy.txt") == b"Hello"

def test_copy_directory_fails():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "home": {
                "type": "directory",
                "children": {},
            },
        },
    })

    try:
        vfs.copy_file("/home", "/copy")
    except ValueError as error:
        assert str(error) == "VFS path is not a file"
    else:
        assert False

def test_copy_missing_file_fails():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {},
    })

    try:
        vfs.copy_file("/missing.txt", "/copy.txt")
    except ValueError as error:
        assert str(error) == "VFS path not found"
    else:
        assert False

def test_copy_to_missing_directory_fails():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "source.txt": {
                "type": "file",
                "content": "Hello",
            },
        },
    })

    try:
        vfs.copy_file("/source.txt", "/missing/copy.txt")
    except ValueError as error:
        assert str(error) == "VFS path not found"
    else:
        assert False

def test_copy_file_overwrites_existing():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "source.txt": {
                "type": "file",
                "content": "New",
            },
            "copy.txt": {
                "type": "file",
                "content": "Old",
            },
        },
    })

    vfs.copy_file("/source.txt", "/copy.txt")

    assert vfs.get_file_content("/copy.txt") == b"New"

def test_cp_relative_source():
    from shell.vfs import VFS
    from shell.core import Shell

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

    shell.execute("cp", ["user.txt", "copy3.txt"])

    assert vfs.get_file_content("/home/copy3.txt") == b"Hello"

def test_cp_missing_destination_directory(capsys):
    from shell.vfs import VFS
    from shell.core import Shell

    vfs = VFS({
        "type": "directory",
        "children": {
            "source.txt": {
                "type": "file",
                "content": "Hello",
            },
        },
    })

    shell = Shell(vfs)
    shell.execute("cp", ["/source.txt", "/missing/copy.txt"])

    assert capsys.readouterr().out == (
        "cp: VFS path not found\n"
    )

def test_cp_directory_fails(capsys):
    from shell.vfs import VFS
    from shell.core import Shell

    vfs = VFS({
        "type": "directory",
        "children": {
            "home": {
                "type": "directory",
                "children": {},
            },
        },
    })

    shell = Shell(vfs)
    shell.execute("cp", ["/home", "/copy"])

    assert capsys.readouterr().out == (
        "cp: VFS path is not a file\n"
    )

def test_cp_invalid_arguments(capsys):
    from shell.vfs import VFS
    from shell.core import Shell

    shell = Shell(VFS())

    shell.execute("cp", [])

    assert capsys.readouterr().out == (
        "cp: expected source and destination\n"
    )

def test_cp_does_not_change_source():
    from shell.vfs import VFS

    vfs = VFS({
        "type": "directory",
        "children": {
            "source.txt": {
                "type": "file",
                "content": "Original",
            },
        },
    })

    vfs.copy_file("/source.txt", "/copy.txt")

    assert vfs.get_file_content("/source.txt") == b"Original"
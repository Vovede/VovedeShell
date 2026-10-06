import json
import base64


def validate_node(node: dict) -> None:
    """Validate a VFS node."""
    if not isinstance(node, dict):
        raise ValueError("VFS node must be an object")

    node_type = node.get("type")

    if node_type not in ("file", "directory"):
        raise ValueError("Invalid VFS node type")

    if node_type == "file":
        if "content" not in node:
            raise ValueError("VFS file must have content")

        if not isinstance(node["content"], str):
            raise ValueError("VFS file content must be a string")

        if node.get("encoding") == "base64":
            try:
                base64.b64decode(
                    node["content"],
                    validate=True,
                )
            except ValueError as error:
                raise ValueError("Invalid Base64 content") from error

        return

    children = node.get("children")

    if not isinstance(children, dict):
        raise ValueError("VFS directory children must be an object")

    for child in children.values():
        validate_node(child)


class VFS:
    """In-memory virtual file system."""

    def __init__(self, data: dict | None = None) -> None:
        self.data = data or {"type": "directory", "children": {}}

    @classmethod
    def from_json(cls, path: str) -> "VFS":
        """Load VFS from a JSON file."""
        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise ValueError("VFS file not found") from error
        except json.JSONDecodeError as error:
            raise ValueError("Invalid VFS JSON") from error

        if not isinstance(data, dict):
            raise ValueError("VFS root must be an object")

        if data.get("type") != "directory":
            raise ValueError("VFS root must be a directory")

        if not isinstance(data.get("children"), dict):
            raise ValueError("VFS children must be an object")

        for node in data["children"].values():
            validate_node(node)

        return cls(data)

    def get_file_content(self, path: str) -> bytes:
        """Return file content as bytes."""
        parts = path.strip("/").split("/") if path.strip("/") else []
        node = self.data

        for part in parts:
            if not isinstance(node, dict):
                raise ValueError("VFS path not found")

            children = node.get("children", {})

            if part not in children:
                raise ValueError("VFS path not found")

            node = children[part]

        if node.get("type") != "file":
            raise ValueError("VFS path is not a file")

        content = node["content"]

        if node.get("encoding") == "base64":
            return base64.b64decode(content)

        return content.encode("utf-8")

    def get_node(self, path: str) -> dict:
        """Return a VFS node by path."""
        parts = path.strip("/").split("/") if path.strip("/") else []
        node = self.data

        for part in parts:
            if not isinstance(node, dict):
                raise ValueError("VFS path not found")

            children = node.get("children", {})

            if part not in children:
                raise ValueError("VFS path not found")

            node = children[part]

        return node

    @classmethod
    def create_default_vfs(cls) -> "VFS":
        """Create default VFS from VFS root directory."""
        return cls({
            "type": "directory",
            "children": {
                "home": {
                    "type": "directory",
                    "children": {},
                },
                "readme.txt": {
                    "type": "file",
                    "content": "VovedeShell VFS",
                },
            },
        })
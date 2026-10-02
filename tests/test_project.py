import subprocess
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


class ProjectStructureTests(unittest.TestCase):
    def test_required_directories_exist(self) -> None:
        for directory in ("src", "tests", "data", "scripts"):
            with self.subTest(directory=directory):
                self.assertTrue((ROOT_DIR / directory).is_dir())

    def test_required_files_exist(self) -> None:
        files = ("README.md", ".gitignore", "Makefile", "run.sh")
        for filename in files:
            with self.subTest(filename=filename):
                self.assertTrue((ROOT_DIR / filename).is_file())

    def test_application_starts(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "shell.main"],
            cwd=ROOT_DIR,
            env={"PYTHONPATH": str(ROOT_DIR / "src")},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("scaffold", result.stdout)


if __name__ == "__main__":
    unittest.main()

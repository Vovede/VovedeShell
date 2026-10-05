from shell.core import Shell
from shell.config import parse_args
from shell.vfs import VFS


def main() -> None:
    args = parse_args()

    vfs = None

    if args.vfs:
        from shell.vfs import VFS

        try:
            vfs = VFS.from_json(args.vfs)
        except ValueError as error:
            print(f"VFS error: {error}")
            return

    shell = Shell(vfs)

    if args.script:
        shell.run_script(args.script)
    else:
        shell.run()


if __name__ == "__main__":
    main()
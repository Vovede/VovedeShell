from shell.core import Shell
from shell.config import parse_args


def main() -> None:
    args = parse_args()
    shell = Shell()

    if args.script:
        shell.run_script(args.script)
    else:
        shell.run()


if __name__ == "__main__":
    main()
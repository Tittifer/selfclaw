import argparse

from selfclaw import __version__
from selfclaw.config import load_config, save_config


def run_version():
    print(f"SelfClaw {__version__}")


def run_chat():
    print("Chat mode is not implemented yet.")


def run_config_show():
    config = load_config()

    for key, value in config.items():
        print(f"{key}: {value}")


def run_config_set(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

    print(f"Set {key} = {value}")


def main():
    parser = argparse.ArgumentParser(prog="selfclaw")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("version")
    subparsers.add_parser("chat")

    config_parser = subparsers.add_parser("config")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    config_subparsers.add_parser("show")

    config_set_parser = config_subparsers.add_parser("set")
    config_set_parser.add_argument("key")
    config_set_parser.add_argument("value")

    args = parser.parse_args()

    if args.command == "version":
        run_version()
    elif args.command == "chat":
        run_chat()
    elif args.command == "config":
        if args.config_command == "show":
            run_config_show()
        elif args.config_command == "set":
            run_config_set(args.key, args.value)
        else:
            parser.print_help()
    else:
        parser.print_help()
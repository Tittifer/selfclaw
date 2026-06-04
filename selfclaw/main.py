import argparse

from selfclaw import __version__
from selfclaw.config import load_config, save_config
from selfclaw.llm import create_llm_client
from selfclaw.agent import Agent
from selfclaw.memory import add_memory, search_memory


def run_version():
    print(f"SelfClaw {__version__}")


def run_chat(session_id):
    config = load_config()
    llm = create_llm_client(config)
    agent = Agent(llm, session_id=session_id)

    print(f"SelfClaw chat started. Session: {session_id}. Type 'exit' to quit.")

    while True:
        user_text = input("You: ")

        if user_text == "exit":
            print("Bye.")
            break

        reply = agent.chat(user_text)
        print(f"SelfClaw: {reply}")


def run_config_show():
    config = load_config()

    for key, value in config.items():
        print(f"{key}: {value}")


def run_config_set(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

    print(f"Set {key} = {value}")


def run_memory_add(text):
    add_memory(text)
    print("Memory added.")


def run_memory_search(query):
    results = search_memory(query)

    if not results:
        print("No memories found.")
        return

    for result in results:
        print(result)


def main():
    parser = argparse.ArgumentParser(prog="selfclaw")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("version")
    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("--session", default="default")

    config_parser = subparsers.add_parser("config")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    config_subparsers.add_parser("show")

    config_set_parser = config_subparsers.add_parser("set")
    config_set_parser.add_argument("key")
    config_set_parser.add_argument("value")

    memory_parser = subparsers.add_parser("memory")
    memory_subparsers = memory_parser.add_subparsers(dest="memory_command")

    memory_add_parser = memory_subparsers.add_parser("add")
    memory_add_parser.add_argument("text")

    memory_search_parser = memory_subparsers.add_parser("search")
    memory_search_parser.add_argument("query")

    args = parser.parse_args()

    if args.command == "version":
        run_version()
    elif args.command == "chat":
        run_chat(args.session)
    elif args.command == "config":
        if args.config_command == "show":
            run_config_show()
        elif args.config_command == "set":
            run_config_set(args.key, args.value)
        else:
            parser.print_help()
    elif args.command == "memory":
        if args.memory_command == "add":
            run_memory_add(args.text)
        elif args.memory_command == "search":
            run_memory_search(args.query)
        else:
            parser.print_help()
    else:
        parser.print_help()
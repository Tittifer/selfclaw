import argparse

from selfclaw import __version__
from selfclaw.config import ALLOWED_CONFIG_KEYS, load_config, parse_config_value, save_config
from selfclaw.llm import create_llm_client
from selfclaw.memory import add_memory, clear_memories, load_memories, search_memory
from selfclaw.session_store import clear_session, list_sessions, load_session
from selfclaw.session_manager import SessionManager
from selfclaw.persona import load_persona, reset_persona, save_persona


def run_version():
    print(f"SelfClaw {__version__}")


def safe_load_config():
    try:
        return load_config()
    except ValueError as error:
        print(f"Error: {error}")
        return None


def run_chat(session_id):
    config = safe_load_config()

    if config is None:
        return

    try:
        llm = create_llm_client(config)
    except ValueError as error:
        print(f"Error: {error}")
        return

    memory_limit = int(config["memory_limit"])

    session_manager = SessionManager(llm, memory_limit=memory_limit)

    print(f"SelfClaw chat started. Session: {session_id}. Type 'exit' to quit.")

    while True:
        user_text = input("You: ")

        if user_text == "exit":
            print("Bye.")
            break

        try:
            reply = session_manager.chat(session_id, user_text)
        except RuntimeError as error:
            print(f"Error: {error}")
            continue

        print(f"SelfClaw: {reply}")


def format_config_value(key, value):
    if key == "api_key" and value:
        return "********"

    return value


def run_config_show():
    config = safe_load_config()

    if config is None:
        return

    for key, value in config.items():
        display_value = format_config_value(key, value)
        print(f"{key}: {display_value}")


def run_config_sources():
    print("Config sources, low to high priority:")
    print("1. DEFAULT_CONFIG in selfclaw/config.py")
    print("2. selfclaw.json")
    print("3. .env / system environment variables")


def run_config_set(key, value):
    if key not in ALLOWED_CONFIG_KEYS:
        allowed = ", ".join(sorted(ALLOWED_CONFIG_KEYS))
        print(f"Invalid config key: {key}")
        print(f"Allowed keys: {allowed}")
        return

    try:
        parsed_value = parse_config_value(key, value)
    except ValueError as error:
        print(f"Error: {error}")
        return

    config = safe_load_config()

    if config is None:
        return
    
    config[key] = parsed_value
    save_config(config)

    print(f"Set {key} = {parsed_value}")


def run_memory_add(text):
    added = add_memory(text)

    if added:
        print("Memory added.")
    else:
        print("Memory already exists.")


def run_memory_search(query, limit):
    results = search_memory(query, limit=limit)

    if not results:
        print("No memories found.")
        return

    for result in results:
        print(result)


def run_memory_list():
    memories = load_memories()

    if not memories:
        print("No memories found.")
        return

    for memory in memories:
        print(memory.strip())


def run_memory_clear():
    clear_memories()
    print("Memories cleared.")


def run_session_list():
    sessions = list_sessions()

    if not sessions:
        print("No sessions found.")
        return

    for session_id in sessions:
        print(session_id)


def run_session_show(session_id):
    messages = load_session(session_id)

    if not messages:
        print(f"No messages found for session: {session_id}")
        return

    for message in messages:
        role = message["role"]
        content = message["content"]
        print(f"{role}: {content}")


def run_session_clear(session_id):
    cleared = clear_session(session_id)

    if cleared:
        print(f"Session cleared: {session_id}")
    else:
        print(f"Session not found: {session_id}")


def run_persona_show():
    print(load_persona())


def run_persona_set(text):
    save_persona(text)
    print("Persona updated.")


def run_persona_reset():
    reset_persona()
    print("Persona reset.")


def main():
    parser = argparse.ArgumentParser(prog="selfclaw")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("version")
    chat_parser = subparsers.add_parser("chat")
    chat_parser.add_argument("--session", default="default")

    config_parser = subparsers.add_parser("config")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    config_subparsers.add_parser("show")
    config_subparsers.add_parser("sources")

    config_set_parser = config_subparsers.add_parser("set")
    config_set_parser.add_argument("key")
    config_set_parser.add_argument("value")

    memory_parser = subparsers.add_parser("memory")
    memory_subparsers = memory_parser.add_subparsers(dest="memory_command")

    memory_add_parser = memory_subparsers.add_parser("add")
    memory_add_parser.add_argument("text")

    memory_search_parser = memory_subparsers.add_parser("search")
    memory_search_parser.add_argument("query")
    memory_search_parser.add_argument("--limit", type=int, default=5)

    memory_subparsers.add_parser("list")
    memory_subparsers.add_parser("clear")

    session_parser = subparsers.add_parser("session")
    session_subparsers = session_parser.add_subparsers(dest="session_command")

    session_subparsers.add_parser("list")

    session_show_parser = session_subparsers.add_parser("show")
    session_show_parser.add_argument("session_id")

    session_clear_parser = session_subparsers.add_parser("clear")
    session_clear_parser.add_argument("session_id")

    persona_parser = subparsers.add_parser("persona")
    persona_subparsers = persona_parser.add_subparsers(dest="persona_command")

    persona_subparsers.add_parser("show")

    persona_set_parser = persona_subparsers.add_parser("set")
    persona_set_parser.add_argument("text")

    persona_subparsers.add_parser("reset")

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
        elif args.config_command == "sources":
            run_config_sources()
        else:
            parser.print_help()
    elif args.command == "memory":
        if args.memory_command == "add":
            run_memory_add(args.text)
        elif args.memory_command == "search":
            run_memory_search(args.query, args.limit)
        elif args.memory_command == "list":
            run_memory_list()
        elif args.memory_command == "clear":
            run_memory_clear()
        else:
            parser.print_help()
    elif args.command == "session":
        if args.session_command == "list":
            run_session_list()
        elif args.session_command == "show":
            run_session_show(args.session_id)
        elif args.session_command == "clear":
            run_session_clear(args.session_id)
        else:
            parser.print_help()
    elif args.command == "persona":
        if args.persona_command == "show":
            run_persona_show()
        elif args.persona_command == "set":
            run_persona_set(args.text)
        elif args.persona_command == "reset":
            run_persona_reset()
        else:
            parser.print_help()
    else:
        parser.print_help()



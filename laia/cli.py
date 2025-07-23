import argparse

from laia.commands.start_project import start_project
from laia.commands.init_project import init_project
from laia.commands.generate_schema import generate_schema

def main():
    parser = argparse.ArgumentParser(description="Laia CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Init new project of LAIA")
    subparsers.add_parser("start", help="Start existing LAIA project")
    subparsers.add_parser("generate-schema", help="Generate new OpenAPI schema")

    subparsers.add_parser("help", help="Help")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "start":
        start_project()
    elif args.command == "generate-schema":
        generate_schema()
    elif args.command == "help":
        parser.print_help()
    else:
        print(f"Invalid command. Type 'help' to see the list of available commands.")
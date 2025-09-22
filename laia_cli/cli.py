import argparse

from laia_cli.commands.start_project import start_project
from laia_cli.commands.init_project import init_project
from laia_cli.commands.generate_schema import generate_schema

def main():
    parser = argparse.ArgumentParser(description="Laia CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Init new project of LAIA")
    start_parser = subparsers.add_parser("start", help="Start existing LAIA project")
    start_parser.add_argument("--backend", action="store_true", help="Start backend server")
    start_parser.add_argument("--backoffice", action="store_true", help="Start backoffice project")
    start_parser.add_argument("--frontend", action="store_true", help="Start frontend project")
    subparsers.add_parser("generate-schema", help="Generate new OpenAPI schema")

    subparsers.add_parser("help", help="Help")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "start":
        start_project(args)
    elif args.command == "generate-schema":
        generate_schema()
    elif args.command == "help":
        parser.print_help()
    else:
        print(f"Invalid command. Type 'help' to see the list of available commands.")
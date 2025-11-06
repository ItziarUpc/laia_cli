import argparse

from laia_cli.commands.start_project import start_project
from laia_cli.commands.init_project import init_project
from laia_cli.commands.generate_schema import generate_schema

def main():
    parser = argparse.ArgumentParser(description="Laia CLI")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Init new LAIA project")
    init_parser.add_argument("--name", type=str, help="Project name", default="routeinjector")
    init_parser.add_argument("--ontology", action="store_true", help="Include ontology (Fuseki)")
    init_parser.add_argument("--storage", action="store_true", help="Include storage (MinIO)")
    init_parser.add_argument("--access-rights", action="store_true", help="Enable access rights")
    init_parser.add_argument("--no-interactive", action="store_true", help="Skip interactive mode")

    start_parser = subparsers.add_parser("start", help="Start existing LAIA project")
    start_parser.add_argument("--backend", action="store_true", help="Start backend server")
    start_parser.add_argument("--backoffice", action="store_true", help="Start backoffice project")
    start_parser.add_argument("--frontend", action="store_true", help="Start frontend project")
    start_parser.add_argument("--env", choices=["dev", "prod"], default="dev", help="Environment to use")
    subparsers.add_parser("generate-schema", help="Generate new OpenAPI schema")

    subparsers.add_parser("help", help="Help")

    args = parser.parse_args()

    if args.command == "init":
        init_project(
            project_name=args.name,
            use_ontology=args.ontology,
            storage=args.storage,
            use_access_rights=args.access_rights,
            interactive=not args.no_interactive
        )
    elif args.command == "start":
        start_project(args)
    elif args.command == "generate-schema":
        generate_schema()
    elif args.command == "help":
        parser.print_help()
    else:
        print(f"Invalid command. Type 'help' to see the list of available commands.")
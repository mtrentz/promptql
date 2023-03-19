from argparse import ArgumentParser
import db_inspect, generate


# Default func
def default(args):
    # Show help
    parser.print_help()


parser = ArgumentParser(
    description="Transform your PostgreSQL database into a compact schema notation to be used in ChatGPT prompts.",
)
parser.set_defaults(func=default)

# Add subcommands
subparsers = parser.add_subparsers(
    title="Operations", help="Call promptql.py <operation> -h for more info."
)

# db_inspect subcommand
db_inspect_parser = subparsers.add_parser(
    "inspect",
    parents=[db_inspect.db_inspect_parser],
    add_help=False,
)
db_inspect_parser.set_defaults(func=db_inspect.db_inspect)

# generate subcommand
generate_parser = subparsers.add_parser(
    "generate",
    parents=[generate.generate_parser],
    add_help=False,
)
generate_parser.set_defaults(func=generate.generate)

args = parser.parse_args()
args.func(args)

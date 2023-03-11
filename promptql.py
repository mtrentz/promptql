from argparse import ArgumentParser
import inspect, tables


# Default func
def default(args):
    # Show help
    parser.print_help()


parser = ArgumentParser(
    description="Transform your PostgreSQL database into DBML to be used in ChatGPT prompts.",
)
parser.set_defaults(func=default)

# Add subcommands
subparsers = parser.add_subparsers(
    title="Operations", help="Call promptql.py <operation> -h for more info."
)

# inspect subcommand
inspect_parser = subparsers.add_parser(
    "inspect",
    parents=[inspect.inspect_parser],
    add_help=False,
)
inspect_parser.set_defaults(func=inspect.inspect)

# Tables subcommand
tables_parser = subparsers.add_parser(
    "tables",
    parents=[tables.table_parser],
    add_help=False,
)
tables_parser.set_defaults(func=tables.tables)

args = parser.parse_args()
args.func(args)

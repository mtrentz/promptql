from argparse import ArgumentParser
import export, tables


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

# Export subcommand
export_parser = subparsers.add_parser(
    "export",
    parents=[export.export_parser],
    add_help=False,
)
export_parser.set_defaults(func=export.export)

# Tables subcommand
tables_parser = subparsers.add_parser(
    "tables",
    parents=[tables.table_parser],
    add_help=False,
)
tables_parser.set_defaults(func=tables.tables)

args = parser.parse_args()
args.func(args)

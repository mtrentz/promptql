from argparse import ArgumentParser
import inspect, generate


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

# generate subcommand
generate_parser = subparsers.add_parser(
    "generate",
    parents=[generate.generate_parser],
    add_help=False,
)
generate_parser.set_defaults(func=generate.generate)

args = parser.parse_args()
args.func(args)

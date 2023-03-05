import argparse

export_parser = argparse.ArgumentParser(
    description="Transform your PostgreSQL database into DBML tables",
)

# Add flags for host, port, user, password, database, and schema
# export_parser.add_argument(
#     "--host",
#     "-H",
#     type=str,
#     help="The host of the database.",
# )

# export_parser.add_argument(
#     "--port",
#     "-p",
#     type=int,
#     help="The port of the database.",
# )

# export_parser.add_argument(
#     "--user",
#     "-u",
#     type=str,
#     help="The user of the database.",
# )

# export_parser.add_argument(
#     "--password",
#     "-P",
#     type=str,
#     help="The password of the database.",
# )

# export_parser.add_argument(
#     "--database",
#     "-d",
#     type=str,
#     help="The database to export.",
# )

# export_parser.add_argument(
#     "--schema",
#     "-s",
#     type=str,
#     help="The schema to export.",
# )

# export_parser.add_argument(
#     "--output",
#     "-o",
#     type=str,
#     help="The output file to write to. Defaults to schema.dbml",
#     default="schema.dbml",
# )

# First arg
export_parser.add_argument(
    "first_arg",
    type=str,
    help="The first arg",
)

# Second arg
export_parser.add_argument(
    "second_arg",
    type=str,
    help="The second arg",
)


def export(args):
    print("hi from export")
    # Print first_arg and second_arg
    print(args.first_arg, args.second_arg)

import argparse
from helpers.read_env import load_env
import os
import subprocess
import shlex

inspect_parser = argparse.ArgumentParser(
    description="Transform your PostgreSQL database into DBML tables. All arguments are required if not provided in a .env file.",
)

# Add flags for host, port, user, password, database, and schema, etc...
inspect_parser.add_argument(
    "--host",
    "-H",
    type=str,
    help="The host of the database.",
)

inspect_parser.add_argument(
    "--port",
    "-p",
    type=int,
    help="The port of the database.",
)

inspect_parser.add_argument(
    "--user",
    "-u",
    type=str,
    help="The user of the database.",
)

inspect_parser.add_argument(
    "--password",
    "-P",
    type=str,
    help="The password of the database.",
)

inspect_parser.add_argument(
    "--database",
    "-d",
    type=str,
    help="The database to inspect.",
)

inspect_parser.add_argument(
    "--output",
    "-o",
    type=str,
    help="The output file to write to. Defaults to schema.dbml",
    default="schema.dbml",
)

# Docker container name
inspect_parser.add_argument(
    "--container",
    "-c",
    type=str,
    help="If provided, will run pg_dump for a docker container with this name.",
)

inspect_parser.add_argument(
    "--env",
    "-e",
    type=str,
    help="The path to the .env file. Defaults to .env",
    default=".env",
)


def inspect(args):
    # Load environment variables
    load_env(args.env)

    # Get arguments
    host = args.host or os.environ.get("HOST")
    port = args.port or os.environ.get("PORT")
    user = args.user or os.environ.get("USER")
    password = args.password or os.environ.get("PASSWORD")
    database = args.database or os.environ.get("DATABASE")
    container = args.container or os.environ.get("CONTAINER")
    output = args.output or os.environ.get("OUTPUT")

    # If providing container name, needs database, user, and password
    if container:
        if not all([database, user, password]):
            print("Missing arguments. Please provide database, user, and password.")
            return
    else:
        # If not providing container name, needs host, port, user, password, and database
        if not all([host, port, user, password, database]):
            print(
                "Missing arguments. Please provide host, port, user, password, and database."
            )
            return

    # Defining some commands
    pg_dump_flags = "-s --no-tablespaces --no-table-access-method --no-comments --no-security-labels --no-publications --no-subscriptions --no-toast-compression --no-unlogged-table-data --quote-all-identifiers --no-acl"

    if container:
        # PASSWORD works because of environment variables
        cmd = f"docker exec {container} pg_dump {pg_dump_flags} -U {user} -d {database}"
    else:
        # TODO: test this
        cmd = f"pg_dump {pg_dump_flags} -h {host} -p {port} -U {user} -d {database}"

    # Save cleand sql to a temp file
    tmp = "promptsql_temp_schema.sql"

    # Run a bunch of commands to clean up the sql and write to output file
    sql = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE)
    awk = subprocess.run(
        shlex.split(r"""awk 'BEGIN {RS=""; ORS="\n\n"} /CREATE TABLE[^;]*;/'"""),
        input=sql.stdout,
        stdout=subprocess.PIPE,
    )
    sed1 = subprocess.run(
        shlex.split(r"""sed 's/double precision/double/g'"""),
        input=awk.stdout,
        stdout=subprocess.PIPE,
    )
    sed2 = subprocess.run(
        shlex.split(r"""sed '/^[[:space:]]*CONSTRAINT/d'"""),
        input=sed1.stdout,
        stdout=subprocess.PIPE,
    )
    subprocess.run(
        shlex.split(r"""sed ':a;N;$!ba;s/,\s*\n\s*)\s*;/\n);/g;s/[[:space:]]*$//'"""),
        input=sed2.stdout,
        stdout=open(tmp, "w"),
    )

    # Run dbml2sql with all the cleaning needed before
    subprocess.run(
        shlex.split(f"sql2dbml {tmp} --postgres"),
        stdout=open(output, "w"),
    )

    # Remove temp file
    os.remove(tmp)

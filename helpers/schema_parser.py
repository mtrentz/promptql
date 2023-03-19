import re


def schema_parser(file: str) -> dict:
    """
    Return a dict where the keys are the table names and
    the value is the string for the compact schema notation.
    """
    # Initialize an empty dictionary
    schema_dict = {}
    # Open the file and read its contents
    with open(file, "r") as f:
        content = f.read()

    # Loop over each line, if starts with TABLE then it's a table.
    # If so, get the table name which is the first value enclosed by double quotes.
    # The value will still be the full line.
    for line in content.splitlines():
        if line.strip().startswith("TABLE"):
            table_name = re.search(r'"([^"]+)"', line).group(1)
            schema_dict[table_name] = line

    return schema_dict

    # # Split the content by table definitions
    # tables = content.split("Table ")[1:]
    # # Loop through each table definition
    # for table in tables:
    #     # Split the table definition by lines
    #     lines = table.split("\n")
    #     # Get the table name from the first line
    #     table_name = lines[0].strip('" {}')
    #     # Join the rest of the lines into a single string
    #     table_content = "\n".join(lines[1:])
    #     # Add the table name and content to the dictionary
    #     dbml_dict[table_name] = "Table “{}” {{\n{}".format(table_name, table_content)
    # # Return the dictionary
    # return dbml_dict

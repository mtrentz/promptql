import os

def parse_dbml(file: str) -> dict:
    """
    Return a dict where the keys are the table names and
    the value is the string for the formatted representation of the DBML.
    """

    # Initialize an empty dictionary
    dbml_dict = {}
    # Open the file and read its contents
    with open(file, 'r') as f:
        content = f.read()
    # Split the content by table definitions
    tables = content.split('Table ')[1:]
    # Loop through each table definition
    for table in tables:
        # Split the table definition by lines
        lines = table.split('\n')
        # Get the table name from the first line
        table_name = lines[0].strip('" {}')
        # Join the rest of the lines into a single string
        table_content = '\n'.join(lines[1:])
        # Add the table name and content to the dictionary
        dbml_dict[table_name] = 'Table “{}” {{\n{}'.format(table_name, table_content)
    # Return the dictionary
    return dbml_dict

import re


def convert_schema(sql: str) -> str:
    """
    Receives an SQL string and return a string with a simplified DBML syntax.
    """
    # Keep only the CREATE TABLE statements
    create_table_pattern = re.compile(r"^CREATE TABLE .*?;", re.DOTALL | re.MULTILINE)
    # This is a list of strings with the CREATE TABLE statements
    sql = re.findall(create_table_pattern, sql)

    # Now I only want to keep the lines that are:
    # 1. CREATE TABLE ...
    # 2. column names like: "col name" types,
    # 3. The lines that are literally -> );
    # If not any of those just remove.
    filtered_content = []
    for stmt in sql:
        # Split the string into a list of lines
        lines = stmt.splitlines()
        # Remove the first line
        first = lines.pop(0)
        # Remove the last line
        last = lines.pop()
        # Remove the lines that are not column names
        lines = [line for line in lines if line.strip().startswith('"')]
        # Join the lines back into a string
        stmt = first + "\n" + "\n".join(lines) + "\n" + last
        # Add the string to the list
        filtered_content.append(stmt)

    # Join the list of strings into a single string
    filtered_content = "\n\n".join(filtered_content)

    # The CREATE lines right now are like these: CREATE TABLE "public"."table_name" (
    # I want to remove the "public" part.
    # Also, make it work even if was anything else besides "public"
    filtered_content = re.sub(
        r'CREATE TABLE "(.*?)\.', "CREATE TABLE ", filtered_content
    )

    # My goal now is to to substitute the data types with an abbreviated letter (very general).
    # For example -> "col_name" varchar(255) -> "col_name" T, where T stands for text.
    abbreviations = {
        "integer": "N",
        "bigint": "N",
        "numeric": "N",
        "double precision": "N",
        "real": "N",
        "smallint": "N",
        "decimal": "N",
        "date": "D",
        "time": "D",
        "timestamp": "D",
        "interval": "D",
        "boolean": "B",
        "text": "T",
        "character": "T",
        "char": "T",
        "varchar": "T",
        "character varying": "T",
        "json": "J",
        "uuid": "U",
        "?": "?",  # default abbreviation
    }

    # For this I will itearte over each line, if it starts with a comma then its a column name.
    # I want to separate the column name from the data type. The column name will be enclosed in
    # the first two double quotes. The data type will be the rest of the line.
    # I will then replace the data type with the abbreviation.
    # If one of the abbreviations are present in the data type, i assume that one and continue.
    # If none of the abbreviations are present, i will use the default abbreviation.
    filtered_content = filtered_content.splitlines()
    for i, line in enumerate(filtered_content):
        # If doenst start with a table quote, continue
        if not line.strip().startswith('"'):
            continue

        # Now get the column name, this is the first two double quotes
        col_name = re.search(r'"([^"]+)"', line).group(1)
        rest = line.split(col_name)[-1]

        # Now get abbreviation
        abbr = "?"

        for key, value in abbreviations.items():
            if key in rest:
                abbr = value
                break

        # The new line will be a tab, the column name enclosed in double quotes, and the abbreviation ending in a commma
        new_line = f'\t"{col_name}" {abbr},'

        # Replace the old line with the new line
        filtered_content[i] = new_line

    # Join the list of strings into a single string
    filtered_content = "\n".join(filtered_content)

    # Do some clean for syntatic definitions.
    # All CREATE TABLE will be only TABLE
    filtered_content = re.sub(r"CREATE TABLE", "TABLE", filtered_content)

    # # Change every newline and tab into a space
    # filtered_content = re.sub(r"[\n\t]", " ", filtered_content)

    # # Group two or more spaces into one
    # filtered_content = re.sub(r" {2,}", " ", filtered_content)

    # Remove every space, tab, newline and so on
    filtered_content = re.sub(r"\s+", "", filtered_content)

    # Place two newline inbetween each TABLE in all caps.
    filtered_content = re.sub(r"TABLE", "\n\nTABLE", filtered_content)

    return filtered_content

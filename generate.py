import argparse
import os
from helpers.schema_parser import schema_parser
from helpers.inquirer_flows import pre_menu_mode, menu_mode, search_mode, select_mode
from helpers.schema_converter import HELP_TEXT

generate_parser = argparse.ArgumentParser(
    description="Pick and choose which generate to export. (Won't affect performance)",
)


def export_to_file(schema):
    with open("prompt.txt", "w+") as f:
        f.write(HELP_TEXT)
        f.write("\n")
        for val in schema.values():
            f.write(val)
            f.write("\n")

        f.write("\n")
        f.write(
            "Act as a Senior Data Analyst with experience in PostgreSQL and write a query to ..."
        )

    print("Prompt saved to prompt.txt!")


def generate(args):
    fname = "out.schema"
    if not os.path.exists(fname):
        print(f"{fname} does not exist. Run promptql inspect first.")
        return

    schema = schema_parser(fname)
    table_names = schema.keys()

    # Pre menu to know if the user actually wants
    # to select tables or just want to export them all
    pre_menu_answer = pre_menu_mode()

    if pre_menu_answer == "export-all":
        export_to_file(schema)
        return

    # For selectio	n flow create a table_selection which is a list of dict
    # as [{name: table_name, checked: bool}, ...]
    table_selection = [{"name": t, "checked": False} for t in table_names]

    # Now initiate the inquirer section where the user
    # will choose which tables to export.
    while True:
        print(
            f"Tables selected: {len([t['name'] for t in table_selection if t['checked']])}"
        )
        menu_answer = menu_mode()

        if menu_answer == "Quit":
            break

        if menu_answer == "Select":
            table_selection = select_mode(table_selection)

        if menu_answer == "Search":
            table_selection = search_mode(table_selection)

        if menu_answer == "Export":
            selected_table_names = [t["name"] for t in table_selection if t["checked"]]
            schema = {k: v for k, v in schema.items() if k in selected_table_names}
            # TODO: ask for file name (still have default)
            export_to_file(schema)
            return

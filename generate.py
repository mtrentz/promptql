import argparse
import os
from helpers.dbml_parser import parse_dbml
from helpers.inquirer_flows import pre_menu_mode, menu_mode, search_mode, select_mode

generate_parser = argparse.ArgumentParser(
		description="Pick and choose which generate to export. (Won't affect performance)",
)


def export_to_file(dbml):
	# TODO: Here in the future I want to put some extra text
	# that will help chatgpt to generate the code. For example: Act as...
	# use postgres! and so on...
	with open("prompt.txt", "w+") as f:
		for val in dbml.values():
			f.write(val)
	print("Tables exported to prompt.txt!")


def generate(args):
	# Check if schema.dbml exists
	fname = "schema.dbml"
	if not os.path.exists(fname):
			print(f"{fname} does not exist. Run promptql inspect first.")
			return
	
	dbml = parse_dbml(fname)
	table_names = dbml.keys()

	# Pre menu to know if the user actually wants
	# to select tables or just want to export them all
	pre_menu_answer = pre_menu_mode()

	if pre_menu_answer == "export-all":
		export_to_file(dbml)
		return


	# For selectio	n flow create a table_selection which is a list of dict
	# as [{name: table_name, checked: bool}, ...]
	table_selection = [{"name": t, "checked": False} for t in table_names]

	# Now initiate the inquirer section where the user
	# will choose which tables to export.
	while True:

		print(f"Tables selected: {len([t['name'] for t in table_selection if t['checked']])}")

		menu_answer = menu_mode()

		if menu_answer == "Quit":
			break

		if menu_answer == "Search":
			table_selection = search_mode(table_selection)
		
		if menu_answer == "Select":
			table_selection = select_mode(table_selection)

		if menu_answer == "Export":
			selected_table_names = [t["name"] for t in table_selection if t["checked"]]
			dbml = {k:v for k,v in dbml.items() if k in selected_table_names}
			export_to_file(dbml)
			return





import inquirer
from typing import List, Dict, Union, Literal

def _update_items(
    items: List[Dict[str, Union[str, bool]]],
    selected_items: List[str],
    previous_selected_items: List[str] = None,
) -> List[Dict[str, Union[str, bool]]]:
    """
    Receives the items, which are a list of dicts with the following structure:
    {
        "name": "Milk",
        "checked": False
    }, ...

    Receives the selected items, which is a list of strings with the names of the
    items that were selected.

    Receives the previous selected items, which is a list of strings with the
    names of the items that were selected in the previous mode.

    Returns the updated items, with the selected items having the "checked" key.
    """
    # Update items
    for item in items:
        # Easy part, if there are items on newly selected items just check them
        # on the original items.
        if item["name"] in selected_items:
            item["checked"] = True

        # Now, if item is in filtere_data but not in newly_selected_items, then
        # we need to uncheck it.
        if (
            previous_selected_items
            and item["name"] in previous_selected_items
            and item["name"] not in selected_items
        ):
            item["checked"] = False

    return items


def select_mode(items: List[Dict[str, Union[str, bool]]]) -> List[dict]:
    """
    Receives the items, which are a list of dicts with the following structure:
    {
        "name": "Milk",
        "checked": False
    }, ...

    Returns the updated items, with the selected items having the "checked" key.
    """
    questions = [
        inquirer.Checkbox(
            "items",
            message="Select items",
            choices=[x["name"] for x in items],
            default=[x["name"] for x in items if x["checked"]],
        )
    ]

    answer = inquirer.prompt(questions)

    # Update items
    items = _update_items(
        items, answer["items"], [x["name"] for x in items if x["checked"]]
    )

    return items


def search_mode(items: List[Dict[str, Union[str, bool]]]) -> List[dict]:
    """
    Receives the items, which are a list of dicts with the following structure:
    {
        "name": "Milk",
        "checked": False
    }, ...

    Returns the updated items, with the selected items having the "checked" key.
    """
    questions = [inquirer.Text("search", message="What do you want to search for?")]

    answer = inquirer.prompt(questions)

    # Filter data
    filtered_data = [x for x in items if answer["search"].lower() in x["name"].lower()]

    # If no items are found, show a message and return to menu without updating
    if not filtered_data:
        print("No items found")
        return items

    # Here I need to do a selection on just the filtered data
    # and then update the original data with the selected items, keeping in mind
    # that the original data might have other items selected that are not in the
    # filtered data. These selected items should be kept selected.
    filter_selected_items = select_mode(filtered_data)

    # Update original data, keeping in mind that the user might have unselected
    # items that are on the filtered_data.
    for item in items:
        # Easy part, if there are items on newly selected items just check them
        # on the original items.
        if item["name"] in filter_selected_items:
            item["checked"] = True

        # Now, if item is in filtere_data but not in newly_selected_items, then
        # we need to uncheck it.
        if item["name"] in filtered_data and item["name"] not in filter_selected_items:
            item["checked"] = False

    return items


def menu_mode() -> str:
    # Options: Search, Select, Export, QUit
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do?",
            choices=[
                "Search",
                "Select",
                "Export",
                "Quit",
            ],
        )
    ]

    choice = inquirer.prompt(questions)["action"]

    return choice


def pre_menu_mode() -> Literal["selection", "export-all"]:
    """
    Checks if the user wants to go to interactive table selection or just
    export all tables.
    """
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do?",
            choices=[
                ("Export all tables", "export-all"),
                ("Interactively choose tables to export", "selection"),
            ],
        )
    ]

    choice = inquirer.prompt(questions)["action"]

    return choice

import inquirer
from typing import List, Dict, Union, Literal


def _update_items(
    items: List[Dict[str, Union[str, bool]]], selected_items: List[str]
) -> List[Dict[str, Union[str, bool]]]:
    """
    Receives the items, which are a list of dicts with the following structure:
    [
        {
            "name": "Milk",
            "checked": False
        },
        ...
    ]

    Receives the selected items, which is a list of strings with the names of the
    items that were selected.

    Returns the updated items, with the selected items having the "checked" key.
    """
    # Get the previous selected items
    previous_selected_items = [item["name"] for item in items if item["checked"]]

    # Update items
    for item in items:
        # If there are items on newly selected items just check them
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
    [
        {
            "name": "Milk",
            "checked": False
        },
        ...
    ]

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

    # Answer is list of strings with the names of the selected items
    answer = inquirer.prompt(questions)["items"]

    # Update items
    items = _update_items(items, answer)

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
    questions = [
        inquirer.Text(
            "search",
            message="What do you want to search for? Use ';' to separate multiple terms",
        )
    ]

    # Get what the user wants to search for
    answer = inquirer.prompt(questions)
    terms = answer["search"].split(";")

    # Filter data
    # filtered_data = [x for x in items if answer["search"].lower() in x["name"].lower()]
    filtered_items = []
    for item in items:
        for term in terms:
            # Check if the item contains the term
            if term.lower() in item["name"].lower():
                filtered_items.append(item)
                break

    # If no items are found, show a message and return to menu without updating
    if not filtered_items:
        print("No items found")
        return items
    
    # Orer by name ascending
    filtered_items = sorted(filtered_items, key=lambda x: x["name"])

    # Here I want to do a search on just my filtered items. So I will send that
    # to select_mode and will get back the items the user selected only from the
    # filtered items.
    filtered_items = select_mode(filtered_items)

    # Now I need to update the original items with the selected items from the
    # filtered items. Every filtered thats checked should be checked on the
    # original items. And every filtered item that is not checked should be
    # unchecked on the original items.
    for item in items:
        for filtered_item in filtered_items:
            if item["name"] == filtered_item["name"]:
                item["checked"] = filtered_item["checked"]

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

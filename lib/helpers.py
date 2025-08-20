# lib/helpers.py
import sys
from models.category import Category
from models.item import Item


def list_all_items():
    items = Item.get_all_items()
    if not items:
        print("No items found.")
    else:
        for item in items:
            print(item)

def find_by_name():
    name = input("Enter item name: ")
    item = Item.find_by_name(name)
    print(item) if item else print(f'{name} item not found.')

def find_by_quantity():
    try:
        quantity = int(input("Enter the item's quantity: "))
    except ValueError:
        print("Quantity must be an integer.")
        return

    items = Item.find_by_quantity(quantity)
    if not items:
        print(f'No items found in quantity "{quantity}".')
    else:
        print(f'Items in quantity "{quantity}":')
        for item in items:
            print(item)

def create_item():
    name = input("Enter the item's name: ")
    quantity = int(input("Enter the items's quantity: "))
    try:
        item = Item.create(name, quantity)
        print(f'Success: {item.name} ({item.quantity}) created for Category')
    except Exception as exc:
        print("Error creating item: ", exc)

def update_item():
    name = input("Enter the items's name: ")
    if item := Item.find_by_name(name):
        try:
            name = input("Enter the items's new name: ")
            item.name = name
            quantity = int(input("Enter the item's new quantity: "))
            item.quantity = quantity

            item.update()
            print(f'Success: {item}')
        except Exception as exc:
            print("Error updating item: ", exc)
    else:
        print(f'Item {name} not found.')

def delete_item():
    name = input("Enter the item's name: ")
    if item := Item.find_by_name(name):
        item.delete()
        print(f'Item {name} deleted.')
    else:
        print(f'Item {name} not found.')

def exit_program():
    print("Goodbye!")
    sys.exit()



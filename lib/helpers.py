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
            print(f"{item.name} | Quantity: {item.quantity} | Category: {item.category.name}")

def find_by_name():
    name = input("Enter item name: ")
    item = Item.find_by_name(name)
    if item: 
        print(f"{item.name} | Quantity: {item.quantity} | Category: {item.category.name}")
    else:
        print(f"No item found with name '{name}'")

def find_by_quantity():
    try:
        quantity = int(input("Enter the item's quantity: "))
    except ValueError:
        print("Quantity must be an integer.")
        return
    items = Item.find_by_quantity(quantity)
    if not items:
        print(f'No items found with quantity: {quantity}.')
        return
    print(f'Items with quantity: {quantity}')
    for item in items:
        print(f"{item.name} | Quantity: {item.quantity} | Category: {item.category.name}")

def create_item():
    try:
        name = input("Enter the item's name: ")
        quantity = int(input("Enter the item's quantity: "))
        item = Item.create(name, quantity)
        print(f'Success: {item.name} ({item.quantity}) created.')
    except ValueError:
        print("Quantity must be an integer.")
    except Exception as exc:
        print("Error creating item: ", exc)

def update_item():
    name = input("Enter the item's name: ")
    if item := Item.find_by_name(name):
        try:
            new_name = input("Enter the item's new name: ")
            item.name = new_name
            new_quantity = int(input("Enter the item's new quantity: "))
            item.quantity = new_quantity

            item.update()
            print(f'Success: {item}')
        except ValueError:
            print("Quantity must be an integer.")
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



# lib/cli.py
import click

from helpers import (
    exit_program,
    list_all_items,
    find_by_name,
    find_by_quantity,
    create_item,
    update_item,
    delete_item
)


@click.command()
def main():
    while True:
        menu()
        choice = click.prompt("> ", type=str).strip()
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_all_items()
        elif choice == "2":
            find_by_name()
        elif choice == "3":
            find_by_quantity()
        elif choice == "4":
            create_item()
        elif choice == "5":
            update_item()
        elif choice == "6":
            delete_item()
        else:
            click.echo("Invalid choice.")


def menu():
    click.echo("\nPlease select an option:")
    click.echo("0. Exit the program")
    click.echo("1. List all items")
    click.echo("2. Find item by name")
    click.echo("3. Find item by quantity")
    click.echo("4. Create item")
    click.echo("5. Update item")
    click.echo("6. Delete item")


if __name__ == "__main__":
    main()

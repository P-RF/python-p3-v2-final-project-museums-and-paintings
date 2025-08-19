# lib/cli.py
import click

from helpers import (
    exit_program,
    list_all_trains,
    find_train_by_line,
    find_train_by_category,
    create_train,
    update_train,
    delete_train
)


@click.command()
def main():
    while True:
        menu()
        choice = click.prompt("> ", type=str).strip()
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_all_trains()
        elif choice == "2":
            line = click.prompt("Enter train line")
            find_train_by_line(line)
        elif choice == "3":
            category = click.prompt("Enter train category")
            find_train_by_category(category)
        elif choice == "4":
            create_train()
            click.echo("Train created!")
        elif choice == "5":
            update_train()
            click.echo("Train updated.")
        elif choice == "6":
            delete_train()
            click.echo("Train deleted.")
        else:
            click.echo("Invalid choice.")


def menu():
    click.echo("\nPlease select an option:")
    click.echo("0. Exit the program")
    click.echo("1. List all trains")
    click.echo("2. Find train by line")
    click.echo("3. Find train by category")
    click.echo("4. Create train")
    click.echo("5. Update train")
    click.echo("6. Delete train")


if __name__ == "__main__":
    main()

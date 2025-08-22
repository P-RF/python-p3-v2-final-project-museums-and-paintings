# lib/cli.py
import click
from models.museum import Museum
from models.painting import Painting

from helpers import (
    list_museums,
    create_museum,
    update_museum,
    delete_museum,
    list_paintings,
    create_painting,
    update_painting,
    delete_painting,
    exit_program,
)


@click.command()
def cli():
    main_menu()


def main_menu():
    while True:
        click.echo("\nPlease select an option: \n")
        click.echo("Type M or m to see the museums")
        click.echo("Type E or e to exit\n")
        choice = input("> ")

        if choice.lower() == "m":
            museums_menu()
        elif choice.lower() == "e":
            exit_program()
        else: 
            click.echo("Invalid choice. Type M/m or E/e.")


def museums_menu():
    while True:
        click.echo("\nMuseums: \n")
        museums = list_museums()

        for i in range(len(museums)):
            museum = museums[i]
            click.echo(f'{i + 1}. {museum.name} ({museum.location})')

        click.echo(" \nPlease type the number corresponding to the museum from the list to see its details")
        click.echo("                or")
        click.echo("Type B or b to go back to the previous menu")
        click.echo("Type A or a to add a new museum")
        click.echo("Type E or e to exit\n")
        choice = input("> ")

        if choice.lower() == "b":
            return main_menu()
        elif choice.lower() == "a":
            create_museum()
        elif choice.lower() == "e":
            exit_program()
        else:
            try:
                number = int(choice)
                if 1 <= number <= len(museums):
                    museum = museums[number - 1]
                    paintings_menu(museum)
                else:
                    click.echo("Invalid number. Choose a number from the museum list.")
            except ValueError:
                click.echo("Invalid choice. Type a number on the list, B/b, A/a, or E/e.")


def paintings_menu(museum):
    while True:
        click.echo(f"\nPaintings at '{museum.name}': \n")
        paintings = list_paintings(museum)

        if paintings:
            for i in range(len(paintings)):
                painting = paintings[i]
                click.echo(f'{i + 1}. {painting.title}')

        click.echo(" \nPlease type the number corresponding to the painting from the list to see its details")
        click.echo("                or")
        click.echo("Type B or b to go back to the previous menu")
        click.echo("Type A or a to add a new painting")
        click.echo("Type U or u to update this museum")
        click.echo("Type D or d to delete this museum")
        click.echo("Type E or e to exit\n")
        choice = input("> ")

        if choice.lower() == "b":
            return museums_menu()
        elif choice.lower() == "a":
            create_painting(museum)
        elif choice.lower() == "u":
            update_museum(museum)
        elif choice.lower() == "d":
            delete_museum(museum)
            return museums_menu()
        elif choice.lower() == "e":
            exit_program()
        else:
            try:
                number = int(choice)
                if 1 <= number <= len(paintings):
                    painting = paintings[number - 1]
                    return painting_details_menu(painting, museum)
                else:
                    click.echo("Invalid number. Choose a number from the painting list.")
            except ValueError:
                click.echo("Invalid choice. Type a number on the list, B/b, A/a, D/d, or E/e.")

def painting_details_menu(painting, museum):
    while True:
        click.echo(f"\nDetails of '{painting.title}': ")
        click.echo(f"Artist: {painting.artist}")
        click.echo(f"Year: {painting.year}")

        click.echo(" \nOptions:")
        click.echo("Type B or b to go back to the previous menu")
        click.echo("Type U or u to update this painting")
        click.echo("Type D or d to delete this painting")
        click.echo("Type E or e to exit\n")
        choice = input("> ")

        if choice.lower() == "b":
            return paintings_menu(museum)
        elif choice.lower() == "u":
            update_painting(painting)
            painting = Painting.find_by_id(painting.id)
            return painting_details_menu(painting, museum)
        elif choice.lower() == "d":
            delete_painting(painting)
            return paintings_menu(museum)
        elif choice.lower() == "e":
            exit_program()
        else: click.echo("Invalid choice. Type B/b, U/u, D/d, or E/e.")


if __name__ == "__main__":
    cli()
# lib/cli.py
import click
from models.museum import Museum
from models.painting import Painting

from helpers import (
    exit_program,
    list_museums,
    list_paintings
)

museums = []

def menu():
    print("Please select an option:")
    print("Type M or m to see the museums")
    print("Type E or e to exit")

def main():
    while True:
        menu()
        choice = input("> ")
        if choice.lower() == "m":
            list_museums(museums)
        elif choice.lower() == "e":
            exit_program()
        else:
            print("Invalid choice. Type M/m or E/e.")


def museums_menu():
    print("\nPlease type the number of the museum to see their details")
    print("or")
    print("Type B or b to go back to the previous menu")
    print("Type A or a to add a new museum")
    print("Type E or e to exit")

def museums_main(museums):
    while True:
        museums_menu()
        choice = input("> ")
        if choice.lower() == "b":
            return
        elif choice.lower() == "a":
            add_museum(museums)
        elif choice.lower() == "e":
            exit_program()
        else:
            print("Invalid choice. Type a valid number, B/b, MA/a, or E/e.")


if __name__ == "__main__":
    main()
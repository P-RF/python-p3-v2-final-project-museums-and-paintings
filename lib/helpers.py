# lib/helpers.py
import sys
import click
from models.museum import Museum
from models.painting import Painting


def list_museums():
    museums = Museum.get_all()
    if not museums:
        click.echo("No museums found.")
        return []

    i = 1
    for museum in museums:
        i += 1
    return museums

def create_museum():
    while True:
        name = input("Enter the museum's name: ")
        if not name or name.isdigit():
            click.echo("Museum name c")
        else:
            break

    while True:
        location = input("Enter the museum's location: ")
        if not location or location.isdigit():
            click.echo("Museum location must contain letters.")
        else:
            break

    Museum.create(name, location)
    click.echo(f"Museum '{name}' in '{location}' has been added!")

def update_museum():
    pass

def delete_museum(museum):
    if not museum:
        click.echo("No museum selected.")
        return

    paintings = Painting.find_by_museum(museum.id)
    for painting in paintings:
        painting.delete()

    museum.delete()
    click.echo(f"Museum '{museum.name}' has been deleted.")

def list_paintings(museum):
    if not museum:
        click.echo("No museum selected.")
        return []

    paintings = Painting.find_by_museum(museum.id)
    
    if not paintings:
        click.echo("No paintings found.")
        return []

    return paintings

def create_painting(museum):
    if not museum:
        click.echo("No museum selected.")
        return

    while True:
        title = input(f"Enter the title for the {museum.name}'s new painting: ")
        if not title or title.isdigit():
            click.echo("Painting title must contain letters.")
        else:
            break

    while True:
        artist = input(f"Enter the artist for the {museum.name}'s new painting: ")
        if not artist or artist.isdigit():
            click.echo("Painting artist must contain letters.")
        else:
            break

    while True:
        year_input = input(f"Enter the year created for the {museum.name}'s new painting (e.g., 1877): ")
        if not year_input.isdigit():
            click.echo("Year must be a valid number.")
            continue
        year = int(year_input)
        from datetime import datetime
        current_year = datetime.now().year
        if year < 1000 or year > current_year:
            click.echo(f"Year must be between 1000 and {current_year}.")
            continue
        break
    Painting.create(title, artist, year, museum)
    click.echo(f"'{title}' by {artist} | {year} has been added to '{museum.name}'.")

    return paintings_menu(museum)

def update_painting(painting):
    if not painting:
        click.echo("No painting selected.")
        return

    click.echo(f"\nUpdating '{painting.title}'")

    while True:
        new_title = input(f"Enter a new title: ")
        if not new_title:
            new_title = painting.title
            break
        elif new_title.isdigit():
            click.echo("Painting title must contain letters.")
        else:
            break

    while True:
        new_artist = input(f"Enter a new artist name: ")
        if not new_artist:
            new_artist = painting.artist
            break
        elif new_artist.isdigit():
            click.echo("Painting artist must contain letters.")
        else:
            break

    from datetime import datetime
    current_year = datetime.now().year
    while True:
        new_year_input = input(f"Enter a new year: ")
        if not new_year_input:
            new_year = painting.year
            break
        elif not new_year_input.isdigit():
            click.echo("Year must be a valid number.")
        else:
            new_year = int(new_year_input)
            if 1000 <= new_year <= current_year:
                break
            else:
                click.echo(f"Year must be between 1000 and {current_year}.")

    painting.update(title=new_title, artist=new_artist, year=new_year)
    click.echo(f"'{painting.title}' by {painting.artist} ({painting.year}) has been updated.")

    return painting

def delete_painting(painting):
    if not painting:
        click.echo("No painting selected.")
        return

    painting.delete()
    click.echo(f"Painting '{painting.title}' by {painting.artist} has been deleted.")

def exit_program():
    print("Goodbye!")
    sys.exit()



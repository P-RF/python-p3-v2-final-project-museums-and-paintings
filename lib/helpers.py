# lib/helpers.py
import sys
from models.nycdot import Nycdot
from models.train import Train


def list_all_trains():
    trains = Train.get_all_trains()
    if not trains:
        print("No trains found.")
    else:
        for train in trains:
            print(train)

def find_by_line():
    line = input("Enter train line: ")
    train = Train.find_by_line(line)
    print(train) if train else print(f'{line} train not found.')

def find_by_category():
    category = input("Enter the train's category: ")
    trains = Train.find_by_category(category)
    if not trains:
        print(f'No trains found in category "{category}".')
    else: 
        print(f'Trains in category "{category}":')
        for train in trains:
            print(train)

def create_train():
    line = input("Enter the train's line: ")
    category = input("Enter the train's category: ")
    try:
        train = Train.create(line, category, nycdot_id=None)
        print(f'Success: {train.line} ({train.category}) created for Nycdot')
    except Exception as exc:
        print("Error creating train: ", exc)

def update_train():
    line = input("Enter the train's line: ")
    if train := Train.find_by_line(line):
        try:
            line = input("Enter the train's new line: ")
            train.line = line
            category = input("Enter the train's new category: ")
            train.category = category

            train.update()
            print(f'Success: {train}')
        except Exception as exc:
            print("Error updating train: ", exc)
    else:
        print(f'Train {line} not found.')

def delete_train():
    line = input("Enter the train's line: ")
    if train := Train.find_by_line(line):
        train.delete()
        print(f'Train {line} deleted.')
    else:
        print(f'Train {line} not found.')

def exit_program():
    print("Goodbye!")
    sys.exit()



import csv
import argparse

from election_maps.entities.observer import Observer
from election_maps.clients.db.users import UsersDatabaseHandler


def parse_arguments():
    argument_parser = argparse.ArgumentParser("Script pentru importul de useri in "
                                              "baza de date")

    argument_parser.add_argument("file", help="Path catre fisierul csv in care sunt "
                                              "stocati userii")

    return argument_parser.parse_args()


def read_data(file: str) -> [Observer]:
    data = []

    with open(file) as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            data.append(Observer.from_dict_csv(row))

    return data


def insert_data(data: [Observer]):
    print(f"{len(data)} Users to insert in the database!")
    database_handler = UsersDatabaseHandler()
    result = database_handler.add_users(data)
    print(f"Inserted successfully {len(result)} entries!")


def main():
    args = parse_arguments()
    data = read_data(args.file)
    insert_data(data)


if __name__ == "__main__":
    main()

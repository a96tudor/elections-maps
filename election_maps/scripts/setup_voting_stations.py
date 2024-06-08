import csv
import argparse

from election_maps.entities.sections import VotingSection
from election_maps.entities.candidates import MayorCandidate, MayorCandidates


def load_mayor_candidates() -> MayorCandidates:
    pass


def load_voting_section(voting_sections_file):
    result = []

    with open(voting_sections_file) as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            result.append(VotingSection.from_dict_csv(row))

    return result

def parse_arguments():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument("voting_sections_file")
    argument_parser.add_argument("--mayor-candidates", required=True)
    argument_parser.add_argument("--local-council-candidates", required=True)

    return argument_parser.parse_args()


def main():
    args = parse_arguments()


if __name__ == '__main__':
    main()

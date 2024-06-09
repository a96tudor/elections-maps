import csv
import argparse

from election_maps.entities.sections import VotingSection, VotingSectionsCollection
from election_maps.entities.candidates import Candidate
from election_maps.entities.voting_results import VotingResult, VotingResultCollection
from election_maps.clients.db.results import ResultsDatabaseHandler


def load_initial_voting_results(file_path: str) -> VotingResultCollection:
    result = VotingResultCollection(invalid_votes=0)

    with open(file_path) as stream:
        reader = csv.DictReader(stream)
        for candidate in reader:
            voting_result = VotingResult(
                candidate=Candidate.from_dict_csv(candidate),
                votes=0,
            )
            result.append(voting_result)

    return result


def load_voting_section(voting_sections_file) -> VotingSectionsCollection:
    result = VotingSectionsCollection()

    with open(voting_sections_file) as stream:
        reader = csv.DictReader(stream)

        for row in reader:
            result.append(VotingSection.from_dict_thin(row))

    return result


def parse_arguments():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument("voting_sections")
    argument_parser.add_argument("--mayor-candidates", required=True)
    argument_parser.add_argument("--local-council-candidates", required=True)
    argument_parser.add_argument("--county-council-candidates", required=True)
    argument_parser.add_argument("--county-council-president-candidates", required=True)
    argument_parser.add_argument("--european-parliament-candidates", required=True)

    return argument_parser.parse_args()


def add_initial_voting_results_to_voting_sections(
    voting_sections: VotingSectionsCollection,
    args: argparse.Namespace
) -> VotingSectionsCollection:
    mayor_results_init = load_initial_voting_results(args.mayor_candidates)
    local_council_results_init = load_initial_voting_results(
        args.local_council_candidates
    )
    county_council_results_init = load_initial_voting_results(
        args.county_council_candidates
    )
    county_council_president_results_init = load_initial_voting_results(
        args.county_council_president_candidates
    )
    european_parliament_results_init = load_initial_voting_results(
        args.european_parliament_candidates
    )

    for vt in voting_sections:
        vt.mayor_results = mayor_results_init
        vt.local_council_results = local_council_results_init
        vt.county_council_results = county_council_results_init
        vt.county_council_president_results = county_council_president_results_init
        vt.european_parliament_results = european_parliament_results_init

    return voting_sections


def main():
    args = parse_arguments()

    voting_sections = load_voting_section(args.voting_sections)
    voting_sections = add_initial_voting_results_to_voting_sections(
        voting_sections, args,
    )

    db_handler = ResultsDatabaseHandler()
    db_handler.insert_batch([vt.to_dict() for vt in voting_sections])


if __name__ == '__main__':
    main()

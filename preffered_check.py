import json
import argparse
from timeit import default_timer as timer
from itertools import combinations

class ArgumentationFramework:
    def __init__(self, arguments, attacks):
        self.arguments = arguments
        self.attacks = attacks
        self.preferred_extensions = None

    def get_attackers(self, argument):
        return [attacker for attacker, attacked in self.attacks if attacked == argument]

    def is_conflict_free(self, subset):
        return not any((a, b) in self.attacks for a in subset for b in subset)

    def defends(self, subset, argument):
        return all(any((defender, attacker) in self.attacks for defender in subset) for attacker, attacked in self.attacks if attacked == argument)

    def powerset(self):
        return [set(subset) for r in range(len(self.arguments)+1) for subset in combinations(self.arguments, r)]

    def is_admissible(self, subset):
        if not self.is_conflict_free(subset):
            return False
        for arg in subset:
            if not self.defends(subset, arg):
                return False
        return True

    def find_preferred_extensions(self):
        all_subsets = sorted(self.powerset(), key=lambda s: len(s), reverse=True)
        preferred_extensions = []
        for subset in all_subsets:
            if self.is_admissible(subset):
                if not any(subset < ext for ext in preferred_extensions):
                    preferred_extensions.append(subset)
        self.preferred_extensions = preferred_extensions
        return preferred_extensions

    def is_credulously_accepted(self, argument):
        preferred_extensions = self.find_preferred_extensions()
        return any(argument in ext for ext in preferred_extensions)
    
def main(file_name, claimed_argument):
    start_time = timer()

    with open(file_name) as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)

    A = parsed_json['Arguments'].keys()
    R = parsed_json['Attack Relations']
    R = [tuple(pair) for pair in R]

    framework = ArgumentationFramework(A, R)
    credulously_accepted = framework.is_credulously_accepted(claimed_argument)
    print(f"\nIs Argument '{claimed_argument}' credulously accepted in the preffered semantic? \nResponse: {credulously_accepted}")
    end_time = timer()
    running_time = end_time - start_time
    print(f"Running time: {running_time} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a discussion game based on an argumentation framework.")
    parser.add_argument("file_name", type=str, help="JSON file containing the argumentation framework.")
    parser.add_argument("claimed_argument", type=str, help="The claimed argument to start the game.")

    args = parser.parse_args()

    main(args.file_name, args.claimed_argument)
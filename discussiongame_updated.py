import json
import random
import argparse
import timeit
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
        return any(argument in ext for ext in self.preferred_extensions)

class DiscussionGame:
    def __init__(self, framework, claimed_argument):
        self.framework = framework
        self.claimed_argument = claimed_argument
        self.IN = set([claimed_argument])
        self.OUT = set()
        self.UNDEC = set(self.framework.get_attackers(claimed_argument))
        self.preferred_extensions = framework.find_preferred_extensions()
        self.preferred_union = set().union(*self.preferred_extensions)

    def proponent_turn(self, last_out_argument):
        # Proponent selects an argument from attackers of last_out_argument

        potential_attackers = set(self.framework.get_attackers(last_out_argument))
        if not potential_attackers:
            return "Opponent wins (rule 3)", True

        preferred_attackers = potential_attackers.intersection(self.preferred_union)
        if preferred_attackers:
            chosen_argument = random.choice(tuple(preferred_attackers))
        else:
            chosen_argument = random.choice(tuple(potential_attackers))

        if chosen_argument in self.OUT:
            return "Proponent wins (rule 2)", True

        self.IN.add(chosen_argument)
        print(f"Proponent chooses argument: {chosen_argument}")

        # Update UNDEC with attackers of the chosen argument, excluding those in OUT
        new_attackers = set(self.framework.get_attackers(chosen_argument)) - self.OUT
        self.UNDEC.update(new_attackers)

        return None, False

    def opponent_turn(self):
        # If UNDEC is empty, proponent wins
        if not self.UNDEC:
            return "Proponent wins (rule 4)", True

        chosen_argument = input(f"Opponent, choose an argument to attack with {self.UNDEC}: ")

        # Check if the chosen argument is valid
        while chosen_argument not in self.UNDEC:
            print("Invalid choice. Try again.")
            chosen_argument = input(f"Opponent, choose an argument to attack with {self.UNDEC}: ")

        print(f"Opponent chooses argument: {chosen_argument}")

        if chosen_argument in self.IN:
            return "Opponent wins (rule 1)", True

        # Move chosen argument from UNDEC to OUT
        self.UNDEC.remove(chosen_argument)
        self.OUT.add(chosen_argument)

        return chosen_argument, False

    def play_game(self):
        last_out_argument = None
        while True:
            result, game_over = self.opponent_turn()
            if game_over:
                print(result)
                break

            last_out_argument, game_over = result, False

            result, game_over = self.proponent_turn(last_out_argument)
            if game_over:
                print(result)
                break


def main(file_name, claimed_argument):
    with open(file_name) as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)

    A = parsed_json['Arguments'].keys()
    R = parsed_json['Attack Relations']
    R = [tuple(pair) for pair in R]

    framework = ArgumentationFramework(A, R)
    
    game = DiscussionGame(framework, claimed_argument)
    game.play_game()
    credulously_accepted = framework.is_credulously_accepted(claimed_argument)
    print(f"\nIs Argument '{claimed_argument}' credulously accepted in the preffered semantic? \nResponse: {credulously_accepted}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a discussion game based on an argumentation framework.")
    parser.add_argument("file_name", type=str, help="JSON file containing the argumentation framework.")
    parser.add_argument("claimed_argument", type=str, help="The claimed argument to start the game.")

    args = parser.parse_args()

    main(args.file_name, args.claimed_argument)
import json
import random
import argparse

class ArgumentationFramework:
    def __init__(self, arguments, attacks):
        """
        arguments: a set of arguments
        attacks: a list of tuples representing attack relations (attacker, attacked)
        """
        self.arguments = arguments
        self.attacks = attacks

    def get_attackers(self, argument):
        """ Return a list of arguments that attack the given argument """
        return [attacker for attacker, attacked in self.attacks if attacked == argument]

    def is_conflict_free(self, args):
        """ Check if a set of arguments is conflict-free """
        for arg in args:
            for attacked in args:
                if (arg, attacked) in self.attacks:
                    return False
        return True

    def defends(self, args, argument):
        """ Check if a set of arguments defends an argument """
        for attacker in self.arguments:
            if (attacker, argument) in self.attacks:
                if not any((defender, attacker) in self.attacks for defender in args):
                    return False
        return True

    def find_admissible_sets(self):
        """ Find all admissible sets in the framework """
        admissible_sets = []
        for args in self.power_set(self.arguments):
            if self.is_conflict_free(args) and all(self.defends(args, arg) for arg in args):
                admissible_sets.append(args)
        return admissible_sets

    def find_preferred_extensions(self):
        """ Find all preferred extensions """
        admissible_sets = self.find_admissible_sets()
        return [a for a in admissible_sets if not any(set(a) < set(b) for b in admissible_sets)]

    @staticmethod
    def power_set(s):
        """ Generate the power set of a set """
        s = list(s)
        x = len(s)
        for i in range(1 << x):
            yield {s[j] for j in range(x) if (i & (1 << j))}


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
            return "Opponent wins (Rule 3)", True

        preferred_attackers = potential_attackers & self.preferred_union
        if preferred_attackers:
            chosen_argument = random.choice(tuple(preferred_attackers))
        else:
            chosen_argument = random.choice(tuple(potential_attackers))

        if chosen_argument in self.OUT:
            return "Proponent wins (Rule 2)", True

        self.IN.add(chosen_argument)
        print(f"Proponent chooses argument: {chosen_argument}")

        # Update UNDEC with attackers of the chosen argument, excluding those in OUT
        new_attackers = set(self.framework.get_attackers(chosen_argument)) - self.OUT
        self.UNDEC.update(new_attackers)

        return None, False

    def opponent_turn(self):
        # If UNDEC is empty, proponent wins
        if not self.UNDEC:
            return "Proponent wins (Rule 4)", True

        chosen_argument = input(f"Opponent, choose an argument to attack {self.UNDEC}: ")

        # Check if the chosen argument is valid
        while chosen_argument not in self.UNDEC:
            print("Invalid choice. Try again.")
            chosen_argument = input(f"Opponent, choose an argument to attack {self.UNDEC}: ")

        print(f"Opponent chooses argument: {chosen_argument}")

        if chosen_argument in self.IN:
            return "Opponent wins (Rule 1)", True

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


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Run a discussion game based on an argumentation framework.")
    # parser.add_argument("file_name", type=str, help="JSON file containing the argumentation framework.")
    # parser.add_argument("claimed_argument", type=str, help="The claimed argument to start the game.")

    # args = parser.parse_args()

    main('AF_2.json', '1')

    # main(args.file_name, args.claimed_argument)
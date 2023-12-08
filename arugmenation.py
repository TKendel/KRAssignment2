import sys
import json
import random
import numpy as np
import itertools

# Load json file
# AFJsonFile = sys.argv[1]
AFJsonFile = "example-argumentation-framework.json"
with open(AFJsonFile, 'r') as argumenation_json:
    argumenation_json = json.load(argumenation_json)

# Get all attack relations from the json
attackRelations = argumenation_json["Attack Relations"]

# Get all arguments from the json
arguments = argumenation_json["Arguments"]
argumentsPlayer = arguments.copy()

listOfArguments = list(arguments.keys())
print(listOfArguments)

# Load claimed argument
# claimedArgument = sys.argv[2]
claimedArgument = "0"

def attackers(argument):
    possible_attackers = []
    for relation in attackRelations:
        if relation[1] == argument:
            possible_attackers.append(relation[0])
    return possible_attackers

def conflictFree():
    conflictFreeSet = [None, ]
    # c reate all possible combinations between the sets 
    # This could be potential bigger then 2, but lets keep it simple for now
    combinations = np.array(np.meshgrid(listOfArguments)).T.reshape(-1,2)
    print(combinations)
    # if a combination of 2 arguments is not in the relation its a conflict free set

    for combination in combinations:
        if combination not in attackRelations:
            if combination[::-1] not in attackRelations:
                conflictFreeSet.append(combination)
    for argument in listOfArguments:
        for relation in attackRelations:
            # if the argument is attacking himself, he is not part of the conflict free set
            if argument != relation[0] and argument != relation[1] and argument not in conflictFreeSet:
                conflictFreeSet.append(argument)    
    return conflictFreeSet

# def admissible(conflictFreeSet):
#     admissibleSet = [None, ]
#     for argumentSet in conflictFreeSet:
#         if 

conflictFreeSet = conflictFree()
print(conflictFreeSet)
print(attackRelations)
# admissible(conflictFreeSet)


''''
NOTES
This game is based on presentation 4 slide 22 and others around it
The game revolves around us the player playing an attacker to our games/ computers/ proponents arguments
If the computer cant find an attacker to our arguments ie an explentation as to why something is out we win
'''

# gameOn = True
# while gameOn:
#     print(f"The proponent plays argument {claimedArgument} which is labelled in")
#     listOfAttackers = attackers(claimedArgument)
#     # Check for attacker count, if there isnt anything, player loses
#     if len(listOfAttackers) == 0:
#         print(" - There are no arguments to attack with, you lose, better luck next time.")
#         gameOn = False
#     # Otherwise the game continues
#     else:
#         print("How would you like to attack?\n")
#         print(f"Your options are {listOfAttackers}")
#         argumentInput = input("Input your attacking argument: ")
#         if argumentInput in argumentsPlayer.keys():
#             # Remove the played argument so that the player cant play it again
#             del argumentsPlayer[argumentInput]
#             # Given on the picked argument,  find an attacker of that argument
#             print(f"You picked argument {argumentInput}")
#             print(f"'But then in your labelling it must also be the case that {claimedArgument}'s attacker {argumentInput} is labelled out. Based on which grounds?'\n")
#             # Try to find for the computer/ proponent a reasoning
#             listOfAttackers = attackers(argumentInput)
#             if len(listOfAttackers) == 0:
#                 print(f"- The proponent has no argumentation left, you win!")
#                 gameOn = False
#                 break
#             else:
#                 # Take random attacker to players argument
#                 claimedArgument = random.choice(listOfAttackers)
#                 print(f"'{argumentInput} is labelled out because {claimedArgument} is labelled in.'\n")
#         else:
#             print("Not a possible argument, please take one from the provided arguments")
#             print(list(arguments.keys()))

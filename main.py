import pandas as pd
from random import *
import numpy as np

pokemon = pd.read_csv("PokemonData\Pokemon.csv")
typeMulti = pd.read_csv(
    "PokemonData\AttackTypeMultipliers.csv")
allMoves = pd.read_csv("PokemonData\PokemonLearnableMoves.csv")
movesStats = pd.read_csv("PokemonData\PokemonMoves.csv")

# data = pokemon.iloc[0:2].values
# prints out the rows from first index to second indnex (exclusive) starting. the title row is not part of the index.

# might have to modify the pokemon name if there is a -
# pokemon_data = [index,
#                  "pokemon_name",
#                 ["type1", "type2"],
#                 {"hp": 10, "atk": 49},
#                 {
#                     "move1":
#                     {"accuracy": 75,
#                     "pp": 25,
#                     "effect": ["chance": 30, "effect": "flinch"],
#                   },
#                 "move2":
#                     {"accuracy": 75,
#                     "pp": 25}
#                 }]

# damage = ((2 * level + 10) / 250 * (attack(of attacking Pokemon) / defense(of defending Pokemon)) * base) + 2


class Pokemon:
    def __init__(self):
        self.index = int(random() * len(pokemon.index))
        self.name = pokemon.iloc[self.index].values[0]
        while ('-' in self.name or ' ' in self.name):
            self.index = int(random() * len(pokemon.index))
            self.name = pokemon.iloc[self.index].values[0]
        # print(self.name)
        self.effect = None
        self.types = pokemon.iloc[self.index].values[1].split("|")
        self.stats = {}
        stats_list = [x.split(":")
                      for x in pokemon.iloc[self.index].values[2].split("|")]
        for stat in stats_list:
            self.stats[stat[0]] = stat[1]
        moveset_index = allMoves[allMoves['Name']
                                 == self.name.lower()].index[0]
        possibleMoves = allMoves.iloc[moveset_index].values[1].split("|")
        if (len(possibleMoves) < 4):
            print("Please rerun program. Selected Pokemon has a moveset of less than 4.")
            exit()
        moveSet = sample(possibleMoves, 4)
        # print(moveSet)
        self.moves = {}
        for i in moveSet:
            moveIndex = movesStats[movesStats['Name'].apply(
                str.lower).str.replace('-', '').str.replace(' ', '') == i.lower()].index[0]
            self.moves[i] = {
                "accuracy": movesStats.iloc[moveIndex].values[1],
                "basePower": movesStats.iloc[moveIndex].values[2],
                "category": movesStats.iloc[moveIndex].values[3],
                "pp": movesStats.iloc[moveIndex].values[4],
                "type": movesStats.iloc[moveIndex].values[5],
                "effect": [x.split(":") for x in movesStats.iloc[moveIndex].values[6].split("|")],
            }
        # print(self.moves)

    def __str__(self):
        return ("Your " + self.types[0] + " type pokemon " + self.name +
                " has " + str(self.stats["hp"]) + " hp remaining.")

    def attack(self, p2):
        move = choice(list(self.moves))
        # print(move)
        # print("pp:")
        # print(self.moves[move]["pp"])

        if (self.moves[move]["pp"] <= 0):
            # print(self.moves[move]["pp"])
            print("There's no pp left for " + str(move) + "!")
            global turn
            print("\n" + "Turn " + str(turn) + ":")
            turn += 1
            return p2.attack(self)
        # elif (self.moves[move]["accuracy"].lower != "true"):
        #     if (int(random() * 100) > int(self.moves[move]["accuracy"])):
        #         print(self.name + " attack's missed!")
        else:
            # print(self.moves[move]["accuracy"].lower())
            if (self.moves[move]["accuracy"].isdigit()):
                if (int(random() * 100) > int(self.moves[move]["accuracy"])):
                    print(self.name + " used " + move + ", but it missed!")
                    return 0
            if (p2.effect == "brn"):
                print(p2.name + " was burned! It lost half its stats.")
                damage = ((2 * 1 + 10) / 250 * int(self.stats["atk"])/2 / int(
                    p2.stats["def"])/2 * int(self.moves[move]["basePower"])/2) + 2
            else:
                damage = ((2 * 1 + 10) / 250 *
                          int(self.stats["spa"]) / int(p2.stats["spd"]) * int(self.moves[move]["basePower"])) + 2
            if (self.moves[move]["category"].lower() == "status"):
                # print("THIS IS STATUS AND THIS WORKS1!!!!")
                damage = 0
            if (self.moves[move]["category"].lower() == "special"):
                # print("THIS IS SPECIAL AND THIS WORKS1!!!!")
                damage = ((2 * 1 + 10) / 250 *
                          int(self.stats["atk"]) / int(p2.stats["def"]) * int(self.moves[move]["basePower"])) + 2
            if (self.moves[move]["type"] in self.types):
                damage *= 1.25
            # p2.stats["hp"] = int(p2.stats["hp"]) - damage
            self.moves[move]["pp"] -= 1
            if (self.moves[move]["pp"] + 1 > 0):
                print(self.name + " attacked " + p2.name +
                      " with " + move + ". ")
            # else:
                # print("\n")
            effect = None
            if (len(self.moves[move]["effect"][0]) > 1):
                # print(self.moves[move]["effect"]) - [['chance', '20'], ['effect', 'confusion']]
                if (int(random() * 100) < int(self.moves[move]["effect"][0][1])):
                    effect = self.moves[move]["effect"][1][1]
                    p2.effect = effect
                    print("\n" + self.name + " gave " + p2.name +
                          " an effect of " + effect)
            if (damage == 0):
                print(self.name + " dealt no damage.")
            return damage
        return 0


pokemon1 = Pokemon()
pokemon2 = Pokemon()
multi = 1

p1_counter = 0
p2_counter = 0
changed1 = False
changed2 = False
turn = 0


def updateMulti(p1, p2):
    global multi
    # print(p1.types)
    # print(p2.types)
    for i in p1.types:
        for j in p2.types:
            multi *= typeMulti[typeMulti['Attack/Defense'] ==
                               str(i)].values[0].tolist()[typeMulti.columns.get_loc(j)]
    print("The current multiplier is " + str(multi) + "!")


def battle(p1, p2):
    p1_hp = int(p1.stats["hp"])

    p1_alive = True
    p2_hp = int(p2.stats["hp"])

    p2_alive = True
    # print(p1_hp, p2_hp)
    print("######## FIGHTERS ########")
    print(p1.name + " vs " + p2.name + "!")
    updateMulti(p1, p2)
    print("######### BEGIN! #########")

    while (p1_alive and p2_alive):
        global turn
        turn += 1
        print("\n" + "Turn " + str(turn) + ":")

        if (p1_hp <= 0):
            p1_alive = False
        if (p2_hp <= 0):
            p2_alive = False

        # if (p1.attack(p2)[1] is not 'None'): then p2 gets the effect
        # opposing pokemon gets the effect
        # flinch - skip a turn,
        # confusion - 50% chance attacks itself,
        # psn - 10% of hp lost,
        # brn - atk, def, spa, spd and spe stats are reduced by 50%,
        # frz - can't attack for 3 turns unless attacked by fire type,
        # slp - skips a turn unless hit by damage,
        # par - 50% chance the pokemon skips its turn
        if ((p1.effect is None and p2.effect is None) or (p1.effect == "brn") or (p2.effect == "brn")):
            if (p1.stats["spd"] > p2.stats["spd"]):

                dmg = int(p1.attack(p2))
                p2_hp -= dmg
                if (dmg != 0):
                    print(p2.name + " was directly hit for " + str(int(dmg)) +
                          " damage and has " + str(int(p2_hp)) + " remaining!")

                dmg = int(p2.attack(p1))
                p1_hp -= dmg
                if (dmg != 0):
                    print(p1.name + " was directly hit for " + str(int(dmg)) +
                          " damage and has " + str(int(p1_hp)) + " remaining!")
                # print(p2_hp)
            else:
                dmg = int(p2.attack(p1))
                p1_hp -= dmg
                if (dmg != 0):
                    print(p1.name + " was directly hit for " + str(int(dmg)) +
                          " damage and has " + str(int(p1_hp)) + " remaining!")

                dmg = int(p1.attack(p2))
                p2_hp -= dmg
                if (dmg != 0):
                    print(p2.name + " was directly hit for " + str(int(dmg)) +
                          " damage and has " + str(int(p2_hp)) + " remaining!")
                # print(p1_hp)
        else:
            if (p1.effect is not None):
                p = p1
            else:
                p = p2
            if (p.effect == "flinch"):
                p.effect = None
                print(p.name + " flinched and had its turn skipped!")

                if (p == p1):
                    dmg = int(p2.attack(p1))
                    p1_hp -= dmg
                    if (dmg != 0):
                        print(p1.name + " was directly hit for " + str(int(dmg)) +
                              " damage and has " + str(int(p1_hp)) + " remaining!")
                    else:
                        dmg = int(p1.attack(p2))
                        p2_hp -= dmg
                        if (dmg != 0):
                            print(p2.name + " was directly hit for " + str(int(dmg)) +
                                  " damage and has " + str(int(p2_hp)) + " remaining!")
                continue
            elif (p.effect == "confusion"):
                dmg = int(p1.attack(p2))
                if (int(random() * 100) < 50):
                    if (p == p1):
                        p1_hp -= dmg
                        print(p1.name + " accidentally damaged itself for " +
                              str(dmg) + " damage in confusionand has " + str(int(p1_hp)) + " hp left!")
                    else:
                        p2_hp -= dmg
                        print(p2.name + " accidentally damaged itself for " +
                              str(dmg) + " damage in confusion and has " + str(int(p2_hp)) + " hp left!")
            elif (p.effect == "psn"):
                if (p == p1):
                    dmg = int(p1.attack(p2))
                    p2_hp -= dmg
                    if (dmg != 0):
                        print(p2.name + " was directly hit for " + str(int(dmg)) +
                              " damage and has " + str(int(p2_hp)) + " remaining!")
                    p1_hp *= .9
                    print(p1.name + " was damaged to poisoned! It has " +
                          str(int(p1_hp)) + " hp left!")
                else:
                    dmg = int(p2.attack(p1))
                    p1_hp -= dmg
                    if (dmg != 0):
                        print(p1.name + " was directly hit for " + str(int(dmg)) +
                              " damage and has " + str(int(p1_hp)) + " remaining!")
                    p2_hp *= .9
                    print(p2.name + " was damaged to poisoned! It has " +
                          str(int(p2_hp)) + " hp left!")
            elif (p.effect == "frz"):
                global p1_counter, p2_counter, changed1, changed2
                if (p1_counter <= 0 and changed1 == True):
                    changed1 = False
                    p1.effect = None
                    continue
                elif (p2_counter <= 0 and changed2 == True):
                    changed2 = False
                    p2.effect = None
                    continue
                if (p == p1):
                    if (changed1 == False):
                        changed1 = True
                        p1_counter = 3

                        dmg = int(p2.attack(p1))
                        p1_hp -= dmg
                        if (dmg != 0):
                            print(p1.name + " was directly hit for " + str(int(dmg)) +
                                  " damage and has " + str(int(p1_hp)) + " remaining!")
                        if ("fire" in p2.types):
                            p1.effect = None
                            changed1 = False
                        continue
                    else:
                        p1_counter -= 1

                if (p == p2):
                    if (changed2 == False):
                        changed2 = True
                        p2_counter = 3

                        dmg = int(p1.attack(p2))
                        p2_hp -= dmg
                        if (dmg != 0):
                            print(p2.name + " was directly hit for " + str(int(dmg)) +
                                  " damage and has " + str(int(p2_hp)) + " remaining!")
                        if ("fire" in p2.types):
                            p2.effect = None
                            changed2 = False
                        continue
                else:
                    p2_counter -= 1
            elif (p.effect == "slp"):
                p.effect = None
                continue
            elif (p.effect == "par"):
                if (p == p1):
                    if (int(random()) * 100 > 50):
                        print(p.name + " was paralyzed and had its turn skipped!")
                        dmg = int(p2.attack(p1))
                        p1_hp -= dmg
                        if (dmg != 0):
                            print(p1.name + " was directly hit for " + str(int(dmg)) +
                                  " damag and has " + str(int(p1_hp)) + " remaining!")
                        continue
                elif (p == p2):
                    if (int(random()) * 100 < 50):
                        print(
                            p.name + " was paralyzed and had its turn skipped!")
                        dmg = int(p1.attack(p2))
                        p2_hp -= dmg
                        if (dmg != 0):
                            print(p2.name + " was directly hit for " + str(int(dmg)) +
                                  " damage and has " + str(int(p2_hp)) + " remaining!")
                        continue

    print("\nGame Over!")
    if (p1_hp > 0):
        print(p1.name + " has won the battle!")
    elif (p2_hp > 0):
        print(p2.name + " has won the battle!")


battle(pokemon1, pokemon2)

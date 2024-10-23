import sys
import csv
import re
from os import sep, path

DATA_DIR = path.dirname(path.realpath(sys.argv[0])) + sep + "data" + sep


def loadStatScale():
    f = open(DATA_DIR + "statScale.csv", 'r')
    reader = csv.reader(f)
    header = next(reader, None)
    header.pop(0)
    data = list(list(row) for row in csv.reader(f, delimiter=","))
    statScale = {}
    for row in data:
        statScale[float(row[0])] = {}
        for i in range(len(header)):
            statScale[float(row[0])][header[i]] = int(row[i+1])
    return statScale


def getCr(promptStr):
    while True:
        try:
            cr = float(input("%s: " % promptStr))
            assert cr >= 0 and cr <= 30
            break
        except ValueError:
            print("CR must be a number.\n")
        except AssertionError:
            print("CR must be between 0 and 30, inclusive.\n")
    return cr


def getCoreStats():
    while True:
        try:
            coreStats = input(
                "Enter the monster's current stats (separated by commas) in the following order.\nArmour, HP: ")
            coreStats = coreStats.replace(" ", "").split(",")
            assert len(coreStats) == 2
            coreStats = {"ac": int(coreStats[0]), "hp": int(
                coreStats[1])}
            break
        except AssertionError:
            print(
                "Please enter 2 comma separated values for Armour and HP (respectively).\n")
        except ValueError:
            print("Each stat must be an integer.\n")
    return coreStats


def getSecondaryStatCommand():
    while True:
        command = input("Command: ").lower().replace(' ', '')
        if command == "exit":
            return None
        validCommands = {"damage", "defence"}
        match = re.match(r"([a-z]+)([0-9]+)", command, re.I)
        isValidCommand = match
        if match:
            command, commandValue = match.groups()
            command = command.replace('dmg', 'damage')
            command = command.replace('def', 'defence')
            isValidCommand = command in validCommands
        if not isValidCommand:
            print("Invalid command (" + command + "), must be one of " +
                  str(validCommands) + ", followed by a number")
            continue
        return command, int(commandValue)


def scaleCoreStats(oldCr, newCr, currCores):
    newCores = {}
    newCores["ac"] = scaleAbsoluteStat(oldCr, newCr, currCores["ac"], "ac")
    newCores["hp"] = scalePercentageStat(oldCr, newCr, currCores["hp"], "hp")
    return newCores


def scalePercentageStat(oldCr, newCr, currValue, stat):
    mod = currValue/STAT_SCALE[oldCr][stat]
    return round(STAT_SCALE[newCr][stat]*mod)


def scaleAbsoluteStat(oldCr, newCr, currValue, stat):
    diff = STAT_SCALE[newCr][stat] - STAT_SCALE[oldCr][stat]
    return round(currValue + diff)


if __name__ == "__main__":
    STAT_SCALE = loadStatScale()

    while True:
        currCr = getCr("\nEnter the monster's current CR to begin")
        newCr = getCr("Enter the new CR to scale the monster to")

        currCores = getCoreStats()
        newCores = scaleCoreStats(currCr, newCr, currCores)
        print("Your new core stats:\nArmour: %s\nHP: %s" %
              (newCores["ac"], newCores["hp"]))

        print("\nYou can now scale damage and other defences. Enter one of the following commands: 'damage' (or 'dmg'), 'defence' (or 'def'), 'exit',\n\t"
              " followed by the relevant number (e.g. def 3).")
        while True:
            commandTuple = getSecondaryStatCommand()
            if commandTuple is None:
                break
            cmd, currValue = commandTuple
            newValue = 0
            match cmd:
                case "damage":
                    newValue = scalePercentageStat(currCr, newCr, currValue, cmd)
                case "defence":
                    newValue = scaleAbsoluteStat(currCr, newCr, currValue, cmd)
            print("Your scaled %s is %i\n" % (cmd, newValue))

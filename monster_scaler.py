import sys, csv, math, re
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
      cr = float(input("%s: " %promptStr))
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
      coreStats = input("Enter the monster's current stats (separated by commas) in the following order.\nAC, HP, AB: ")
      coreStats = coreStats.replace(" ", "").split(",")
      assert len(coreStats) == 3
      coreStats = {"ac": int(coreStats[0]), "hp": int(coreStats[1]), "ab": int(coreStats[2])}
      break
    except AssertionError:
      print("Please enter 3 comma separated values for AC, HP, and AB (respectively).\n")
    except ValueError:
      print("Each stat must be an integer.\n")
  return coreStats

def getSecondaryStatCommand():
  while True:
    command = input("Command: ").lower().replace(' ', '')
    if command == "exit":
      return None
    validCommands = {"damage", "dc"}
    match = re.match(r"([a-z]+)([0-9]+)", command, re.I)
    isValidCommand = match
    if match:
      command, commandValue = match.groups()
      isValidCommand = command in validCommands
    if not isValidCommand:
      print("Invalid command (" + command + "), must be one of " + str(validCommands) + ", followed by a number")
      continue
    return command, int(commandValue)

def scaleCoreStats(oldCr, newCr, currCores):
  newCores = {}
  for stat in ("ac", "hp", "ab"):
    newCores[stat] = scaleStat(oldCr, newCr, currCores[stat], stat)
  return newCores

def scaleStat(oldCr, newCr, currValue, stat):
  mod = currValue/STAT_SCALE[oldCr][stat]
  return math.floor(STAT_SCALE[newCr][stat]*mod)

if __name__ == "__main__":
  STAT_SCALE = loadStatScale()

  while True:
    currCr = getCr("\nEnter the monster's current CR to begin")
    newCr = getCr("Enter the new CR to scale the monster to")

    currCores = getCoreStats()
    newCores = scaleCoreStats(currCr, newCr, currCores)
    print("Your new core stats:\nAC: %s\nHP: %s\nAB: %s" % (newCores["ac"], newCores["hp"], newCores["ab"]))

    print("\nYou can now scale damage and save DCs. Enter one of the following commands: 'damage', 'dc', 'exit',\n\t"
          " followed by the relevant number (e.g. DC15).")
    while True:
      commandTuple = getSecondaryStatCommand()
      if commandTuple is None:
        break
      cmd, currValue = commandTuple
      newValue = scaleStat(currCr, newCr, currValue, cmd)
      print("Your scaled %s is %i\n" % (cmd, newValue))

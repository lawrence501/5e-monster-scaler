import sys, csv, math

DATA_DIR = "./data/"

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
      coreStats = {"AC": int(coreStats[0]), "HP": int(coreStats[1]), "AB": int(coreStats[2])}
      break
    except AssertionError:
      print("Please enter 3 comma separated values for AC, HP, and AB (respectively).\n")
    except ValueError:
      print("Each stat must be an integer.\n")
  return coreStats
  
def scaleCoreStats(oldCr, newCr, currCores):
  newCores = {}
  for stat in ["AC", "HP", "AB"]:
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
    print("Your new core stats:\nAC: %s\nHP: %s\nAB: %s" %(newCores["AC"], newCores["HP"], newCores["AB"]))

    print("\nYou can now scale damage and save DCs. Enter one of the following commands: 'damage', 'DC', 'exit'.")
    while True:  
      cmd = input("Command: ")
      if cmd == "exit":
        break
      else:
        validCommands = ["damage", "DC"]
        try:
          assert cmd in validCommands
        except AssertionError:
          print("Invalid command.")
          continue

        currValue = 0
        while True:
          try:
            currValue = int(input("Current value: "))
            break
          except ValueError:
            print("Current value must be an integer.\n")
        newValue = scaleStat(currCr, newCr, currValue, cmd)
        print("Your scaled %s is %i\n" %(cmd, newValue))      

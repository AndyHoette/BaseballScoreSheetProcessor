import sys, os, re


class player:
    def __init__(self, name):
        self.name = name
        self.ab = 0
        self.h = 0

    def __str__(self):
        if self.ab == 0:
            return self.name + ": 0.000"
        return f"{self.name}: {self.h / self.ab:.3f}"

    def addGame(self, ab, h):
        self.ab += int(ab)
        self.h += int(h)

    def getBattingAverage(self):
        if self.ab == 0:
            return 0
        return round(self.h / self.ab, 3)

    def getName(self):
        return self.name


wordsRegex = r'^\w+\s\w+'
numbersRegex = r'\d+'

global players
players = []


def playerExists(name):
    for p in players:
        if p.getName() == name:
            return p
    return None


def parse(s):
    gameWords = re.findall(wordsRegex, s)
    gameNumbers = re.findall(numbersRegex, s)
    if len(gameWords) != 1 or len(gameNumbers) != 3:
        return
    playerName = gameWords[0]
    playerAB = gameNumbers[0]
    playerH = gameNumbers[1]
    potentialPlayer = playerExists(playerName)
    if potentialPlayer is None:
        potentialPlayer = player(playerName)
    potentialPlayer.addGame(playerAB, playerH)
    if potentialPlayer not in players:
        players.append(potentialPlayer)


if len(sys.argv) < 2:
    sys.exit(f"Usage: {sys.argv[0]} <filename>")

filename = sys.argv[1]

if not os.path.isfile(filename):
    sys.exit(f"File {filename} not found")

with open(filename) as f:
    for line in f:
        parse(line)

players.sort(key=lambda p: p.getBattingAverage(), reverse=True)
for p in players:
    print(p)

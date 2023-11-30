"""
main.py
Entry point for the program
"""

import yaml
from utils.solver import AStarSolver, UtilityDrivenSolver

# RoadTrip
# Creates an AStarSolver object and passes required parameters
# Params: startLoc (string), goalLoc (string), LocFile (string), EdgeFile (string), resultFile (string)
def RoadTrip(startLoc, goalLoc, LocFile, EdgeFile, resultFile):
    solver = AStarSolver(locFilePath=LocFile, edgeFilePath=EdgeFile, startLoc=startLoc, goal=goalLoc, resultFilePath=resultFile)
    solver.solve()

# RoadTrip
# Creates an AStarSolver object and passes required parameters
# Params: startLoc (string), goalLoc (string), LocFile (string), EdgeFile (string), resultFile (string)
def RoundTripRoadTrip(startLoc, LocFile, EdgeFile, PrefFile, maxTime, x_mph, resultFile):
    solver = UtilityDrivenSolver(locFilePath=LocFile, edgeFilePath=EdgeFile, prefFilePath=PrefFile, startLoc=startLoc, goal=startLoc, resultFilePath=resultFile, maxTime=maxTime, x_mph=x_mph)
    solver.solve()

# main
# Opens config.YAML and sets the parameters of the search
# Entry point of the program.
def main():
    with open('config.YAML', 'r') as file:
        config = yaml.safe_load(file)
    locFilePath = config['locationFile']
    edgeFilePath = config['edgeFile']
    prefFilePath = config['prefFile']
    start = config['startLoc']
    resultFilePath = config['resultFile']
    maxTime = config['maxTime']
    x_mph = config['x_mph']

    RoundTripRoadTrip(start, locFilePath, edgeFilePath, prefFilePath, maxTime, x_mph, resultFilePath)


if __name__ == '__main__':
        main()
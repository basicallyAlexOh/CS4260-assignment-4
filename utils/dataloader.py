"""
dataloader.py
Classes: Dataloader
Purpose: Provides the utilities needed to load data into nodes and edges from CSV files.
"""
import csv
import random
import yaml
from structs.node import Node
from structs.edge import Edge
from collections import defaultdict
from customML.NeuralNetwork.nnrunner import NNRunner
from customML.Dataloader.dataloader import Dataloader as DL

class Dataloader:

    # __init__
    # Constructor - instantiates an object of Dataloader given the path to the file.
    # Params: locFile (string), edgeFile (string)
    def __init__(self, locFile: str, edgeFile: str, prefFile: str, speed: float = 0.0):
        try:
            self.__locFile = open(locFile, 'r')
            self.__edgeFile = open(edgeFile, 'r')
            self.__prefFile = open(prefFile, 'r')
        except:
            raise Exception("File not found...")

        with open('config.YAML', 'r') as file:
            config = yaml.safe_load(file)

        self.themes = list(csv.reader(self.__prefFile, delimiter='\t'))[0][1:]
        self.numThemes = len(self.themes)

        myData = DL(prefFile)
        runner = NNRunner(config['num_folds'], numInputs=self.numThemes, hiddenLayers=config['hidden_layers'], numOutputs=1, epochs=config['epochs'], lr=config['lr'])
        runner.run(myData.utilList, myData.utilList)


        self.NN = runner.getBestNN()
        self.nodeList = []
        self.nodeDict = {}
        self.edgeList = []
        self.speed = speed

        random.seed(0)
        self.generatePreferences(config)
        self.__readCSV()


    # readCSV (Private)
    # Reads the CSV files and constructs the node list and the edge list.
    # Will print out invalid locations and edges.
    # NOTE: will output on invalid lines of the input.
    def __readCSV(self):
        with self.__locFile as locCSV:
            reader = csv.reader(locCSV, delimiter=',')
            for row in reader:
                try:
                    lat = float(row[1])
                    lon = float(row[2])
                    if row[0] in self.scores:
                        pref = self.scores[row[0]]
                    else:
                        pref = 0
                    print(row[0] + ": " + str(pref))
                    self.nodeList.append(Node(row[0], lat, lon, pref))
                    self.nodeDict.update({row[0]: Node(row[0], lat, lon, pref)})
                except:
                    print("Not a valid location: " + row[0])

        with self.__edgeFile as edgeCSV:
            reader = csv.reader(edgeCSV, delimiter=',')
            for row in reader:
                try:
                    dist = float(row[3])
                    if row[0] in self.scores:
                        pref = self.scores[row[0]] * 0.1
                    #     Edge weights will be multiplied by 0.1
                    else:
                        pref = 0
                    print(row[0] + ": " + str(pref))
                    self.edgeList.append(Edge(row[0], self.nodeDict[row[1]], self.nodeDict[row[2]], dist, float(pref), self.speed))
                except:
                    print("One or more locations are invalid: " + row[1] + " " + row[2])

    def generatePreferences(self, config):
        themeReader = csv.reader(open(config['themeFile'], 'r'), delimiter="\t")
        attractionReader = csv.reader(open(config['attractionFile'], 'r'), delimiter="\t")
        themeList = []
        attractionList = []
        for row in themeReader:
            themeList.append(row[0])
        for row in attractionReader:
            try:
                themes = row[3].split(', ')
                for theme in themes:
                    if theme not in themeList:
                        themeList.append(theme)
                attractionList.append((row[0], row[1], themes))
            except:
                print("Failed on:" + str(row))
                print(len(row))

        locationDict = defaultdict(list)
        locationList = []
        for item in attractionList:
            if item[1] not in locationList:
                locationList.append(item[1])
            locationDict[item[1]].append((item[0], item[2]))


        random.shuffle(locationList)

        self.scores = defaultdict()

        for loc in locationList:
            themeCount = [0] * self.numThemes
            for attraction in locationDict[loc]:
                themes = attraction[1]
                for theme in themes:
                    if theme in self.themes:
                        themeCount[self.themes.index(theme)] += 1
            score = self.NN.predict(themeCount)[0]
            self.scores[loc] = score

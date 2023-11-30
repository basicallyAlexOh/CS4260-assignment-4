from collections import defaultdict
import random
import csv
import yaml


def main():
    with open('config.YAML', 'r') as file:
        config = yaml.safe_load(file)
    print("Getting User Preferences...")
    try:
        themeFile = open(config["themeFile"], 'r')
        attractionFile = open(config["attractionFile"], 'r')
    except:
        raise Exception("File not found...")

    outname = str(input("Name of file to be saved:"))
    outFile = open("./data/" + outname + '.csv', 'w')
    outWriter = csv.writer(outFile, delimiter='\t')


    themeReader = csv.reader(themeFile, delimiter="\t")
    attractionReader = csv.reader(attractionFile, delimiter="\t")
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

    print("Listing Themes...")
    for item in themeList:
        print(item)


    prefThemes = input("Enter up to 5 themes that you would like to explore (each word separated by a comma and space")
    prefThemes = prefThemes.split(', ')

    random.shuffle(locationList)
    count = 0

    outWriter.writerow(["score"] + prefThemes)

    for loc in locationList:
        themeCount = [0] * len(prefThemes)
        for attraction in locationDict[loc]:
            themes = attraction[1]
            for theme in themes:
                if theme in prefThemes:
                    themeCount[prefThemes.index(theme)] += 1
        if sum(themeCount) != 0:
            print("Rate this location and attractions from 0 - 10")
            print(loc)
            for attraction in locationDict[loc]:
                themes = attraction[1]
                for theme in themes:
                    if theme in prefThemes:
                        print(attraction[0] + ": " + str(themes))
                        break
            score = int(input("Enter your score here as an integer between 0 and 10 inclusive")) / 10
            if score > 10:
                score = 10
            elif score < 0:
                score = 0

            outWriter.writerow([score] + themeCount)
            count += 1

        if count == config["maxSamples"]:
            break



if __name__ == "__main__":
    main()
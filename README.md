# CS4260-assignment-4
Final Project for CS 4260

Problem Statement: Devise a program to perform anytime utility driven search for a round trip given a starting location and maximum time. 
This program should use past data to generate a machine learning model to assign appropriate edge weights and they should be dynamically assessed in relation to the rest of the path that has been developed already. 
The algorithm should penalize a path for having too many of one theme. An important note is that the weighting should not be updated on the original graph, but must be tracked in the path itself, as one path should not change the entire graph. 
Even after a suitable solution has been found, alternative solutions should be explored to give the user options.

Two Main Objectives
1) Using a machine learning model in order to assign weights to the different attractions, and thus edges.
2) Use dynamic weighting of edges as new states are developed to avoid too much of one specific area (theme).


How to run:
1) Activate the virtual environment in /env
2) Change the /config.YAML file for your training parameters
3) Run generatePref.py to create the user's preferences
4) Change the prefFile in /config.YAML to point to your preferences that you just made
5) Run main.py to run the anytime solver.

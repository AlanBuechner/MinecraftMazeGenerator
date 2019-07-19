#!/usr/bin/env python
from maze import *
import argparse

# argparse parsing
parser = argparse.ArgumentParser(description="Minecraft Maze Generator")
parser.add_argument('-w', '--width', type=int, metavar='', help="the width of the maze") # argument for the width of the maze
parser.add_argument('-l', '--length', type=int, metavar='', help="the length of the maze") # argument for length of the maze
parser.add_argument('-s', '--spawn', type=str, metavar='', help="the location you want to spawn it") # whare to spawn if you want to spawn
parser.add_argument('-st', '--start', action='store_true', help="get teleported to the start of the maze and start the timer") # to start the maze
parser.add_argument('-S', '--save', type=str, metavar='', help="the file you want to save the maze to") # load the maze form a file
parser.add_argument('-L', '--load', type=str, metavar='', help="the file you want to load the maze form") # save the maze to a file
group = parser.add_mutually_exclusive_group()
# verbosity
group.add_argument('-v', '--verbose',action='store_true', help="verbose print")
group.add_argument('-vv', '--doubleverbose',action='store_true', help="double verbose print")
args = parser.parse_args() # parse the arguments

mc = Minecraft.create() # create a conection to minecraft

def main():
    verbosity = 0
    if(args.verbose):
        verbosity = 1
    if(args.doubleverbose):
        verbosity = 2

    haseMaze = False
    maze = MazeData()
    if(args.load != None):
        if(args.width != None or args.length != None):
            print("loding dose not requier maze dimentions")
            return
        else:
            maze.load(args.load)
            haseMaze = True

    if(args.width != None and args.length != None):
        maze = genMaze(args.width, args.length, verbosity)
        haseMaze = True
    else:
        if(args.width != None):
            print("length of maze is needed to generat a maze")
            return
        if(args.length != None):
            print("width of maze is needed to generat a maze")
            return

    if(args.spawn != None):
        if(haseMaze == False):
            print("a maze is needed to spaw")
            return
        else:
            x = 0
            y = 0
            z = 0
            if(args.spawn == "player"):
                pos = mc.player.getPos()
                x = pos.x
                y = pos.y
                z = pos.z
            else:
                pos = split(args.spawn, ',')
                x = int(pos[0])
                y = int(pos[1])
                z = int(pos[2])
            maze.spawn(Vector(x, y, z), 1, mc)

    if(args.save != None):
        if(haseMaze == False):
            print("a maze is needed to save to a file")
            return
        else:
            maze.save(args.save)

    if(args.start):
        if(haseMaze == False):
            print("a maze is needed to start the game")
            return
        if(args.spawn == None):
            print("a maze needes to be spawend in to wold to start the game")
            return
        maze.startGame(mc)

if(__name__ == "__main__"):
    main()

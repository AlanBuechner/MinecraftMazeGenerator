from mcpi.minecraft import Minecraft
import random
import time

# verbose printing
def verbos_print(msg, msgverbosity, verbosity):
    # print messege if the verbosity is high enough
    if(msgverbosity <= verbosity):
        print(msg)

# vector class
class Vector():
    def __init__(self, x, y, z):
        # x, y and z components
        self.x = x
        self.y = y
        self.z = z

    # add 2 vectors together
    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    # translate the vector to another socation
    def translate(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    # scale the vector
    def scale(self, s):
        self.x *= s
        self.y *= s
        self.z *= s

    # returns wether or not the vector is negitive
    def isNeg(self):
        if(self.x < 0 or self.y < 0 or self.z < 0):
            return True
        return False

    # copys the vector
    def copy(self):
        return Vector(self.x, self.y, self.z)

# line class 
class Line():
    def __init__(self, v1, v2):
        # vertices for the line
        self.vec1 = v1
        self.vec2 = v2

# stack class
class Stack():
    def __init__(self):
        # elements in the stack
        self.stack = []

    # puts new element on the top of the stack
    def push(self, obj):
        self.stack.append(obj)

    # removes the top element from the stack
    def pop(self):
        val = self.stack[-1:]
        self.stack = self.stack[:-1]
        return val

    # returns the top element on the stack
    def peek(self):
        return self.stack[-1:][0]

# the Data for the maze
class MazeData():
    def __init__(self):
        self.width = 0 # width of the maze
        self.length = 0 # length of the maze
        self.end = None # endpoint of the maze
        self.maze = [] # shape of the maze
        location = None # location of the maze when spawed

    def spawn(self, pos, blockId, handle):
        handle.setBlocks(pos.x, pos.y, pos.z, pos.x+(self.width*2), pos.y+2,
                         pos.z+(self.length*2), blockId)

        for i in self.maze:
            first = i.vec1.copy()
            sec = i.vec2.copy()
            
            first.x *= 2
            first.z *= 2
            sec.x *= 2
            sec.z *= 2

            first.translate(pos.x+1, pos.y+1, pos.z+1)
            sec.translate(pos.x+1, pos.y+3, pos.z+1)
            
            handle.setBlocks(first.x, first.y, first.z, sec.x, sec.y, sec.z, 0)

        end = self.end

        handle.setBlock(pos.x+1, pos.y, pos.z+1, 35, 5)
        handle.setBlock((end.x*2)+pos.x+1,(end.y*2)+pos.y, (end.z*2)+pos.z+1, 35, 14)
        self.location = pos

    def startGame(self, handle):
        pos = self.location
        handle.player.setPos(pos.x+1, pos.y+1, pos.z+1)

        endx = int((self.end.x*2) + pos.x+1)
        endy = int((self.end.y*2) + pos.y+1)
        endz = int((self.end.z*2) + pos.z+1)

        start = time.time()
        
        playing = True
        while playing:
            x = int(handle.player.getPos().x)
            y = int(handle.player.getPos().y)
            z = int(handle.player.getPos().z)

            if(x == endx and y == endy and z == endz):
                playing = False

        end = time.time()
        timeElapsed = end - start
        handle.postToChat("cangrats you completed the maze in "+ str(int(timeElapsed)) +" secends")

    def save(self, filePath):
        with open(filePath, 'w', encoding = 'utf-8') as f:
            f.seek(0,0)
            f.write(str(self.width)+'\n')
            f.write(str(self.length)+'\n')
            f.write(str(self.end.x)+","+str(self.end.z)+'\n')

            for l in self.maze:
                f.write(str(l.vec1.x)+","+str(l.vec1.z)+","+str(l.vec2.x)+","+str(l.vec2.z)+'\n')

    def load(self, filePath):
        with open(filePath, 'r') as f:
            self.width = int(f.readline())
            self.length = int(f.readline())
            endverts = f.readline().split(',')
            self.end = Vector(int(endverts[0]),0, int(endverts[1]))
            lines = f.readlines()
            for line in lines:
                verts = line.split(',')
                v1 = Vector(int(verts[0]),0, int(verts[1]))
                v2 = Vector(int(verts[2]),0, int(verts[3]))
                self.maze.append(Line(v1, v2))
                print(str(v1.x)+','+str(v1.z)+','+str(v2.x)+','+str(v2.z))


# generates the maze
def genMaze(width, length, v):
    verbos_print("Error checking", 1, v)
    # Error checking
    # checks if the maze dimentions are valid
    if(not(width > 1 and length > 1)):
        print("invalid maze dimentions")
        return 0

    verbos_print("Initalizing", 1, v)
    # Initialize
    # careat a mazedata object
    mazeData = MazeData()
    # sets the width and length of the maze
    mazeData.width = width
    mazeData.length = length
    depth = 1 # how far into the maze
    longestDepth = depth # ferthest length form the start
    end = None # end of the maze
    maze = Stack() # pathe taken to get to the current point in the maze
    maze.push(Vector(0,0,0)) # start the maze

    visitedCount = 1 # the amount of elements in the maze that have be visited
    visited = [] # 2d array storing wither or not the element was visited
    # initialize each element with False
    for i in range(width):
        layer = []
        for l in range(length):
            layer.append(False)
        visited.append(layer)
    visited[0][0] = True # set the start of the maze as visited

    # all posible directions to move in
    directions = [Vector(1 ,0, 0),
                      Vector(-1,0, 0),
                      Vector(0 ,0, 1),
                      Vector(0 ,0,-1)]

    verbos_print("Generating Maze", 1, v)
    # generate maze
    while(visitedCount < width*length):
            
        #get current position
        curr = maze.peek()
        # find valid position to move in
        direction = 0
        valid = False
        tried = [False,
                 False,
                 False,
                 False]
        while valid == False:
            # check for if all Moves have Been tried
            new = None # new element that we are moving to
            # chekcs if all directions have been tried
            count = 0
            for i in range(4):
                if(tried[i] == True):
                    count += 1
            if(count == 4):
                verbos_print("No valid move", 2, v)
                curr = maze.pop() # moves back one element on the maze
                depth -= 1 # decrements the depth
                break
            # pick a random direction to atempt to move in
            moveintry = random.randint(0,3)
            # check if direction has already be tried
            if(tried[moveintry] == True):
                continue # try another direction
            else:
                # check if the move is valid
                # get the new postion in the maze
                movein = directions[moveintry]
                new = curr.add(movein)
                verbos_print("atempting point: "+str(new.x)+","+str(new.z), 3, v)
                # checks if out of the maze bounderys
                if(not new.isNeg()):
                    if(new.x < width and new.z < length):
                        # checks if location has already been visetid
                        if(visited[new.x][new.z] == False):
                            valid = True
                            verbos_print(str(new.x)+","+str(new.z)+": Valid Move", 2, v)
                            break
                        else:
                            verbos_print(str(new.x)+","+str(new.z)+": Invalid Move alredy viseted", 2, v)
                    else:
                        verbos_print(str(new.x)+","+str(new.z)+": Invalid Move out side maze bounderys over", 2, v)
                else:
                    verbos_print(str(new.x)+","+str(new.z)+": Invalid Move out side maze bounderys neg", 2, v)
            if(valid == False):
                tried[moveintry] = True
                    
        if(valid == True):
            # increses visited count
            visitedCount += 1
            depth += 1 # increses the depth
            # makes the end = the to new point if it is at a ferther depth into the maze than the current end
            if(depth > longestDepth):
                end = new.copy()
                longestDepth = depth
            # markes the point as visited
            visited[new.x][new.z] = True
            # makes a connection between the current point and last point on the maze
            prev = maze.peek()
            mazeData.maze.append(Line(new, prev))
            # updates the current point on the maze
            maze.push(new)

    mazeData.end = end
    return mazeData
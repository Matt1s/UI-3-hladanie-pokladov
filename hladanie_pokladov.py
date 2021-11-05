from random import randint

# Declaring variables
grid_x = 0
grid_y = 0
start_x = 0
start_y = 0
treasures = []

# Number of entities in single generation
N_IN_GENERATION = 100
MAX_INSTRUCTIONS = 500

generation = []

start_pos = [0,0]


# Function to read input from files
def read_file(route):
    global grid_x, grid_y, start_x, start_y, treasures, start_pos
    # Read-only open
    f = open(route, "r")

    line_index = 0

    grid_size = ""

    # Reading lines from files
    for line in f:
        line = line[:-1]
        if(line_index == 0):
            # Grid size
            grid_size = line.split(" ")
        elif(line_index == 1):
            # Player initial position
            start_pos = line.split(" ")
        elif(line_index == 2):
            pass
        else:
            # Location of treasures
            treasure_location = line.split(" ")
            if( len(treasure_location) == 2 ): # Caring about EOF
                treasures.append([int(treasure_location[0]), int(treasure_location[1])])

        line_index += 1

    # Initializing global variables
    grid_x = int(grid_size[0])
    grid_y = int(grid_size[1])

    start_x = int(start_pos[0])
    start_y = int(start_pos[1])

    # Closing files
    f.close()

read_file('./vstup.txt')
print("Rozmer mriežky:",grid_x, grid_y)
print("Štart:",start_x, start_y)
print("Počet pokladov:", len(treasures))
print("Poklady:",treasures)

class Generation():
    entities = []

class Entity():
    def __init__(self):
        self.genome = []
        self.fitness = 0
        self.prints = []

    def addDirection(self,bits):
        direction = ""
        if(bits == '00'):
            direction = "H"
        elif(bits == '01'):
            direction = "D"
        elif(bits == '10'):
            direction = "P"
        elif(bits == '11'):
            direction = "L"
        self.prints.append(direction)


def VM(index, entity):
    i = 0
    for i in range(len(entity.genome)):

        if(MAX_INSTRUCTIONS > 500):
            print("Too many instructions!")
            return
        #print("Jedinec:",index,"gén:",i,"inštrukcia",gene[0:2])

        instruction = entity.genome[i][:2]
        if(instruction == '00'):
            # Increment
            print("INCREMENT")
            improved_gene = bin(int(entity.genome[i],2) + 1)[2:].zfill(8)
        if(instruction == '00'):
            # Decrement
            print(entity.genome[i])
            print("DECREMENT")
            improved_gene = bin(int(entity.genome[i],2) - 1)[2:].zfill(8)
            print(improved_gene)
        if(instruction == '01'):
            print("JUMP")
            # Jump on next gene
            print(entity.genome[i])
            # Get last 6 characters from variable gene
            jump_gene = int(entity.genome[i][-6:])
            i = jump_gene
            print(jump_gene)
            break
        if(instruction == '11'): # Instruction PRINT
            #print(i, entity.genome[i])
            print("PRINT")
            direction = entity.genome[i][-2:]
            entity.addDirection(direction)
        i+=1
    #print(entity.prints)

found_treasures = []

def checkTreasure(entity):
    global treasures
    for treasure in treasures:
        if(start_x == treasure[0] and start_y == treasure[1]):
            for found_treasure in found_treasures:
                if(found_treasure == treasure):
                    return False
            print("Treasure found!", treasure)
            found_treasures.append([treasure[0], treasure[1]])
            entity.fitness += 1
            return True
    return False

def movePlayer(direction):
    global start_x, start_y
    if(direction == "H"):
        if(start_y == 0):
            return False
        else:
            start_y -= 1

    elif(direction == "D"):
        if(start_y == grid_y-1):
            return False
        else:
            start_y += 1

    elif(direction == "P"):
        if(start_x == 0):
            return False
        else:
            start_x -= 1

    elif(direction == "L"):
        if(start_x == grid_x-1):
            return False
        else:
            start_x += 1
    else:
        print("Error")
    
def rateEntity(entity):
    global start_x, start_y, start_pos
    moves = entity.prints
    for move in moves:
        if(move == "H"):
            movePlayer("H")
        elif(move == "D"):
            movePlayer("D")
        elif(move == "P"):
            movePlayer("P")
        elif(move == "L"):
            movePlayer("L")
        else:
            print("Error")
        checkTreasure(entity)
    if(len(found_treasures) == len(treasures)):
        # This entity is the winner
        return True
    else:
        found_treasures.clear()
        start_x = int(start_pos[0])
        start_y = int(start_pos[1])

    


# Generating initial population
for count in range(N_IN_GENERATION):
    # Generating entity
    entity = Entity()
    entity.genome = []
    for i in range(64):
        # Generating random gene from 0 to 255
        gene_int = randint(0,255)
        gene_bin = bin(gene_int)[2:].zfill(8)

        # Adding genome to entity
        entity.genome.append(gene_bin)

    # Adding entity into generation
    generation.append(entity)

print("Počet jedincov v generácii: ",len(generation))
index = 0
for entity in generation:
    VM(index, entity)
    index += 1
    rateEntity(entity)
    print("Jedinec:",i,"Fitness:", entity.fitness)

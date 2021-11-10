from random import randint
import time
import math

# Declaring variables
grid_x = 0
grid_y = 0
start_x = 0
start_y = 0
treasures = []

# Number of entities in single generation
N_IN_GENERATION = 100
MAX_INSTRUCTIONS = 500

# Number of max possible generations
MAX_GENERATIONS = 10000

# Mutation rate in percent
MUTATION_RATE = 2

# Setting contants for genetic algorithm
N_ELITES = 20
N_PARENTS = 60
NEW_ENTITIES_COUNT = 10

# Coutn number of steps in order to calculate fitness - not working better though
COUNT_STEPS = False

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


def VM(entity):
    i = 0
    for i in range(len(entity.genome)):

        # Caring for loop in VM
        if(i > MAX_INSTRUCTIONS):
            print("Too many instructions!")
            return

        instruction = entity.genome[i][:2]
        if(instruction == '00'):
            # Increment
            if(int(entity.genome[i]) == 255):
                entity.genome[i] = '00000000'
                print("Increment overflow!")
            else:
                entity.genome[i] = bin(int(entity.genome[i],2) + 1)[2:].zfill(8)

        if(instruction == '00'):
            # Decrement
            if(bin(int(entity.genome[i],2)) == 0):
                entity.genome[i] = '11111111'
                print("Decrement overflow!")
            else:
                entity.genome[i] = bin(int(entity.genome[i],2) - 1)[2:].zfill(8)
                
        if(instruction == '01'):
            # Get last 6 characters from variable gene
            jump_gene = int(entity.genome[i][-6:])
            i = jump_gene
            break

        if(instruction == '11'): # Instruction PRINT
            direction = entity.genome[i][-2:]
            entity.addDirection(direction)

        i+=1

found_treasures = []

def checkTreasure(entity):
    global treasures
    for treasure in treasures:
        # Looping through treasures
        if(start_x == treasure[0] and start_y == treasure[1]):
            # Treasure found
            for found_treasure in found_treasures:
                # If this treasure was found before
                if(found_treasure == treasure):
                    return False

            # Adding to found treasures
            found_treasures.append([treasure[0], treasure[1]])
            entity.fitness += 1

            # Calculating fitness of entity based on found treasures and steps
            if(COUNT_STEPS):
                entity.fitness += 0.01
                entity.fitness -= 0.0001 * len(entity.prints)
                # Round fitness to 4 decimal places
                entity.fitness = round(entity.fitness, 4)
            
            return True
    return False

def movePlayer(direction):
    global start_x, start_y

    # Moving player in given direction
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

    elif(direction == "L"):
        if(start_x == 0):
            return False
        else:
            start_x -= 1

    elif(direction == "P"):
        if(start_x == grid_x-1):
            return False
        else:
            start_x += 1
    else:
        print("Error")
    return True
    
def rateEntity(entity):
    global start_x, start_y, start_pos

    # Getting player moves 
    moves = entity.prints

    # Calculating fitness of entity based on found treasures and steps
    for move in moves:
        if(not movePlayer(move)):
            return False
        checkTreasure(entity)
    if(len(found_treasures) == len(treasures)):
        # This entity is the winner
        return True
    else:
        # This entity is not the winner
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

def pickElites(old_generation):

    # Sorting generation by fitness
    old_generation.sort(key=lambda x: x.fitness, reverse=True)

    # Selecting best entities
    elites = []
    for i in range(N_ELITES):
        # Reset prints and fitness
        old_generation[i].fitness = 0
        old_generation[i].prints = []
        elites.append(old_generation[i])

    return elites

def pickParents(old_generation):
    # Sorting generation by fitness
    old_generation.sort(key=lambda x: x.fitness, reverse=True)

    # Selecting best entities
    parents = []
    for i in range(N_PARENTS):
        parents.append(old_generation[i])

    return parents

def crossGeneration(old_generation):
    # Selecting parents
    parents = pickParents(old_generation)

    new_generation = []


    # Crossing parents
    for i in range(N_IN_GENERATION - N_ELITES - NEW_ENTITIES_COUNT):

        tournament_winners = []

        # Selecting random parents through tournament
        for i in range(2):

            # pick 4 random parents and put then into tournament
            tournament = []
            for j in range(4):
                tournament.append(parents[randint(0,N_PARENTS-1)])
            
            # Sorting tournament by fitness
            if(tournament[0].fitness > tournament[1].fitness):
                finalist1 = tournament[0]
            else:
                finalist1 = tournament[1]
            
            # Selecting best entity from tournament
            if(tournament[2].fitness > tournament[3].fitness):
                finalist2 = tournament[2]
            else:
                finalist2 = tournament[3]

            # Pick tournament winner
            if(finalist1.fitness > finalist2.fitness):
                tournament_winners.append(finalist1)
            else:
                tournament_winners.append(finalist2)
                
        # Crossing parents
        parent1 = tournament_winners[0]
        parent2 = tournament_winners[1]
        child = Entity()

        # Crossing genes
        for i in range(len(parent1.genome)):
            if(randint(0,1) == 1):
                child.genome.append(parent1.genome[i])
            else:
                child.genome.append(parent2.genome[i])

            # Mutate child gene with propability MUTATION_RATE in percent
            if(randint(0,100) < MUTATION_RATE):
                child.genome[i] = bin(randint(0,255))[2:].zfill(8)

        # Adding child to new generation
        new_generation.append(child)

    return new_generation

def spawn():

    new_entities = []

    # Creating new entities
    for i in range(NEW_ENTITIES_COUNT):
        new_entity = Entity()
        new_entity.fitness = 0
        new_entity.prints = []
        new_entity.genome = []
        for j in range(64):
            # Generating random gene from 0 to 255
            gene_int = randint(0,255)
            gene_bin = bin(gene_int)[2:].zfill(8)

            # Adding genome to entity
            new_entity.genome.append(gene_bin)
        new_entities.append(new_entity)
    return new_entities

# Declaring variables for statistics
gen_number = 0
curr_best_fitness = 0
new_gen_best_fitness = 0
best_entity = Entity()

all_time_stopped = 0

# start timer
start = time.time()

def newGeneration():
    global generation, gen_number, curr_best_fitness, new_gen_best_fitness, best_entity

    gen_number += 1

    # Creating new generation
    if(gen_number != 1):
        new_generation = pickElites(generation)
        new_children = (crossGeneration(generation))

        # Adding new children to new generation
        spawned_entities = spawn()
        generation = new_generation

        # Extending generation with new entities
        generation.extend(new_children)
        generation.extend(spawned_entities)
        #print("Počet jedincov v generácii: ",len(generation))

    # Creating new empty entity
    best_entity = Entity()
    best_entity.genome = []
    best_entity.fitness = 0
    best_entity.prints = []

    # Calculating best entity in generation
    for entity in generation:
        # Main cycle of virtual machine and rating
        VM(entity)
        rateEntity(entity)
        #print("Jedinec:",i,"Fitness:", entity.fitness)
        if(entity.fitness > best_entity.fitness):
            best_entity = entity
            if( math.floor(best_entity.fitness) == len(treasures)):
                # Winning entity found
                print(str(gen_number) + ". generácia")
                print("Best entity fitness:", best_entity.fitness)
                print("WINNER")
                print(best_entity.prints)
                return True

for i in range(MAX_GENERATIONS):
    if(i % 100 == 0):
        print(str(gen_number) + ". generácia")
    if(best_entity.fitness > curr_best_fitness):

        # Updating statistics
            curr_best_fitness = best_entity.fitness

            print(str(gen_number) + ". generácia")
            print("Best entity fitness:", best_entity.fitness)
            print("Best entity moves:",best_entity.prints)
            print("-------------------------------------")

            print("Prajete si vytvoriť ďalšiu generáciu? [A/n]")
            time_stop_start = time.time()
            answer = input()
            if(answer == "A" or answer == "a" or answer == ""):
                time_stop_end = time.time()
                time_stop = time_stop_end - time_stop_start
                all_time_stopped += time_stop
                newGeneration()

            else:
                time_stop_end = time.time()
                time_stop = time_stop_end - time_stop_start
                all_time_stopped += time_stop
                print("Ukončené používateľom")
                exit(0)
    else:
        if(newGeneration()):
            break

end_time = time.time()

#print time elapsed and round it to two decimal places
print("Prejdený čas:", round(end_time - start - all_time_stopped, 2), "sekúnd")
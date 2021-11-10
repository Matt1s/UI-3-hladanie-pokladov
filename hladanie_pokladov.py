from random import randint
import time

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
MAX_GENERATIONS = 15000

# Mutation rate in percent
MUTATION_RATE = 2

N_ELITES = 20
N_PARENTS = 60
NEW_ENTITIES_COUNT = 10

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

        if(i > MAX_INSTRUCTIONS):
            print("Too many instructions!")
            return
        #print("Jedinec:",index,"gén:",i,"inštrukcia",gene[0:2])

        instruction = entity.genome[i][:2]
        if(instruction == '00'):
            # Increment
            #print("INCREMENT")
            if(int(entity.genome[i]) == 255):
                entity.genome[i] = '00000000'
                print("Increment overflow!")
            else:
                entity.genome[i] = bin(int(entity.genome[i],2) + 1)[2:].zfill(8)
        if(instruction == '00'):
            # Decrement
            #print(entity.genome[i])
            #print("DECREMENT")
            if(bin(int(entity.genome[i],2)) == 0):
                entity.genome[i] = '11111111'
                print("Decrement overflow!")
            else:
                entity.genome[i] = bin(int(entity.genome[i],2) - 1)[2:].zfill(8)
            #print(improved_gene)
        if(instruction == '01'):
            #print("JUMP")
            # Jump on next gene
            #print(entity.genome[i])
            # Get last 6 characters from variable gene
            jump_gene = int(entity.genome[i][-6:])
            i = jump_gene
            #print(jump_gene)
            break
        if(instruction == '11'): # Instruction PRINT
            #print(i, entity.genome[i])
            #print("PRINT")
            direction = entity.genome[i][-2:]
            entity.addDirection(direction)
    #print(entity.prints)

        i+=1

found_treasures = []

def checkTreasure(entity):
    global treasures
    for treasure in treasures:
        if(start_x == treasure[0] and start_y == treasure[1]):
            for found_treasure in found_treasures:
                if(found_treasure == treasure):
                    return False
            #print("Treasure found!", treasure)
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
    #print(direction)
    #print(start_x,start_y)
    
def rateEntity(entity):
    global start_x, start_y, start_pos
    moves = entity.prints

    for move in moves:
        if(not movePlayer(move)):
            return False
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
    parents = pickParents(old_generation)

    new_generation = []

    for i in range(N_IN_GENERATION - N_ELITES - NEW_ENTITIES_COUNT):
        parent1 = parents[randint(0,N_PARENTS-1)]
        parent2 = parents[randint(0,N_PARENTS-1)]
        child = Entity()

        #print("PRINTS: ",child.prints)
        for i in range(len(parent1.genome)):
            if(randint(0,1) == 1):
                child.genome.append(parent1.genome[i])
            else:
                child.genome.append(parent2.genome[i])

            #mutate child gene with propability MUTATION_RATE in percent
            if(randint(0,100) < MUTATION_RATE):
                #print("Mutated!")
                child.genome[i] = bin(randint(0,255))[2:].zfill(8)

        #print("Crossing: ",parent1.fitness,"+",parent2.fitness)
        new_generation.append(child)

    return new_generation

def spawn():
    new_entities = []
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

    if(gen_number != 1):
        new_generation = pickElites(generation)
        new_children = (crossGeneration(generation))

        spawned_entities = spawn()
        generation = new_generation

        generation.extend(new_children)
        generation.extend(spawned_entities)
        #print("Počet jedincov v generácii: ",len(generation))


    best_entity = Entity()
    best_entity.genome = []
    best_entity.fitness = 0
    best_entity.prints = []

    for entity in generation:
        VM(entity)
        rateEntity(entity)
        #print("Jedinec:",i,"Fitness:", entity.fitness)
        if(entity.fitness > best_entity.fitness):
            best_entity = entity
            if(best_entity.fitness == len(treasures)):
                print(str(gen_number) + ". generácia")
                print("Best entity fitness:", best_entity.fitness)
                print("WINNER")
                print(best_entity.prints)
                return True

for i in range(MAX_GENERATIONS):
    if(i % 100 == 0):
        print(str(gen_number) + ". generácia")
    if(best_entity.fitness > curr_best_fitness):
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
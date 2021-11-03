from random import randint

# Declaring variables
grid_x = 0
grid_y = 0
start_x = 0
start_y = 0
treasures = []

# Number of entities in single generation
N_IN_GENERATION = 100

generation = []



# Function to read input from files
def read_file(route):
    global grid_x, grid_y, start_x, start_y, treasures
    # Read-only open
    f = open(route, "r")

    line_index = 0

    grid_size = ""
    start_pos = ""

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
    grid_x = grid_size[0]
    grid_y = grid_size[1]

    start_x = start_pos[0]
    start_y = start_pos[1]

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
    genome = []
    fitness = 0

# Generating initial population
for count in range(N_IN_GENERATION):
    # Generating entity
    entity = Entity()
    for i in range(64):

        # Generating random gene from 0 to 255
        gene_int = randint(0,255)
        gene_bin = bin(gene_int)[2:].zfill(8)
        print(gene_bin)

        # Adding genome to entity
        entity.genome.append(gene_bin)

    # Adding entity into generation
    generation.append(entity)

print("Počet generácií: ",len(generation))
for entity in generation:
    print("Dĺžka jedinca:", len(entity))


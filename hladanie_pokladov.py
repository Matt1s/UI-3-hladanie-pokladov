from random import randint

# Declaring variables
grid_x = 0
grid_y = 0
start_x = 0
start_y = 0
treasures = []

VM = []



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

for i in range(64):
    chromosome = ["0","0","0","0","0","0","0","0"]
    random_instruction = randint(0,3)
    if(random_instruction == 0):
        chromosome[0] = '0'
        chromosome[1] = '0'
    if(random_instruction == 1):
        chromosome[0] = '0'
        chromosome[1] = '1'
    if(random_instruction == 2):
        chromosome[0] = '1'
        chromosome[1] = '0'
    if(random_instruction == 3):
        chromosome[0] = '1'
        chromosome[1] = '1'
    VM.append(''.join(chromosome))
    print(VM[i])
print(len(VM))


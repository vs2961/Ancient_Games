import random

def create_ships(ships, shipPos, size):
    while True:
        coords = []

        # Choose random coordinates and orientation, restrict placement space
        isVert = random.choice([True, False])
        if isVert:
            x, y = random.randint(0, 9), random.randint(0, 10 - size)
        else:
            x, y = random.randint(0, 10 - size), random.randint(0, 9)
        br = False
        # Make sure there are no collisions
        for i in range(size):   
            if (isVert and ships[x][y + i] == 1) or (not isVert and ships[x + i][y] == 1):
                br = True
                break
        if br:
            continue

        # Place the ship in the board
        for i in range(size):
            if isVert:
                ships[x][y + i] = 1
                coords.append([x, y + i])
            else:
                ships[x + i][y] = 1
                coords.append([x + i, y])

        # Store the ship's location
        shipPos.append(coords)
        break

def randomize_ships():
    # Create a board for the player
    ships = [[0 for i in range(10)] for i in range(10)]
    shipPos = []

    # Place ships of varying lengths (2, 3, 3, 4, 5)
    for i in range(2, 6):
        create_ships(ships, shipPos, i)
    create_ships(ships, shipPos, 3)
    return ships, shipPos

def print_board(ships, hidden):
    # Prints a readable board for the user
    print("   A  B  C  D  E  F  G  H  I  J")
    for i in range(len(ships)):
        output = f"{i}  "
        for j in range(len(ships)):
            if hidden and ships[i][j] == 1:
                output += "0  "
            else:
                output += str(ships[i][j]) + "  "
        print(output)

def ask_coords():
    nums = "0123456789"
    alpha = "abcdefghij"
    while True:
        a = input("Input coordinates: ")

        # Parse user input for information
        if len(a) == 2:
            a = sorted(list(a))
            a[1] = a[1].lower()
            if a[0] in nums and a[1] in alpha:
                return int(a[0]), alpha.index(a[1])

def get_valid_coords(ships, x, y, signX, signY):

    # Look in cardinal directions for possible hits
    for i in range(1, 9):
        if (signX < 0 and i > x) or (signY < 0 and i > y) or (signX > 0 and x + i >= 10) or (signY > 0 and y + i >= 10):
            return None, None
        if ships[x + i * signX][y + i * signY] == "*":
            continue
        elif ships[x + (i * signX)][y + (i * signY)] in [0, 1]:
            return x + i * signX, y + i * signY
        else:
            # Return None if there is no possible location for the specific direction
            return None, None

def opponent_turn(ships, brain):
    # Check if a hit was detected last turn
    if brain["seen"]:
        if brain["vert"]:
            # Get coordinates for vertically up and down 
            x, y = get_valid_coords(ships, brain["x"], brain["y"], 1, 0)
            if x == None:
                x, y = get_valid_coords(ships, brain["x"], brain["y"], -1, 0)
            else:
                return x, y
            if x == None:
                brain["vert"] = False
            else:
                return x, y

        # Get coordinates for horizontally left and right
        x, y = get_valid_coords(ships, brain["x"], brain["y"], 0, 1)
        if x == None:
            x, y = get_valid_coords(ships, brain["x"], brain["y"], 0, -1)
        return x, y
    
    # If there was no hit, choose a random square
    while True:
        x, y = random.randint(0, 9), random.randint(0, 9)
        if ships[x][y] == "*" or ships[x][y] == "s":
            continue
        return x, y

def update_board(ships, shipPos, x, y, player, brain = None):
    alpha = "abcdefghij"
    # If the guess is a hit
    if ships[x][y] == 1:
        ships[x][y] = "*"
        for i in range(len(shipPos)):
            coords = [x, y]
            # Check if a ship was destroyed
            if coords in shipPos[i]:
                # If this is the opponent's guess, update the brain
                if player == "Opponent" and not brain["seen"]:
                    brain["x"], brain["y"] = x, y
                    brain["seen"] = True 
                for j in shipPos[i]:
                    if j == coords and len(shipPos[i]) == 1:
                        # Update brain if ship was destroyed
                        if player == "Opponent":
                            brain["seen"] = False
                            brain["vert"] = True
                        # Remove ship
                        shipPos.pop(i)
                        return f"{player}: Ship Sunk on {alpha[y]}{x}!"
                    elif j == coords:
                        # Remove target when hit
                        shipPos[i].remove(j)
                        return f"{player}: Hit Ship on {alpha[y]}{x}!"
    # Tell if ship was already hit
    elif ships[x][y] == "*":
        return f"{player}: Already hit ship on {alpha[y]}{x}"
    # Tell if the person missed
    else:
        ships[x][y] = "s"
        return f"{player}: Missed on {alpha[y]}{x}."

def game():
    # Initialize opponent's brain, ships, and ship positions
    opBrain = {"seen": False, "x":0, "y":0, "vert":True} 
    opponent, opShipPos = randomize_ships()
    you, myShipPos = randomize_ships()
    turn = 1

    while True:
        # Display boards
        print("Opponent's Board:")
        print_board(opponent, True)
        print("Your Board:")
        print_board(you, False)

        # Ask the user for input
        x, y = ask_coords()

        print(f"\nTurn {turn}: ")
        # Update the board with your inputs and the opponent's inputs
        print(update_board(opponent, opShipPos, x, y, "You"))
        x, y = opponent_turn(you, opBrain)
        print(update_board(you, myShipPos, x, y, "Opponent", opBrain))
        
        # Separate different turns
        turn += 1
        print("_" * 50)

        # Check for win/loss conditions
        if len(myShipPos) == 0:
            print("You lose.")
            break
        elif len(opShipPos) == 0:
            print("You win!")
            break

if __name__ == "__main__":
    game()

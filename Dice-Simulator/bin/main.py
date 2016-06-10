from bin.Dice import Dice

def get_num_of_sides():
    num_of_sides = input("How many sides does your dice have?\n")
    if num_of_sides < 1:
        print "Cannot have less than 1 side, please try again"
        return get_num_of_sides()
    return num_of_sides


num_of_sides = get_num_of_sides()

dice = Dice(num_of_sides + 1)

selection = 0

while selection != 3:
    selection = input("What do you want to do?"
                      "\n1. Change number of sides."
                      "\n2. Roll dice"
                      "\n3. Quit\n")

    if selection == 1:
        num_of_sides = get_num_of_sides()
        dice.change_sides(num_of_sides + 1)
    elif selection == 2:
        print "You have rolled a %d.\n" % dice.roll()

print "Goodbye."
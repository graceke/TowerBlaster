import random

turn_count = 0


def setup_bricks():
    '''sets up the game main pile with 1-60 in a list and discareded empty then return them as a tuple'''
    main_bricks = list(range(1, 61))
    discarded_bricks = []

    return main_bricks, discarded_bricks


def shuffle_bricks(bricks):
    '''shuffles bricks with random...'''
    random.shuffle(bricks)


def check_bricks(main_pile, discard):
    '''checks if main pile (list) is empty. If it is shuffles discard and copies it over and clears discard. Then adds the top brick to discard'''
    if len(main_pile) == 0:
        random.shuffle(discard)
        main_pile = discard.copy()
        discard.clear()
        first_brick = get_top_brick(main_pile)
        add_brick_to_discard(first_brick, discard)


def check_tower_blaster(tower):
    '''check if player/computer tower is sorted'''
    for num in range(1, 9):
        if tower[num] < tower[num + 1]:
            continue
        else:
            return True
    return False


def get_top_brick(brick_pile):
    '''returns top brick of either pile'''
    return brick_pile.pop(0)


def deal_initial_bricks(main_pile):
    '''appends bricks to each players tower from the main pile then returns both towers as a tuple'''
    computer_tower = []
    human_tower = []
    for n in range(10):
        computer_tower.append(get_top_brick(main_pile))
        human_tower.append(get_top_brick(main_pile))
    human_tower.reverse()
    computer_tower.reverse()
    return computer_tower, human_tower


def add_brick_to_discard(brick, discard):
    '''inserts discarded brick to discard pile'''
    discard.insert(0, brick)


def find_and_replace(new_brick, brick_to_be_replaced, tower, discard):
    '''finds the brick player wants to replace if it is in the tower then replace it with the brick player wants. After adds brick to be replaced to discard'''
    if brick_to_be_replaced in tower:
        i = tower.index(brick_to_be_replaced)
        tower[i] = new_brick
        add_brick_to_discard(brick_to_be_replaced, discard)
        return True
    else:
        return False


def computer_play(tower, main_pile, discard):  # my function will check if the main_pile
    '''basically my computer for the first 30 turns checks if a number is greater then a determined number by me. 
    It then iterates through the positions backwards for 5-9 and determines if that number is larger then the number in those given positions'''
    ### Summary of my strategy. Read below comments for break down of each if/elif statement. Basically this will look 
    ###if a number is greater then the value in positions 9-5. Because if it is greater then the block at that location
    ### then its a more stable piece. through this it will set a strong base and replace smaller number blockes one at a time 
    ###iterating through the positions. Making sure the block above it will not be greater then the block below
    ### For the 1-4 positions we do the opposite. If a block is smaller then the first position we replace it. 
    ###If it is not we go to the next block to see if it is smaller. This will ensure a ascending tower(towards the base)    
    ### We want to do that for the first 30 turns(15 per player) because this will set a good general tower. See the else statement for next part of stratergy.
    global turn_count
    print(' It is the computer turn! ', tower)
    if turn_count < 30:  # my computer play if it is under turn 30 it will follow the below formula
        if discard[
            0] > 45:  # if the top discarded brick is greater then 45 it will iterate backwards form 9 to 7. If the brick is greater then them it will replace the first one it is greater then
            for n in range(9, 6, -1):
                if discard[0] > tower[n]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n], tower, discard)
                    turn_count += 1
                    break

        elif discard[
            0] > 30:  # if the top discarded brick is greater then 30 it will iterate from 6 and 5 as index for the tower. Same as above if it is greater it will replace the given brick.
            for n in range(6, 4, -1):
                if discard[0] > tower[n]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n], tower, discard)
                    turn_count += 1
                    break

        elif discard[
            0] > 15:  # if the brick is greather then 15 it will iterate through 3 and 4 as index for tower and if it is less then the brick at that location it will repalce
            for n in range(3, 5):
                if discard[0] < tower[n]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n], tower, discard)
                    turn_count += 1
                    break

        elif discard[0] > 0 and discard[
            0] < 16:  # Same as above. For the given range iterate through 0,1,2 if it is less it will replace. 
            for n in range(0, 3):
                if discard[0] < tower[n]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n], tower, discard)
                    turn_count += 1
                    break

        else:  # if the brick did not meet any of the conditions above we will come to this statement. Here we will iterate through 1-9 to see where does the tower hit a snag.
            for n in range(9):  # When the brick is bigger then the brick following it we go to the elif statement. 
                if tower[n] < tower[n + 1]:
                    continue
                elif main_pile[0] < tower[
                    n]:  # If the main pile brick is less then the out of position brick. we simply replace that with the smaller one.
                    mainBrick = get_top_brick(main_pile)
                    find_and_replace(mainBrick, tower[n], tower, discard)

                else:
                    add_brick_to_discard(main_pile.pop(0), discard)
    else:
        ###The second part of the stratergy is that after 30 turns we will look to better optimize the individual blocks of the tower
        ###So we check if the tower is ascending in block numbers through a for loop. When we hit a snag where the pervious block is greater then the next blocks
        ###we willl test to see if the discard block is less then the tower location and if it is also greater then the previous position
        ###if those conditions arn't met we see if the discard is bigger then the current posotion(n). If it is we check to see if it is less then the next next position(n+2) 
        ###if it is we will put that block in. This catches the case where a small number is caught in between 2 correct blocks.
        ###Stratergy basically stays the same for main_pile
        for n in range(9):
            if tower[n] < tower[n + 1]:
                continue
            else:
                if discard[0] < tower[n] and discard[0] > tower[n - 1]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n], tower, discard)
                    break
                elif discard[0] > tower[n] and discard[0] > tower[n + 1] and discard[0] < tower[n + 2]:
                    discardBrick = get_top_brick(discard)
                    find_and_replace(discardBrick, tower[n + 1], tower, discard)
                    break
                elif main_pile[0] < tower[n] or main_pile[0] > tower[n] and main_pile[0] < tower[n + 2]:
                    mainBrick = get_top_brick(main_pile)
                    find_and_replace(mainBrick, tower[n], tower, discard)
                    break


def user_play(tower, main_pile, discard):
    '''used in combination with ask_yes_or_no to prompt user input if they want to use discard brick. If so ask which brick they want to replace with. 
    Does the same for main pile brick. Then uses find and replace function to replace that block'''
    print('top discarded brick:', discard[0])
    print('your current tower:', tower)
    global turn_count
    if ask_yes_or_no('do you want to use the top discard block?(Y/N)'):  # asks if they want to use top discarded brick
        discardBrick = get_top_brick(discard)  # gets top brick sets it to a temp variable
        brickNum = brick_number()  # asks what brick number they want to change
        valid = False  # temp variable
        while valid == False:  # while it is false we try to find and replace the input. If it works we return True for valid and breaks the loop.
            valid = find_and_replace(discardBrick, brickNum, tower, discard)
            if valid == False:
                print('Please Enter a Valid Brick')
                brickNum = brick_number()
        turn_count += 1
    else:
        print('top main pile brick:', main_pile[0])
        if ask_yes_or_no('do you want to use the top main brick?(Y/N)'):
            mainBrick = get_top_brick(main_pile)
            brickNum = brick_number()
            valid = False
            while valid == False:
                valid = find_and_replace(mainBrick, brickNum, tower, discard)
                if valid == False:
                    ('Please Enter a Valid Brick')
                    brickNum = brick_number()
            turn_count += 1
            print('you replaced', brickNum)
        else:
            mainBrick = get_top_brick(main_pile)
            add_brick_to_discard(mainBrick, discard)
            print('you have ended your turn')
            turn_count += 1


def brick_number():
    '''prompts user for brick number they want to replace with either discarded or main pile brick. Checks if its between 1 and 60. Also catches errors if they input a not int type'''
    while True:
        num = input('What number do you want to replace?')

        try:  # while loop to see if the input is integers
            if 1 <= int(num) < 61:
                return int(num)
                break
            else:
                print('please enter a valid response')
        except:
            print('please enter a valid response')


def ask_yes_or_no(prompt):
    '''While loop asking for player input. If player inputs a string starting with y it returns True. If player inputs
    a string starting with n it returns False. Else we print a message'''
    while True:
        a = input(prompt).lower()  # asks for user input and puts it into lower case

        try:  # while loop to see if the first letter starts with y or n. In order to return True or False
            if a[0] == 'y':
                return True
                break
            elif a[0] == 'n':
                return False
            else:
                print('please enter a valid response')
        except:
            print('please enter a valid response')


def main():
    playing = True
    brick_pile = setup_bricks()
    main_bricks = brick_pile[0]
    discarded_bricks = brick_pile[1]
    shuffle_bricks(main_bricks)
    towers = deal_initial_bricks(main_bricks)
    computer_tower = towers[0]
    human_tower = towers[1]
    first_brick = get_top_brick(main_bricks)
    add_brick_to_discard(first_brick, discarded_bricks)

    while playing == True:
        print(discarded_bricks)
        computer_play(computer_tower, main_bricks, discarded_bricks)
        print('This is computer tower now', computer_tower)
        playing = check_tower_blaster(computer_tower)
        if playing == False:
            print('COMPUTER WINS!!!!')
            continue
        check_bricks(main_bricks, discarded_bricks)
        print(discarded_bricks)

        user_play(human_tower, main_bricks, discarded_bricks)
        playing = check_tower_blaster(human_tower)
        if playing == False:
            print('HUMAN WINS!!!!')
            continue

        check_bricks(main_bricks, discarded_bricks)
        print(discarded_bricks)


if __name__ == "__main__":
    main()

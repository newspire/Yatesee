# Yet Another simple rules based Yatesee player
# The rules mirror my own general play patterns
# This version optionally prints and provides a function so that the automated play can be put in a loop
from yatesee import Yatesee

small_straights = [
		[1,2,3,4],
		[2,3,4,5],
		[3,4,5,6]
	]

large_straights = [
		[1,2,3,4,5],
		[2,3,4,5,6]
	]

my_print_flag = False

def is_yatesee(game) :
    if game.score.yatesee == 0 :    # Yatesee already scored with 0. What a shame.
        return False

    for x in range(1,7) :
        if game.dice.count(x) == 5 :
            return True

    return False

def get_possible_straight(dice) :
    """Returns a list of indexes of the best possible straight"""
    results = []
    for s in small_straights :
        results.append( list(set(s) & set(dice)) )
    for s in large_straights :
        results.append( list(set(s) & set(dice)) )

    best_match = []
    max = 0
    for x in range(len(results)) :
        if len(results[x]) > max :
            best_match = results[x]
            max = len(results[x])

    return [dice.index(x) for x in best_match]

def get_possible_full_house(dice) :

    pfh = []
    for k in range(1,7) :
        d = get_kind(dice, k)
        if len(d) >= 2  :
            pfh += d[0:3]

    return pfh


def get_kind(dice, kind) :
    """Returns a list of indexes of a kind"""
    indexes = []
    for i in range(len(dice)) :
        if kind == dice[i] :
            indexes.append(i)

    return indexes


def is_straight(dice, straights) :
    for s in straights :
        if len(set(s) & set(dice)) == len(s) :
            return True

    return False

def is_full_house(dice) :
    for tre in range(1,7) :
        if dice.count(tre) == 3 :
            for duce in range(1, 7) :
                if duce == tre :
                    continue
                if dice.count(duce) == 2 :
                    return True

    return False

def get_indexes(dice, value) :
    """Get index of dice with value"""

    indexes = []
    for i in range(len(dice)) :
        if value == dice[i] :
            indexes.append(i)

    return indexes


def print_score(score) :
    my_print(str(score.category))
    my_print('Bonus:          %s' % score.category_bonus)
    my_print('Three of a kind:%s' % score.three_of_a_kind)
    my_print('Four of a kind: %s' % score.four_of_a_kind)
    my_print('Full House:     %s' % score.full_house)
    my_print('Small Straight: %s' % score.small_straight)
    my_print('Large Straight: %s' % score.large_straight)
    my_print('Chance:         %s' % score.chance)
    my_print('Yatesee:        %s' % score.yatesee)
    my_print('Total:          %s' % score.total)



####################################################################
#from yatesee import Die

#dice = [Die(3), Die(2), Die(3), Die(3), Die(1)]
#print 'Possible Straight:', getPossibleStraight(dice)
#dice = [Die(3), Die(2), Die(3), Die(2), Die(1)]
#print 'Possible Full House:', getPossibleFullHouse(dice)
#quit()

def my_print(s='') :
    if my_print_flag :
        print(s)

def play_yatesee() :
    game = Yatesee()

    hold_indexes = []
    while not game.is_game_over() :
        #raw_input()
        #print
        if game.roll == 0 :
            print_score(game.score)
            my_print()

        game.roll_dice(hold_indexes)
        hold_indexes.sort()
        my_print('Roll: {} Hold: {:12} Dice: {}'.format( game.roll, str([i+1 for i in hold_indexes]), game.dice))
        hold_indexes = []

        if is_yatesee(game) :
            my_print( '***Score Yatesee')
            game.score_yatesee()
            continue

        if game.score.large_straight == None :
            if is_straight(game.dice, large_straights) :
                my_print('***Score large straight')
                game.score_large_straight()
                continue

        if game.score.small_straight == None and game.roll == 3:
            if is_straight(game.dice, small_straights) :
                my_print('***Score small straight')
                game.score_small_straight()
                continue

        if game.score.full_house == None :
            if is_full_house(game.dice) :
                my_print('***Score full house')
                game.score_full_house()
                continue

        for cat in range(1, 7) :
            if game.score.category[cat] == None and game.roll == 3 :
                if game.dice.count(cat) >= 3:
                    my_print('***Score Category %d' % cat)
                    game.score_category(cat)
                    break

        if game.roll == 0 :     #We must have scored a category
            continue

        if game.score.four_of_a_kind == None and game.roll == 3 :
            for cat in range(1, 7) :
                if game.dice.count(cat) >= 4 :
                    my_print('***Score 4 of a kind')
                    game.score_four_of_a_kind()
                    break

        if game.roll == 0 :
            continue

        if game.score.three_of_a_kind == None and game.roll == 3 :
            for cat in range(1, 7) :
                if game.dice.count(cat) >= 3 :
                    my_print('***Score 3 of a kind')
                    game.score_three_of_a_kind()
                    break

        if game.roll == 0 :
            continue



        if game.roll < 3 and game.score.full_house == None :
            pfh = get_possible_full_house(game.dice)
            if len(pfh) > 2 :
                hold_indexes = pfh
                continue

        if game.roll < 3 and ( (game.score.small_straight == None) or (game.score.large_straight == None) ) :
            ps = get_possible_straight(game.dice)
            if len(ps) >= 3 :
                hold_indexes = ps
                continue

        if game.roll < 3 :
            for k in range(1, 7) :
                if (game.score.three_of_a_kind == None) or (game.score.four_of_a_kind == None) or (game.score.category[k] == None) :
                    i = get_kind(game.dice, k)
                    if len(i) >= 2  and len(i) > len(hold_indexes) :
                        hold_indexes = i
                        continue

        #No good options left so we must score something
        if game.roll == 3 :

            if game.score.chance == None :
                my_print('***Score give up chance')
                game.score_chance()
                continue

            for cnt in range(2, -1, -1) :
                if game.roll == 0 :
                    break
                for cat in range(1, 7) :
                    if game.score.category[cat] == None :
                        if game.dice.count(cat) >= cnt:
                            my_print('***Score give up category %d' % cat)
                            game.score_category(cat)
                            break

            if game.roll == 0 :
                continue


            if game.score.three_of_a_kind == None :
                my_print('***Score give up 3 of a kind')
                game.score_three_of_a_kind()
                continue

            if game.score.four_of_a_kind == None :
                my_print('***Score give up 4 of a kind')
                game.score_four_of_a_kind()
                continue

            if game.score.full_house == None :
                my_print('***Score give up full house')
                game.score_full_house()
                continue

            if game.score.small_straight == None :
                my_print('***Score give up small straight')
                game.score_small_straight()
                continue

            if game.score.large_straight == None :
                my_print('***Score give up large straight')
                game.score_large_straight()
                continue

            if game.score.yatesee == None :
                my_print('***Score give up Yatesee')
                game.score_yatesee()
                continue

    my_print()
    my_print('***Game Over Dude***')
    print_score(game.score)

    return game.score

if __name__ == "__main__" :
    my_print_flag = True
    play_yatesee()
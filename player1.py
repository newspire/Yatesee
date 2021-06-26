#A simple rules based Yatesee player
#An example of how to use the Yatesee module
#The rules mirror my own general play patterns
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



def is_yatesee(dice) :
    for x in range(1,7) :
        if dice.count(x) == 5 :
            return True

    return False

def is_possible_straight(dice) :
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

    return best_match

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

game = Yatesee()

while not game.is_game_over() :
    print(game.score.__dict__)
    game.roll_dice()
    print(game.roll, game.dice)

    if is_yatesee(game.dice) :
        game.score_yatesee()
        continue

    if game.score.large_straight == None :
        if is_straight(game.dice, large_straights) :
            game.score_large_straight()
            continue

    if game.score.small_straight == None :
        if is_straight(game.dice, small_straights) :
            game.score_small_straight()
            continue

    if game.score.full_house == None :
        if is_full_house(game.dice) :
            game.score_full_house()
            continue

    if game.score.four_of_a_kind == None :
        for cat in range(1, 7) :
            if game.dice.count(cat) >= 4 :
                game.score_four_of_a_kind()
                break

    if game.roll == 0 :
        continue

    if game.score.three_of_a_kind == None :
        for cat in range(1, 7) :
            if game.dice.count(cat) >= 3 :
                game.score_three_of_a_kind()
                break

    if game.roll == 0 :
        continue

    for cat in range(1, 7) :
        if game.score.category[cat] == None :
            if game.dice.count(cat) >= 3:
                game.score_category(cat)
                break

    if game.roll == 0 :     #We must have scored a category
        continue

    #No good options left so we must score something
    if game.roll == 3 :
        for cnt in range(2, -1, -1) :
            if game.roll == 0 :
                break
            for cat in range(1, 7) :
                if game.score.category[cat] == None :
                    if game.dice.count(cat) >= cnt:
                        game.score_category(cat)
                        break

        if game.roll == 0 :
            continue

        if game.score.chance == None :
            game.score_chance()
            continue

        if game.score.three_of_a_kind == None :
            game.score_three_of_a_kind()
            continue

        if game.score.four_of_a_kind == None :
            game.score_four_of_a_kind()
            continue

        if game.score.full_house == None :
            game.score_full_house()
            continue

        if game.score.small_straight == None :
            game.score_small_straight()
            continue

        if game.score.large_straight == None :
            game.score_large_straight()
            continue

        if game.score.yatesee == None :
            game.score_yatesee()
            continue

print()
print('***Game Over Dude***')
print(game.score.__dict__)
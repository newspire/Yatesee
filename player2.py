#Yet Another simple rules based Yatesee player
#The rules mirror my own general play patterns
#This version optionally prints and provides a function so that the automated play can be put in a loop
from yatesee import Yatesee

smallStraights = [
		[1,2,3,4],
		[2,3,4,5],
		[3,4,5,6]
	]

largeStraights = [
		[1,2,3,4,5],
		[2,3,4,5,6]
	]

myPrintFlag = False

def isYatesee(game) :
    if game.score.yatesee == 0 :    #Yatesee already scored with 0. What a shame.
        return False

    for x in range(1,7) :
        if game.dice.count(x) == 5 :
            return True

    return False

def getPossibleStraight(dice) :
    """Returns a list of indexes of the best possible straight"""
    results = []
    for s in smallStraights :
        results.append( list(set(s) & set(dice)) )
    for s in largeStraights :
        results.append( list(set(s) & set(dice)) )

    bestMatch = []
    max = 0
    for x in range(len(results)) :
        if len(results[x]) > max :
            bestMatch = results[x]
            max = len(results[x])

    return [dice.index(x) for x in bestMatch]

def getPossibleFullHouse(dice) :

    pfh = []
    for k in range(1,7) :
        d = getKind(dice, k)
        if len(d) >= 2  :
            pfh += d[0:3]

    return pfh


def getKind(dice, kind) :
    """Returns a list of indexes of a kind"""
    indexes = []
    for i in range(len(dice)) :
        if kind == dice[i] :
            indexes.append(i)

    return indexes


def isStraight(dice, straights) :
    for s in straights :
        if len(set(s) & set(dice)) == len(s) :
            return True

    return False

def isFullHouse(dice) :
    for tre in range(1,7) :
        if dice.count(tre) == 3 :
            for duce in range(1, 7) :
                if duce == tre :
                    continue
                if dice.count(duce) == 2 :
                    return True

    return False

def getIndexes(dice, value) :
    """Get index of dice with value"""

    indexes = []
    for i in range(len(dice)) :
        if value == dice[i] :
            indexes.append(i)

    return indexes


def printScore(score) :
    myPrint(str(score.category))
    myPrint('Bonus:          %s' % score.categoryBonus)
    myPrint('Three of a kind:%s' % score.threeOfAKind)
    myPrint('Four of a kind: %s' % score.fourOfAKind)
    myPrint('Full House:     %s' % score.fullHouse)
    myPrint('Small Straight: %s' % score.smallStraight)
    myPrint('Large Straight: %s' % score.largeStraight)
    myPrint('Chance:         %s' % score.chance)
    myPrint('Yatesee:        %s' % score.yatesee)
    myPrint('Total:          %s' % score.total)



####################################################################
#from yatesee import Die

#dice = [Die(3), Die(2), Die(3), Die(3), Die(1)]
#print 'Possible Straight:', getPossibleStraight(dice)
#dice = [Die(3), Die(2), Die(3), Die(2), Die(1)]
#print 'Possible Full House:', getPossibleFullHouse(dice)
#quit()

def myPrint(s='') :
    if myPrintFlag :
        print(s)

def playYatesee() :
    game = Yatesee()

    holdIndexes = []
    while not game.isGameOver() :
        #raw_input()
        #print
        if game.roll == 0 :
            printScore(game.score)
            myPrint()

        game.rollDice(holdIndexes)
        holdIndexes.sort()
        myPrint('Roll: {} Hold: {:12} Dice: {}'.format( game.roll, str([i+1 for i in holdIndexes]), game.dice))
        holdIndexes = []

        if isYatesee(game) :
            myPrint( '***Score Yatesee')
            game.scoreYatesee()
            continue

        if game.score.largeStraight == None :
            if isStraight(game.dice, largeStraights) :
                myPrint('***Score large straight')
                game.scoreLargeStraight()
                continue

        if game.score.smallStraight == None and game.roll == 3:
            if isStraight(game.dice, smallStraights) :
                myPrint('***Score small straight')
                game.scoreSmallStraight()
                continue

        if game.score.fullHouse == None :
            if isFullHouse(game.dice) :
                myPrint('***Score full house')
                game.scoreFullHouse()
                continue

        for cat in range(1, 7) :
            if game.score.category[cat] == None and game.roll == 3 :
                if game.dice.count(cat) >= 3:
                    myPrint('***Score Category %d' % cat)
                    game.scoreCategory(cat)
                    break

        if game.roll == 0 :     #We must have scored a category
            continue

        if game.score.fourOfAKind == None and game.roll == 3 :
            for cat in range(1, 7) :
                if game.dice.count(cat) >= 4 :
                    myPrint('***Score 4 of a kind')
                    game.scoreFourOfAKind()
                    break

        if game.roll == 0 :
            continue

        if game.score.threeOfAKind == None and game.roll == 3 :
            for cat in range(1, 7) :
                if game.dice.count(cat) >= 3 :
                    myPrint('***Score 3 of a kind')
                    game.scoreThreeOfAKind()
                    break

        if game.roll == 0 :
            continue



        if game.roll < 3 and game.score.fullHouse == None :
            pfh = getPossibleFullHouse(game.dice)
            if len(pfh) > 2 :
                holdIndexes = pfh
                continue

        if game.roll < 3 and ( (game.score.smallStraight == None) or (game.score.largeStraight == None) ) :
            ps = getPossibleStraight(game.dice)
            if len(ps) >= 3 :
                holdIndexes = ps
                continue

        if game.roll < 3 :
            for k in range(1, 7) :
                if (game.score.threeOfAKind == None) or (game.score.fourOfAKind == None) or (game.score.category[k] == None) :
                    i = getKind(game.dice, k)
                    if len(i) >= 2  and len(i) > len(holdIndexes) :
                        holdIndexes = i
                        continue

        #No good options left so we must score something
        if game.roll == 3 :

            if game.score.chance == None :
                myPrint('***Score give up chance')
                game.scoreChance()
                continue

            for cnt in range(2, -1, -1) :
                if game.roll == 0 :
                    break
                for cat in range(1, 7) :
                    if game.score.category[cat] == None :
                        if game.dice.count(cat) >= cnt:
                            myPrint('***Score give up category %d' % cat)
                            game.scoreCategory(cat)
                            break

            if game.roll == 0 :
                continue


            if game.score.threeOfAKind == None :
                myPrint('***Score give up 3 of a kind')
                game.scoreThreeOfAKind()
                continue

            if game.score.fourOfAKind == None :
                myPrint('***Score give up 4 of a kind')
                game.scoreFourOfAKind()
                continue

            if game.score.fullHouse == None :
                myPrint('***Score give up full house')
                game.scoreFullHouse()
                continue

            if game.score.smallStraight == None :
                myPrint('***Score give up small straight')
                game.scoreSmallStraight()
                continue

            if game.score.largeStraight == None :
                myPrint('***Score give up large straight')
                game.scoreLargeStraight()
                continue

            if game.score.yatesee == None :
                myPrint('***Score give up Yatesee')
                game.scoreYatesee()
                continue

    myPrint()
    myPrint('***Game Over Dude***')
    printScore(game.score)

    return game.score

if __name__ == "__main__" :
    myPrintFlag = True
    playYatesee()
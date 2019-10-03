#A simple rules based Yatesee player
#An example of how to use the Yatesee module
#The rules mirror my own general play patterns
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



def isYatesee(dice) :
    for x in range(1,7) :
        if dice.count(x) == 5 :
            return True
         
    return False

def isPossibleStraight(dice) :
    results = []
    for s in smallStraights :
        results.append( list(set(s) & set(dice)) )
    for s in largeStraights :
        results.append( list(set(s) & set(dice)) )
    
    best_match = []
    max = 0
    for x in range(len(results)) :
        if len(results[x]) > max :
            best_match = results[x]
            max = len(results[x])
        
    return best_match    

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
        
game = Yatesee()    
    
while not game.isGameOver() :
    print(game.score.__dict__)
    game.rollDice()
    print(game.roll, game.dice)
    
    if isYatesee(game.dice) :
        game.scoreYatesee()
        continue
    
    if game.score.largeStraight == None :
        if isStraight(game.dice, largeStraights) :
            game.scoreLargeStraight()
            continue
            
    if game.score.smallStraight == None :
        if isStraight(game.dice, smallStraights) :
            game.scoreSmallStraight()
            continue        
            
    if game.score.fullHouse == None :
        if isFullHouse(game.dice) :
            game.scoreFullHouse()
            continue
            
    if game.score.fourOfAKind == None :  
        for cat in range(1, 7) :
            if game.dice.count(cat) >= 4 :
                game.scoreFourOfAKind()
                break
                
    if game.roll == 0 : 
        continue
        
    if game.score.threeOfAKind == None :  
        for cat in range(1, 7) :
            if game.dice.count(cat) >= 3 :
                game.scoreThreeOfAKind()
                break
    
    if game.roll == 0 : 
        continue
        
    for cat in range(1, 7) :        
        if game.score.category[cat] == None :
            if game.dice.count(cat) >= 3:
                game.scoreCategory(cat)
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
                        game.scoreCategory(cat)
                        break

        if game.roll == 0 :
            continue
            
        if game.score.chance == None :
            game.scoreChance()
            continue
            
        if game.score.threeOfAKind == None :
            game.scoreThreeOfAKind()
            continue
        
        if game.score.fourOfAKind == None :
            game.scoreFourOfAKind()
            continue
            
        if game.score.fullHouse == None :
            game.scoreFullHouse()
            continue
            
        if game.score.smallStraight == None :
            game.scoreSmallStraight()
            continue
            
        if game.score.largeStraight == None :
            game.scoreLargeStraight()
            continue
            
        if game.score.yatesee == None :
            game.scoreYatesee()
            continue
        
print()
print('***Game Over Dude***')
print(game.score.__dict__)
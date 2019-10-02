from random import randint

    
class YateseeError(Exception) :
    def __init__(self) :
        self.msg = "Yatesee Error"
    
    
class YateseeGameOver(YateseeError) :
    def __init__(self) :
        self.msg = "Game Over!"
    
class YateseeRollError(YateseeError) :
    def __init__(self, roll, msg) :
        self.roll = roll
        self.msg = msg

class YateseeScoreError(YateseeError) :
    def __init__(self, msg) :        
        self.msg = msg
    
class Die(object) :
    def __init__(self, val=1, sides=6) :
        self.val = val
        self.sides = sides        
        
    def roll(self) :
        self.val = randint(1,self.sides)
        return self.val
        
    def currentValue(self) :
        return self.val
    
    def __hash__(self) :
        #print '__hash__', self.val
        return hash(self.val)
    
    def __eq__(self, other):
        #print '__eq__', self.val, other
        if isinstance(other, Die) :
            return self.val == other.val
        return self.val == other
            
    def __lt__(self, other):
        #print '__lt__', self.val, other
        if isinstance(other, Die) :
            return self.val < other.val
        return self.val < other

    def __le__(self, other):
        #print '__le__', self.val, other
        if isinstance(other, Die) :
            return self.val <= other.val
        return self.val <= other

    def __ne__(self, other):
        #print '__ne__', self.val, other
        if isinstance(other, Die) :
            return self.val != other.val
        return self.val != other

    def __gt__(self, other):
        #print '__gt__', self.val, other
        if isinstance(other, Die) :
            return self.val > other.val
        return self.val > other

    def __ge__(self, other):
        #print '__ge__', self.val, other
        if isinstance(other, Die) :
            return self.val >= other.val
        return self.val >= other

    def __and__(self, other):
        #print '__and__', self.val, other
        if isinstance(other, Die) :
            return self.val == other.val
        return self.val & other
        
    def __rand__(self, other):
        #print '__rand__', self.val, other
        if isinstance(other, Die) :
            return self.val & other.val
        return self.val & other    
    
    def __str__(self) :
        return str(self.val)
        
    def __repr__(self) :
        return str(self.val)    
        
    def __add__(self, other) :
        if isinstance(other, Die) :
            return self.val + other.val
        return other + self.val
    
    def __radd__(self, other) :
        if isinstance(other, Die) :
            return self.val + other.val
        return other + self.val

        
        
class YateseeScore(object) :
    def __init__(self) :
        self.category = { 1:None,2:None,3:None,4:None,5:None,6:None}
        self.categoryBonus = 0
        self.threeOfAKind = None
        self.fourOfAKind = None
        self.fullHouse = None
        self.smallStraight = None
        self.largeStraight = None
        self.chance = None        
        self.yatesee = None
        self.yateseeCount = 0
        self.total = 0
        
        
    def totalScore(self) :  
                        
        self.total = sum( filter(None, self.category.values()))
        self.total += sum( filter(None, [self.threeOfAKind, self.fourOfAKind, self.fullHouse, self.smallStraight, self.largeStraight, self.chance, self.yatesee]))
            
        return self.total
                

class Yatesee() :

    _smallStraights = [
            [1,2,3,4],
            [2,3,4,5],
            [3,4,5,6]
        ]

    _largeStraights = [
            [1,2,3,4,5],
            [2,3,4,5,6]
        ]

    def __init__(self) :
        self.newGame()
        
    def newGame(self) :
        self.score = YateseeScore()
        self.roll = 0
        self.dice = [Die(), Die(), Die(), Die(), Die()]

    def rollDice(self, holdIndexes=[]) :
    
        if self.isGameOver() :
            raise YateseeGameOver()
            
        if self.roll >= 3 :
            raise YateseeRollError(self.roll, "Out of rolls for this turn.")
        
        if holdIndexes and ( max(holdIndexes) > 4 or min(holdIndexes) < 0 ) :
            raise IndexError
                
        for i in range(len(self.dice)) :
            if i not in holdIndexes :
                self.dice[i].roll()
            
        self.roll += 1

    def scoreCategory(self, category) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.category[category] != None :
            raise YateseeScoreError("Category %s has already been scored." % category)
            
        if category not in self.score.category.keys() :
            raise IndexError
            
        self.score.category[category] = self.dice.count(category) * category
        self.roll = 0
        
        catTotal = sum(filter(None, self.score.category.values()))    
        if catTotal >= 63 :
            self.score.categoryBonus = 35
        
        return self.score.totalScore()
        
    def scoreFullHouse(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.fullHouse != None :
            raise YateseeScoreError("Full House has already been scored.")
            
        if self._isFullHouse() :
            self.score.fullHouse = 25
        else :
            self.score.fullHouse = 0
        
        self.roll = 0        
        
        return self.score.totalScore()
        
    def scoreSmallStraight(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.smallStraight != None :
            raise YateseeScoreError("Small Straight has already been scored.")
            
        if self._isSmallStraight() :
            self.score.smallStraight = 30
        else :
            self.score.smallStraight = 0
        
        self.roll = 0        
        
        return self.score.totalScore()
        
    def scoreLargeStraight(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.largeStraight != None :
            raise YateseeScoreError("Large Straight has already been scored.")
            
        if self._isLargeStraight() :
            self.score.largeStraight = 40
        else :
            self.score.largeStraight = 0
        
        self.roll = 0        
        
        return self.score.totalScore()
            
    def scoreThreeOfAKind(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.threeOfAKind != None :
            raise YateseeScoreError("Three of a kind has already been scored.")
                    
        for kind in range(1,7) :
            if self._isKind(kind, 3) :
                self.score.threeOfAKind = sum(self.dice)
                break
            self.score.threeOfAKind = 0
        
        self.roll = 0        
        
        return self.score.totalScore()
        
    def scoreFourOfAKind(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.fourOfAKind != None :
            raise YateseeScoreError("Four of a kind has already been scored.")
                    
        for kind in range(1,7) :
            if self._isKind(kind, 4) :
                self.score.fourOfAKind = sum(self.dice)
                break
            self.score.fourOfAKind = 0
            
        self.roll = 0        
        
        return self.score.totalScore()
        
        
    def scoreChance(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")
            
        if self.score.chance != None :
            raise YateseeScoreError("Chance has already been scored.")
            
        self.score.chance = sum(self.dice)
        
        self.roll = 0        
        
        return self.score.totalScore()

    def scoreYatesee(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")        

        if self.score.yatesee == 0 :
            raise YateseeScoreError("Yatesee has already been scored.")
            
        for kind in range(1,7) :
            if self._isKind(kind, 5) :
                self.score.yateseeCount += 1
                break
         
        if self.score.yateseeCount > 0 :   # 50 for first Yatesee + 100 for each additional Yatesee
            self.score.yatesee = 50 + ((self.score.yateseeCount - 1) * 100)
        else :
            self.score.yatesee = 0
         
        self.roll = 0        
        
        return self.score.totalScore()
        
    def isGameOver(self) :
        if None in self.score.category.values() :
            return False
            
        if None in self.score.__dict__.values() :
            return False
            
        return True

    def _isKind(self, value, count) :
        if self.dice.count(value) >= count :
            return True
            
        return False


    def _isFullHouse(self) :
        for tre in range(1,7) :
            if self._isKind(tre, 3) :
                for duce in range(1,7) :
                    if duce == tre :
                        continue
                    if self._isKind(duce, 2) :
                        return True
                        
        return False

    def _isStraight(self, straights) :
        for s in straights :
            if len(set(s) & set(self.dice)) == len(s) :
                return True
        
        return False

    def _isLargeStraight(self) :
        return self._isStraight(Yatesee._largeStraights)
        
    def _isSmallStraight(self) :
        return self._isStraight(Yatesee._smallStraights)

if __name__ == "__main__" :
    import sys, traceback
    
    def printScore(score) :
        print(score.category)
        print('Bonus:          ', score.categoryBonus)
        print('Three of a kind:', score.threeOfAKind)
        print('Four of a kind: ', score.fourOfAKind)
        print('Full House:     ', score.fullHouse)
        print('Small Straight: ', score.smallStraight)
        print('Large Straight: ', score.largeStraight)
        print('Chance:         ', score.chance)
        print('Yatesee:        ', score.yatesee)
        print('Total:          ', score.total)

    print("Yatesee!  Let's roll!")
    print()
    print("Type '?' for help")
    print()
    game = Yatesee()
    
    while not game.isGameOver() :
        try:
            if game.roll == 0 :
                printScore(game.score)
            else :
                print()
                print("Roll: ", game.roll, game.dice)
            
            
            command = hinput("Enter Yatesee Command: ")
            
            command = command.lower()
            
            if command == 'help' or command == '?' :
                print("Yatesee Commands:")
                print('?          Help')
                print('r          Roll all the dice')
                print('r[1-5]...  Roll holding one or more dice')
                print('1-6        Score Category 1-6')
                print('t          Score three of a kind')
                print('f          Score four of a kind')
                print('h          Score full house')
                print('s          Score small straight')
                print('l          Score large straight')
                print('c          Score chance')
                print('y          Score Yatesee')
                print('q          Quit')
                continue
                
            elif command == 'q' or command == 'quit' :
                print
                print('Quiter')
                print
                quit()
                
            elif command == 'r' or command == 'roll' :
                game.rollDice()   

            elif command[0] == 'r' :
                if game.roll == 0 :
                    print()
                    print('ERROR: You must roll all the dice.')
                    print()
                    continue
                holdIndexes = [int(x)-1 for x in command[1:]]
                game.rollDice(holdIndexes)
        
            elif command in ('1','2','3','4','5','6') :
                game.scoreCategory(int(command))
                           
            elif command == 't' :
                game.scoreThreeOfAKind()
                          
            elif command == 'f' :
                game.scoreFourOfAKind()
                
            elif command == 'h' :
                game.scoreFullHouse()
                
            elif command == 's' :
                game.scoreSmallStraight()
              
            elif command == 'l' :
                game.scoreLargeStraight()
                
            elif command == 'c' :
                game.scoreChance()
                
            elif command == 'y' :
                game.scoreYatesee()
                
            else :
                print()
                print("ERROR: Unknown Command: ", command)
                print()
        except YateseeError as e:
            print()
            print('ERROR:', e.msg)
            print()
            
        except Exception :
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print()
            print("Unknown ERROR:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
            print()
            
    
    print()
    print() 
    printScore(game.score)
    print()
    print("Game Over Dude")

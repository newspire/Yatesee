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

    def current_value(self) :
        return self.val

    def __hash__(self) :
        #print('__hash__', self.val)
        return hash(self.val)

    def __eq__(self, other):
        #print('__eq__', self.val, other)
        if isinstance(other, Die) :
            return self.val == other.val
        return self.val == other

    def __lt__(self, other):
        #print('__lt__', self.val, other)
        if isinstance(other, Die) :
            return self.val < other.val
        return self.val < other

    def __le__(self, other):
        #print('__le__', self.val, other)
        if isinstance(other, Die) :
            return self.val <= other.val
        return self.val <= other

    def __ne__(self, other):
        #print('__ne__', self.val, other)
        if isinstance(other, Die) :
            return self.val != other.val
        return self.val != other

    def __gt__(self, other):
        #print('__gt__', self.val, other)
        if isinstance(other, Die) :
            return self.val > other.val
        return self.val > other

    def __ge__(self, other):
        #print('__ge__', self.val, other)
        if isinstance(other, Die) :
            return self.val >= other.val
        return self.val >= other

    def __and__(self, other):
        #print('__and__', self.val, other)
        if isinstance(other, Die) :
            return self.val == other.val
        return self.val & other

    def __rand__(self, other):
        #print('__rand__', self.val, other)
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
        self.category_bonus = 0
        self.three_of_a_kind = None
        self.four_of_a_kind = None
        self.full_house = None
        self.small_straight = None
        self.large_straight = None
        self.chance = None
        self.yatesee = None
        self.yatesee_count = 0
        self.total = 0


    def total_score(self) :

        self.total = sum( filter(None, self.category.values()))
        self.total += sum( filter(None, [self.three_of_a_kind, self.four_of_a_kind, self.full_house, self.small_straight, self.large_straight, self.chance, self.yatesee]))

        return self.total


class Yatesee() :

    _small_straights = [
            [1,2,3,4],
            [2,3,4,5],
            [3,4,5,6]
        ]

    _large_straights = [
            [1,2,3,4,5],
            [2,3,4,5,6]
        ]

    def __init__(self) :
        self.new_game()

    def new_game(self) :
        self.score = YateseeScore()
        self.roll = 0
        self.dice = [Die(), Die(), Die(), Die(), Die()]

    def roll_dice(self, holdIndexes=[]) :

        if self.is_game_over() :
            raise YateseeGameOver()

        if self.roll >= 3 :
            raise YateseeRollError(self.roll, "Out of rolls for this turn.")

        if holdIndexes and ( max(holdIndexes) > 4 or min(holdIndexes) < 0 ) :
            raise IndexError

        for i in range(len(self.dice)) :
            if i not in holdIndexes :
                self.dice[i].roll()

        self.roll += 1

    def score_category(self, category) :
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
            self.score.category_bonus = 35

        return self.score.total_score()

    def score_full_house(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.full_house != None :
            raise YateseeScoreError("Full House has already been scored.")

        if self._is_full_house() :
            self.score.full_house = 25
        else :
            self.score.full_house = 0

        self.roll = 0

        return self.score.total_score()

    def score_small_straight(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.small_straight != None :
            raise YateseeScoreError("Small Straight has already been scored.")

        if self._is_small_straight() :
            self.score.small_straight = 30
        else :
            self.score.small_straight = 0

        self.roll = 0

        return self.score.total_score()

    def score_large_straight(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.large_straight != None :
            raise YateseeScoreError("Large Straight has already been scored.")

        if self._is_large_straight() :
            self.score.large_straight = 40
        else :
            self.score.large_straight = 0

        self.roll = 0

        return self.score.total_score()

    def score_three_of_a_kind(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.three_of_a_kind != None :
            raise YateseeScoreError("Three of a kind has already been scored.")

        for kind in range(1,7) :
            if self._is_kind(kind, 3) :
                self.score.three_of_a_kind = sum(self.dice)
                break
            self.score.three_of_a_kind = 0

        self.roll = 0

        return self.score.total_score()

    def score_four_of_a_kind(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.four_of_a_kind != None :
            raise YateseeScoreError("Four of a kind has already been scored.")

        for kind in range(1,7) :
            if self._is_kind(kind, 4) :
                self.score.four_of_a_kind = sum(self.dice)
                break
            self.score.four_of_a_kind = 0

        self.roll = 0

        return self.score.total_score()


    def score_chance(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.chance != None :
            raise YateseeScoreError("Chance has already been scored.")

        self.score.chance = sum(self.dice)

        self.roll = 0

        return self.score.total_score()

    def score_yatesee(self) :
        if not self.roll :
            raise YateseeScoreError("You must roll first.")

        if self.score.yatesee == 0 :
            raise YateseeScoreError("Yatesee has already been scored.")

        for kind in range(1,7) :
            if self._is_kind(kind, 5) :
                self.score.yatesee_count += 1
                break

        if self.score.yatesee_count > 0 :   # 50 for first Yatesee + 100 for each additional Yatesee
            self.score.yatesee = 50 + ((self.score.yatesee_count - 1) * 100)
        else :
            self.score.yatesee = 0

        self.roll = 0

        return self.score.total_score()

    def is_game_over(self) :
        if None in self.score.category.values() :
            return False

        if None in self.score.__dict__.values() :
            return False

        return True

    def _is_kind(self, value, count) :
        if self.dice.count(value) >= count :
            return True

        return False


    def _is_full_house(self) :
        for tre in range(1,7) :
            if self._is_kind(tre, 3) :
                for duce in range(1,7) :
                    if duce == tre :
                        continue
                    if self._is_kind(duce, 2) :
                        return True

        return False

    def _is_straight(self, straights) :
        for s in straights :
            if len(set(s) & set(self.dice)) == len(s) :
                return True

        return False

    def _is_large_straight(self) :
        return self._is_straight(Yatesee._large_straights)

    def _is_small_straight(self) :
        return self._is_straight(Yatesee._small_straights)

if __name__ == "__main__" :
    import sys, traceback

    def print_score(score) :
        print(score.category)
        print('Bonus:          ', score.category_bonus)
        print('Three of a kind:', score.three_of_a_kind)
        print('Four of a kind: ', score.four_of_a_kind)
        print('Full House:     ', score.full_house)
        print('Small Straight: ', score.small_straight)
        print('Large Straight: ', score.large_straight)
        print('Chance:         ', score.chance)
        print('Yatesee:        ', score.yatesee)
        print('Total:          ', score.total)

    print("Yatesee!  Let's roll!")
    print()
    print("Type '?' for help")
    print()
    game = Yatesee()

    while not game.is_game_over() :
        try:
            if game.roll == 0 :
                print_score(game.score)
            else :
                print()
                print("Roll: ", game.roll, game.dice)


            command = input("Enter Yatesee Command: ")

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
                game.roll_dice()

            elif command[0] == 'r' :
                if game.roll == 0 :
                    print()
                    print('ERROR: You must roll all the dice.')
                    print()
                    continue
                holdIndexes = [int(x)-1 for x in command[1:]]
                game.roll_dice(holdIndexes)

            elif command in ('1','2','3','4','5','6') :
                game.score_category(int(command))

            elif command == 't' :
                game.score_three_of_a_kind()

            elif command == 'f' :
                game.score_four_of_a_kind()

            elif command == 'h' :
                game.score_full_house()

            elif command == 's' :
                game.score_small_straight()

            elif command == 'l' :
                game.score_large_straight()

            elif command == 'c' :
                game.score_chance()

            elif command == 'y' :
                game.score_yatesee()

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
    print_score(game.score)
    print()
    print("Game Over Dude")

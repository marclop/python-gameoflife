import yaml, os, time, random, uuid, numpy as np


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class animal(object):
    """Animal object expects to receive the world object and
    the possition of the animal as an array"""

    def __init__(self, world, pos=[]):
        self.__liveTurns = 10
        self.__eatHealth = 1
        self.__id = uuid.uuid4()
        self.__symbol = 'A'
        self.__alive = True
        self.__pos = pos
        self.__world = world
        self.__moveDown = None
        self.__moveRight = None
        self.__stayStill = False

    def move(self):
        # Stay or move
        self.__stayStill = bool(random.getrandbits(1))
        self.__moveRight = bool(random.getrandbits(1))
        self.__moveDown = bool(random.getrandbits(1))

        if not self.__stayStill:
            if self.__moveRight:
                self.__pos[1] += 1
            else:
                self.__pos[1] -= 1

            if self.__moveDown:
                self.__pos[0] += 1
            else:
                self.__pos[0] -= 1

        # Implement boundary correction
        # Y correction
        if self.__pos[0] == self.__world.height:
            # random go back
            if bool(random.getrandbits(1)):
                self.__pos[0] -= 2
            else:
                self.__pos[0] -= 1

        # X correction
        if self.__pos[1] == self.__world.width:
            # random go back
            if bool(random.getrandbits(1)):
                self.__pos[1] -= 2
            else:
                self.__pos[1] -= 1

    def showPos(self):
        return self.__pos

    def drawSymbol(self):
        return self.__symbol

    def age(self):
        self.__liveTurns -= 1

    def showId(self):
        return self.__id

    def isAlive(self):
        return self.__alive

    def getAge(self):
        return self.__liveTurns

    def eat(self):
        self.__liveTurns += 1


class plant(object):
    """Plant object expects to receive the world object and
    the possition of the animal as an array"""

    def __init__(self, world, pos=[]):
        self.__symbol = 'P'
        self.__alive = True
        self.__world = world
        self.__pos = pos

    def getEaten(self):
        self.__alive = False

    def isAlive(self):
        return self.__alive

    def showPos(self):
        return self.__pos

    def drawSymbol(self):
        return self.__symbol


class world(object):
    """world object expects to receive the height and width
    of the world that we will instanciate"""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.__rain = False
        self.plantList = []
        self.animalList = []
        self.__days = 0

    def showRain(self):
        return self.__rain

    def showDays(self):
        return self.__days

    def __setRain(self, rain):
        if rain:
            self.__rain = True
        else:
            self.__rain = False

        return self.__rain

    def displayAnimals(self):
        for item in self.animalList:
            print item.showPos()

    def displayPlants(self):
        for item in self.plantList:
            print item.showPos()

    def purgeField(self):

        for a in self.animalList:
            for p in self.plantList:
                # Eat plants
                if p.showPos() == a.showPos():
                    p.getEaten()  # Plant gets eaten
                    a.eat()  # animal eats
                    self.plantList.remove(p)

        # Check duplicates (reproductions)
        for b in self.animalList:
            if a.showPos() == b.showPos() and a.showId() != b.showId():
                # print "duplicate %s ID %s" % (a.showPos(), a.showId())
                # print "duplicate %s ID %s" % (b.showPos(), b.showId())
                self.placeAnimals(self, 1, False, b.showPos())
                # time.sleep(1)

                # Check if possible to compute
    def checkPossible(self, plants, animals):
        if (self.height *
                self.width) <= animals or self.height * self.width <= plants:
            return False
        elif self.height * self.width <= (animals + plants):
            return False
        else:
            return True

    def displayField(self):
        field = np.zeros((self.height, self.width), dtype=np.str)
        # Map
        translation = {'': '-'}

        # Translate
        field = np.vectorize(translation.get)(field)

        for y in xrange(self.height):
            for x in xrange(self.width):

                for value in self.animalList:
                    if value.showPos() == [y, x]:
                        field[y][x] = value.drawSymbol()

                for value in self.plantList:
                    if value.showPos() == [y, x]:
                        field[y][x] = value.drawSymbol()

        return str(field).replace('[[', ' ').replace(']', '').replace(
            '[', '').replace("'", "")

    def placePlants(self, worldName, number):
        for count in xrange(number):
            height = random.randint(0, self.height - 1)
            width = random.randint(0, self.width - 1)
            list = [height, width]
            if self.plantList:
                for value in self.plantList:
                    while list == value.showPos():
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            if self.animalList:
                for value in self.animalList:
                    while list == value.showPos():
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            x = plant(worldName, [height, width])
            self.plantList.append(x)

    def placeAnimals(self, worldName, number, rand=True, xy=[]):
        for count in xrange(number):
            if rand:
                height = random.randint(0, self.height - 1)
                width = random.randint(0, self.width - 1)
            else:
                height = random.randint(xy[0] - 1, xy[0] + 2)
                width = random.randint(xy[1] - 1, xy[1] + 2)

            list = [height, width]

            exit = False
            if self.plantList:
                while not exit:
                    for p in self.plantList:
                        if list == p.showPos():
                            if rand:
                                height = random.randint(0, self.height - 1)
                                width = random.randint(0, self.width - 1)
                            else:
                                height = random.randint(xy[0] - 1, xy[0] + 2)
                                width = random.randint(xy[1] - 1, xy[1] + 2)
                        list = [height, width]
                        exit = False
                    else:
                        exit = True

                if self.animalList:
                    while not exit:
                        for a in self.animalList:
                            if list == a.showPos():
                                if rand:
                                    height = random.randint(0, self.height - 1)
                                    width = random.randint(0, self.width - 1)
                                else:
                                    height = random.randint(xy[0] - 1,
                                                            xy[0] + 2)
                                    width = random.randint(xy[1] - 1,
                                                           xy[1] + 2)
                            list = [height, width]
                            exit = False
                        else:
                            exit = True

            x = animal(worldName, [height, width])
            # if not rand:
            # print "[%s, %s]" % (height, width)
            self.animalList.append(x)

    def spinWorld(self):
        # Make it rain
        if self.__rain:
            self.placePlants(self, 1)

        # Random rain
        if bool(random.getrandbits(1)):
            self.__setRain(True)
        else:
            self.__setRain(False)

        # Move all the animals
        for a in self.animalList:

            a.move()  # Move animal

            self.purgeField()  # purge the field (duplicates and eaten)

            a.age()
            if a.getAge() == 0:
                # Kill old animals
                self.animalList.remove(a)

        # Add a day and return
        self.__days += 1
        return self.__days


# Config Loader
def parseCreds(filename):
    with open(filename, 'r') as conf:
        config = yaml.load(conf)

    return config


# Main execution function
def main():
    # Numpy print options
    np.set_printoptions(threshold='nan')
    fmt = "%s"

    # Load yaml
    config = parseCreds('config.yml')

    # Initialize Earth
    earth = world(config['height'], config['width'])

    # Check if possible to compute
    if not earth.checkPossible(config['plants'], config['animals']):
        print(
            'Impossible to compute %s plants and %s animals in a %s x %s world'
            % (config['plants'], config['animals'], config['height'],
               config['width']))
        return False

    # Initialize World with plants definped in YAML
    earth.placePlants(earth, config['plants'])
    earth.placeAnimals(earth, config['animals'])

    while True:
        time.sleep(config['timer'])
        os.system('clear')
        print "Marc's world"
        print "============="
        if earth.showRain():
            print(bcolors.FAIL + "Raining" + bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + "Not raining" + bcolors.ENDC)
        print "Plants: %s \t Animals: %s" % (len(earth.plantList),
                                             len(earth.animalList))
        print "Elapsed days: %s\n" % (earth.spinWorld())

        print earth.displayField()


if __name__ == "__main__":
    main()

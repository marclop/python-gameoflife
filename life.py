import yaml, os, time, random, pprint, numpy as np


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
        self.__liveTurns = 3
        self.__eatHealth = 1
        self.__symbol = 'A'
        self.__alive = True
        self.__pos = pos
        self.__world = world
        self.__moveDown = None
        self.__moverRight = None

    def move(self):
        movement = random.randint(0, 2)
        print "movement is %s" % movement
        ## Random movement 1 is Vertical
        if movement == 0:
            pass
        elif movement == 1:
            self.__pos[0] = random.randrange(0, (self.__world.height), 1)
        else:
            self.__pos[1] = random.randrange(0, (self.__world.width), 1)

    def showPos(self):
        return self.__pos

    def drawSymbol(self):
        return self.__symbol

    def reproduce(self):
        pass

    def isAlive(self):
        return self.__alive

    def eat(self):
        pass


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
        if rain == True:
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

    ## Check if possible to compute
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
        translation = {'': ' '}

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

        return field

    def placePlants(self, worldName, number):
        for count in xrange(number):
            height = random.randint(0, self.height - 1)
            width = random.randint(0, self.width - 1)
            list = [height, width]
            if self.plantList:
                for value in self.plantList:
                    while list == value.showPos():
                        #print "plant overwrite %s" % list
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            if self.animalList:
                for value in self.animalList:
                    while list == value.showPos():
                        #print "animal-animal overwrite %s" % list
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            x = plant(worldName, [height, width])
            self.plantList.append(x)

    def placeAnimals(self, worldName, number):
        for count in xrange(number):
            height = random.randint(0, self.height - 1)
            width = random.randint(0, self.width - 1)

            list = [height, width]
            if self.plantList:
                for value in self.plantList:
                    while list == value.showPos():
                        #print "animal overwrite %s" % list
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            if self.animalList:
                for value in self.animalList:
                    while list == value.showPos():
                        #print "animal-animal overwrite %s" % list
                        height = random.randint(0, self.height - 1)
                        width = random.randint(0, self.width - 1)
                        list = [height, width]

            x = animal(worldName, [height, width])
            self.animalList.append(x)

    def spinWorld(self):
        ## Make it rain
        if self.__rain:
            self.placePlants(self, 1)

        ## Random rain
        if bool(random.getrandbits(1)):
            self.__setRain(True)
        else:
            self.__setRain(False)

        ## Add a day and return
        self.__days += 1
        return self.__days


## Config Loader
def parseCreds(filename):
    with open(filename, 'r') as conf:
        config = yaml.load(conf)

    return config


## Main execution function
def main():
    ## Numpy print options
    np.set_printoptions(threshold='nan')

    ## Load yaml
    config = parseCreds('config.yml')

    ## Initialize Earth
    earth = world(config['height'], config['width'])

    ## Check if possible to compute
    if not earth.checkPossible(config['plants'], config['animals']):
        print(
            'Impossible to compute %s plants and %s animals in a %s x %s world'
            % (config['plants'], config['animals'], config['height'],
               config['width']))
        return False

    ## Initialize World with plants definped in YAML
    earth.placePlants(earth, config['plants'])
    earth.placeAnimals(earth, config['animals'])

    while True:
        time.sleep(1.5)
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

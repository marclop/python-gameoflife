import yaml, os, time, random, numpy as np

class animal(object):
    """Animal object expects to receive the world object and
    the possition of the animal as an array"""
    def __init__(self, world, pos = []):
        self.__liveTurns = 3
        self.__eatHealth = 1
        self.__symbol = 'A'
        self.__alive = True
        self.__pos = pos
        self.__world = world
        self.__moveDown = None
        self.__moverRight = None

    def move(self):

        movement = random.randint(0,2)
        print "movement is %s" % movement
        ## Random movement 1 is Vertical
        if movement == 0:
            pass
        elif movement == 1:
            self.__pos[0] = random.randrange(0,(self.__world.height), 1)
        else:
            self.__pos[1] = random.randrange(0,(self.__world.width), 1)

    def showPos(self):
        return self.__pos

    def drawSymbol(self):
        return self.__symbol

    def reproduce(self):
        pass

    def eat(self):
        pass


class world(object):
    """world object expects to receive the height and width
    of the world that we will instanciate"""
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.__rain = False
        self.plantList = []
        self.animalList = []

    def showRain(self):
        return self.__rain

    def setRain(self, rain):
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

    def placePlants(self, worldName, number):
        for count in xrange(number):
            height = random.randint(0,number-1)
            width = random.randint(0,number-1)
            list = [height,width]
            if self.plantList:
                for value in self.plantList:
                    while list == value.showPos():
                        #print "plant overwrite %s" % list
                        height = random.randint(0,number-1)
                        width = random.randint(0,number-1)
                        list = [height,width]

            x = plant(worldName, [height, width])
            self.plantList.append(x)

    def placeAnimals(self, worldName, number):
        for count in xrange(number):
            height = random.randint(0,number-1)
            width = random.randint(0,number-1)

            list = [height,width]
            if self.plantList:
                for value in self.plantList:
                    while list == value.showPos():
                        #print "animal overwrite %s" % list
                        height = random.randint(0,number-1)
                        width = random.randint(0,number-1)
                        list = [height,width]

            if self.animalList:
                for value in self.animalList:
                    while list == value.showPos():
                        #print "animal-animal overwrite %s" % list
                        height = random.randint(0,number-1)
                        width = random.randint(0,number-1)
                        list = [height,width]

            x = animal(worldName, [height, width])
            self.animalList.append(x)


class plant(object):
    """docstring for plant"""
    def __init__(self, world, pos = []):
        self.symbol = 'P'
        self.eaten = False
        self.__world = world
        self.__pos = pos

    def eaten(self):
        self.eaten = True

    def showPos(self):
        return self.__pos

## Config Loader
def parseCreds(filename):
    with open(filename, 'r') as conf:
        config = yaml.load(conf)

    return config

## Generate a field with the height and width desired
def generateField(height, width, plants, animals):
    print ("Number of plants is %02d" % plants)
    print ("Number of animals is %02d" % animals)
    print ("Rains: True" + "\n")
    for row in range (0, width):
        for column in range (0, height):
            if column + 1  == width:
                print('- ')
            else:
                print('- '),

## Check if possible to compute
def checkPossible(height, width, plants, animals):
    if (height * width) <= animals or height * width <= plants:
        return False
    elif height * width <= (animals + plants):
        return False
    else:
        return True

## Main execution function
def main():
    config = parseCreds('config.yml')

    earth = world(config['height'], config['width'])
    earth.placePlants(earth, config['plants'])
    earth.placeAnimals(earth, config['animals'])

    print "Animals"
    earth.displayAnimals()
    print "Plants"
    earth.displayPlants()



if __name__ == "__main__":
    main()

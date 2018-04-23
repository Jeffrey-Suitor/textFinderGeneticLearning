# Libraries
import random
from graphics import *


def newChar():  # Removes string characters
    c = random.randint(63,122)

    if c == 63 :  # Replace ? with space
        c = 32
    elif c == 64:  # Replace @ with .
        c = 46
    elif c == 91:  # Replace [ with (
        c = 40
    elif c == 93:  # Replace ] with )
        c = 41
    return chr(c)

class DNA: # DNA Class

    def __init__(self, num):  # Constructor

        self.genes = []
        self.fitness = 0

        for i in range(num):
            self.genes.append(newChar())  # Appends to self.genes list a random list of characters the length of the entered string

    def getPhrase(self):
        return ''.join(self.genes)  # Joins the self.genes characters into a single string

    def calcFitness(self,target):
        score = 0
        for i in range(len(self.genes)):
            if self.genes[i] == target[i]:  # If the character in self.genes matches the string character increment score
                score +=1
        self.fitness = score / len(target)  # Fitness is the score divided by the length of the string

    def crossover(self, partner):
        child = DNA(len(self.genes))  # Creates a new DNA object called child
        midpoint = random.randint(0,len(self.genes)-1)  # Selects a random split point
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child  # Child is a combination of the parent and partner DNA objects

    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if random.random() < mutationRate:
                self.genes[i] = newChar() # Randomly mutates a new character


class newPopulation:  # Population Class

    def __init__(self, phrase, mutation, number):  # Constructor
        self.population = []
        self.matingPool = []
        self.generations = 0
        self.finished = False
        self.target = phrase
        self.mutationRate = mutation
        self.perfectScore = 1
        self.best = ''

        for i in range(number):  # Appends the DNA objects into the population list
            self.population.append(DNA(len(self.target)))

        self.calcFitnessPopulation()  #Calculates the fitness of the population

    def calcFitnessPopulation(self):
        for i in range(len(self.population)):  # Calls the calcFitness mutator of the DNA population
            self.population[i].calcFitness(self.target)


    def naturalSelection(self):
        self.matingPool = []
        maxFitness = 0
        matingSucess = 100
        for i in range(len(self.population)):  # Finds the greatest fitness in a population
            if self.population[i].fitness > maxFitness:
                maxFitness = self.population[i].fitness

        for i in range(len(self.population)):
            fitness = float((self.population[i].fitness/maxFitness))  # Fitness of the DNA object compared to the fittest DNA object
            n = int(fitness *matingSucess)  # matingSucess is a multiplier used to determine how many DNA objects will be available in the mating pool based on their fitness compared to the fittest DNA objects
            for j in range(n):
                self.matingPool.append(self.population[i])

    def generate(self):
        for i in range(len(self.population)):
            a = random.randint(0,len(self.matingPool)-1)  # Randomly selects one member of the mating pool
            b = random.randint(0,len(self.matingPool)-1)  # Randomly selects another member of the mating pool
            partnerA = self.matingPool[a]
            partnerB = self.matingPool[b]
            child = partnerA.crossover(partnerB)  # Crosses the two random members
            child.mutate(self.mutationRate)  # Chance to randomly mutate the child
            self.population[i] = child  # Previous DNA object replaced with new child DNA object
        self.generations += 1



    def evaluate(self):
        worldRecord = 0.0
        index = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > worldRecord:
                index = i
                worldRecord = self.population[i].fitness  # Finds the fittest DNA object so far
        self.best = self.population[index].genes  # Finds fittest DNA object of generation
        for i in range(len(self.population)):
            if worldRecord == self.perfectScore:  # Stop when phrase is reached
                self.finished = True

    def isFinished(self):
        return self.finished  #Checks to see if phrase was found

    def getGenerations(self):
        return self.generations  # Returns generations completed

    def getAverageFitness(self):
        total = 0
        for i in range(len(self.population)):
            total += self.population[i].fitness
        return int(total / len(self.population)*100)  # Calculates average fitness of entire population

    def allPhrases(self):
        everything = ""
        displayLimit = min(len(self.population), 25)
        for i in range(displayLimit):
            everything += str(self.population[i].getPhrase()) +'\n'
        return everything  # Returns the display limit of populations with newline characters


def main():
    phrase = input("What sentence would you like to use:")
    popMax = 200  # Max population
    mutationRate = 0.01  # Mutation rate
    test = newPopulation(phrase, mutationRate, popMax)

    # Graphics
    win = GraphWin('Phrase Finder', 700,600)
    bestPhrase = Text(Point(70,100), "Best phrase:")
    allPhrases = Text(Point(400,100), "All phrases:")
    stats = Text(Point(50,220), "Stats:")
    totalGenerations = Text(Point(120,250), "Total generations:")
    averageFitness = Text(Point(115, 280), "Average fitness:")
    totalPopulation = Text(Point(115,310), "Total population:")
    mutationRateDisplay = Text(Point(105,340),"Mutation rate:")
    mainText = Text(Point(win.getWidth()/2,50),''.join(["Phrase: ",phrase]))
    mainText.setSize(30)
    mutation = Text(Point(209,340),''.join([str(mutationRate*100),'%']))
    population = Text(Point(205, 310), str(popMax))
    bestPhrase.draw(win), allPhrases.draw(win), stats.draw(win),totalGenerations.draw(win),mainText.draw(win)
    averageFitness.draw(win),totalPopulation.draw(win),population.draw(win), mutation.draw(win),mutationRateDisplay.draw(win)
    answer = Text(Point(300, 30),'')
    generation = Text(Point(150,250),str(test.getGenerations()))
    fitness = Text(Point(145,280), str(test.getAverageFitness()))
    everyPhrase = Text(Point(500,100),str(test.allPhrases()))


    while test.isFinished() != True:
        generation.undraw()
        everyPhrase.undraw()
        answer.undraw()
        fitness.undraw()
        test.naturalSelection()
        test.generate()
        test.calcFitnessPopulation()
        test.evaluate()
        answer = Text(Point(190,100), ''.join(test.best))
        generation = Text(Point(202, 250), str(test.getGenerations()))
        fitness = Text(Point(213, 280), ''.join([str(test.getAverageFitness()),'%']))
        everyPhrase = Text(Point(520, 325), str(test.allPhrases()))
        answer.draw(win), generation.draw(win), fitness.draw(win), everyPhrase.draw(win)
        time.sleep(0.05)

    input("Press any key to exit")

main()

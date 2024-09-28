import random

class KingsDecision:
    def __init__(self, description, people_reaction, how_wise):
        self.description = description
        self.people_reaction = people_reaction
        self.how_wise = how_wise
    def getDescription(self):
        return self.description
    def getPeopleReaction(self):
        return self.people_reaction
    def getHowWise(self):
        return self.how_wise


class Population:
    def __init__(self, start_population):
        self.population = start_population
        self.healthy = start_population
        self.convalescents = 0
        self.sick = 0
        self.is_epidemy = False
        self.beta = 0
        self.gamma = 0
        self.lethality = 0.3
        self.reset_epidemy = False
        self.dead = 0

    def reset(self):
        self.healthy = self.population
        self.convalescents = 0
        self.sick = 0
        self.dead = 0

    def startEpidemy(self,  beta, gamma, lethality=0.3):
        self.healthy -= 5
        self.sick += 5
        self.is_epidemy = True
        self.beta = beta
        self.gamma = gamma
        self.lethality = lethality

    def moddedSIR(self):
        beta = self.beta
        gamma = self.gamma
        lethality = self.lethality
        if(self.sick == 0):
            self.is_epidemy = False
            self.reset_epidemy = True
            return
        # Oblicz nowe zakażenia i wyzdrowienia
        self.dead = round(lethality*self.sick)
        self.sick -= self.dead
        self.population -= self.dead
        new_infected = round(beta * self.healthy * self.sick / self.population)
        new_recovered = round(gamma * self.sick)

        # Aktualizacja stanów, upewniając się, że nie przekraczamy dostępnych zasobów
        self.healthy = max(0, self.healthy - new_infected)
        self.sick = max(0, self.sick + new_infected - new_recovered)
        self.convalescents = min(self.population, self.convalescents + new_recovered)

    def getPopulation(self):
        return self.population

    def getIsEpidemy(self):
        return self.is_epidemy

    def plagueNow(self, defensebility):
        self.population -= int((1-defensebility)*self.population)

    def populationGrowth(self, culturality):
        if not self.is_epidemy:
            self.population += round(culturality*self.population)
            pass


class State:

    def __init__(self, start_population=10):
        self.population = Population(start_population)
        self.history_of_decisions = []
        self.history_of_events = []

        self.hospitals = 15
        self.culture = 15
        self.defense = 15
        self.technology = 15

        self.coins = 100

        self.time_from_last_plague = 0
        self.time_from_last_epidemy = 0

    def moneyProfit(self):
        self.coins += round(self.tech/3 + self.culture/4 + (self.tech*self.culture)/6)*(self.population+1)

    def spendMoneyOn(self, donations):
        self.coins -= int(donations["technology"] - donations["culture"] - donations["defense"] - donations["hospital"])
        decay = 0.7
        self.culture += decay*self.culture + int(donations["culture"] - 30)
        self.technology += decay*self.technology + int(donations["technology"] - 30)
        self.defense += decay*self.defense + int(donations["defense"] - 30)
        self.hospitals += decay*self.hospitals + int(donations["hospitals"] - 30)
    
    def nextStep(self, donations):
        self.spendMoneyOn(donations)
        self.moneyProfit()
        culturality = max(0.07, max(0,self.culture-4)/15)
        if(not self.population.getIsEpidemy()):
            probablity_of_plague = min(0.4, max(0, self.time_from_last_plague-7)/20)
            if(random.random() < probablity_of_plague):
                defensibility = max(1, min(0, self.defense - 5)/20)
                self.population.plagueNow(defensibility)
                self.time_from_last_plague = 0
                self.time_from_last_epidemy += 1
            else:
                self.time_from_last_plague += 1 
                probablity_of_epidemy = min(0.3, max(0, self.time_from_last_plague-8)/20)
                if (random.random() < probablity_of_epidemy):
                    beta = 0.3
                    gamma = max(1, min(0, self.hospitals - 5)/20)
                    self.population.startEpidemy(beta, gamma)
                else:
                    self.population.populationGrowth(culturality)
                    self.time_from_last_epidemy += 1

        elif(self.population.reset_epidemy):
            self.time_from_last_epidemy = 0
            self.population.reset_epidemy = False
            self.time_from_last_plague += 1
        else:
            self.time_from_last_plague += 1
            self.time_from_last_epidemy += 1
            self.population.populationGrowth(culturality)




        


    




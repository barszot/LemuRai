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
        self.is_plague = False
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
        self.dead = int((1-defensebility)*self.population)
        self.population -= self.dead
        self.is_plague = True

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
        self.coins += round(self.technology/3 + self.culture/4 + (self.technology*self.culture)/6)*(self.population.population+1)

    def spendMoneyOn(self, donations):
        # Użycie get() z wartością domyślną 0 dla każdego klucza
        tech = donations.get("technologia", 0)
        kultura = donations.get("kultura", 0)
        ochrona = donations.get("ochrona", 0)
        szpitale = donations.get("szpitale", 0)
        
        # Obliczenie wydatków i aktualizacja coins
        self.coins -= int(tech - kultura - ochrona - szpitale)

        decay = 0.7
        
        # Aktualizacja wartości z zachowaniem minimum 0
        self.culture = max(0, self.culture + int( decay * self.culture +kultura - 30))
        self.technology = max(0, self.technology + int(decay * self.technology + tech - 30))
        self.defense = max(0, self.defense + int(decay * self.defense + ochrona - 30))
        self.hospitals = max(0, self.hospitals + int( decay * self.hospitals + szpitale - 30))

    
    def nextStep(self, donations):
        self.spendMoneyOn(donations)
        self.moneyProfit()
        culturality = max(0.07, max(0,self.culture-4)/15)
        self.population.dead = 0
        self.population.is_plague = False
        if(not self.population.getIsEpidemy()):
            probablity_of_plague = min(0.4, max(0, self.time_from_last_plague-8)/15)
            if(random.random() < probablity_of_plague):
                defensibility = max(1, min(0, self.defense - 5)/20)
                self.population.plagueNow(defensibility)
                self.time_from_last_plague = 0
                self.time_from_last_epidemy += 1
            else:
                self.time_from_last_plague += 1 
                probablity_of_epidemy = min(0.3, max(0, self.time_from_last_plague-10)/10)
                if (random.random() < probablity_of_epidemy):
                    beta = 0.3
                    gamma = max(0.2, self.hospitals - 5)/20
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

    def __str__(self):
        dict = {
            "pieniądze": self.coins,
            "populacja": self.population.population,
            "czy-teraz-jest-epidemia": "prawda" if self.population.is_epidemy else "fałsz",
            "czy-teraz-jest-klęska-żywiołowa": "prawda" if self.population.is_plague else "fałsz",
            "jaki-odsetek-populacji-umarł": f"{int(self.population.dead/self.population.population*100)}%",
            "punkty-kultury": self.culture,
            "punkty-technologii": self.technology,
            "punkty-szpitalne": self.hospitals,
            "punkty-ochrony": self.defense
        }
        return str(dict)

    def printStats(self):
        gamma = max(0.2, self.hospitals - 5)/20
        print("GAMMA: ", gamma)
        earn = round(self.technology/3 + self.culture/4 + (self.technology*self.culture)/6)*(self.population.population+1)
        print("EARN: ", earn)
        probablity_of_plague = min(0.4, max(0, self.time_from_last_plague-8)/15)
        print("PROBABILITY OF PLAGUE: ", probablity_of_plague)
        probablity_of_epidemy = min(0.3, max(0, self.time_from_last_plague-10)/10)
        print("PROBABILITY OF EPIDEMY: ", probablity_of_epidemy)


    




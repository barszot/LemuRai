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

    def reset(self):
        self.healthy = self.population
        self.convalescents = 0
        self.sick = 0

    def startEpidemy(self):
        self.healthy -= 5
        self.sick += 5
        self.is_epidemy = True

    def moddedSIR(self, beta, gamma, lethality=0.3):
        if(self.sick == 0):
            self.is_epidemy = False
            return
        # Oblicz nowe zakażenia i wyzdrowienia
        dead = round(lethality*self.sick)
        self.sick -= dead
        self.population -= dead
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
        self.population -= int(defensebility*self.population)

    def populationGrowth(self, culturality):
        if not self.is_epidemy:
            self.population += culturality*self.population
            pass


class State:

    def __init__(self, start_population=10):
        self.population = start_population
        self.history_of_decisions = []
        self.history_of_events = []

        self.hospitals = 10
        self.culture = 10
        self.defense = 10
        self.technology = 0
        self.devastation_level = 0.0

        self.coins = 100
        self.situation = """
            hello, fdsagifdaoiad
        """
        self.time_from_last_plague = 0
        self.time_from_last_epidemy = 0

    def moneyProfit(self):
        return (self.tech/3 + self.culture/4 + (self.tech*self.culture)/6)*self.population

    def spendMoneyOn(self, donations):
        self.coins -= int(donations["technology"] - donations["culture"] - donations["defense"] - donations["hospital"])
        self.culture += int(donations["culture"] - 30)
        self.technology += int(donations["technology"] - 30)
        self.defense += int(donations["defense"] - 30)
        self.hospitals += int(donations["hospitals"] - 30)
    
    def nextStep(self):
        pass
    




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



class State:
    def __init__(self, start_population=10):
        self.population = start_population
        self.history_of_decisions = []
        self.history_of_events = []
        self.health = 0
        self.devastation_level = 0.0
        self.eco_defense = 10
        self.food = start_population
        self.water = start_population
        self.culture = 0
        self.tech = 0
        self.coins = 100
        self.situation = """
            hello, fdsagifdaoiad
        """

    # Gettery
    def getPopulation(self):
        return self.population

    def getHistoryOfDecisions(self):
        return self.history_of_decisions

    def getHistoryOfEvents(self):
        return self.history_of_events

    def getHealth(self):
        return self.health

    def getDevastationLevel(self):
        return self.devastation_level

    def getFood(self):
        return self.food

    def getWater(self):
        return self.water

    def getCulture(self):
        return self.culture

    def getTech(self):
        return self.tech

    def getCoins(self):
        return self.coins

    def getSituation(self):
        return self.situation

    def moneyProfit(self):
        return self.tech/100 + self.culture/200 + (self.tech*self.culture)/500

    def spendMoneyOn(self, type):
        pass

NUM_PLAYERS = 15

# performs algorithm to choose players, based on their predicted scores created in the pointsPredictor
class Picker:
    def __init__(self, goalkeepers, defenders, midfielders, forwards) -> None:
        self.budget = 100000000
        self.positionAllocations = (2, 5, 5, 3) # picks 4-4-2 formation with 1 sub each
        # position budgets will be used as the budget allocated in the Knapsack problem selection
        self.positionBudgets = (self.budget * self.positionAllocations[0]/ NUM_PLAYERS,self.budget * self.positionAllocations[1] / NUM_PLAYERS,
                                self.budget * self.positionAllocations[2]/ NUM_PLAYERS, self.budget * self.positionAllocations[3]/ NUM_PLAYERS)
        
        print(self.positionBudgets)
        
        # storing data frames of each position
        self.goalkeepers = goalkeepers
        self.defenders = defenders
        self.midfielders = midfielders
        self.forwards = forwards
        
        self.sortLists()
        
    # sorts list by predicted score (won't make an effect until I calculate predicted score differently then initial setup)
    def sortLists(self):
        self.goalkeepers = self.goalkeepers.sort_values(by='predicted_score', ascending=False)
        self.defenders = self.defenders.sort_values(by='predicted_score', ascending=False)
        self.midfielders = self.midfielders.sort_values(by='predicted_score', ascending=False)
        self.forwards = self.forwards.sort_values(by='predicted_score', ascending=False)
        
    # deploys greedy algorithm to get one of the best (not necessarily the absolute best) predicted subset of players
    def pickTeam(self):
        budgetSpent = 0
        
        gkInd = defInd = midInd = forInd = 0
        self.goalkeepersChosen = [] # really should just be one, just using an array for consistency
        self.defendersChosen = []
        self.midfieldersChosen = []
        self.forwardsChosen = []
        
        # greedy algorithm to pick players
        # initial allocations -- starts off with highest predicted socres
        for i in range(self.positionAllocations[0]):
            self.goalkeepersChosen.append(i)
            
        for i in range(self.positionAllocations[1]):
            self.defendersChosen.append(i)
            
        for i in range(self.positionAllocations[2]):
            self.midfieldersChosen.append(i)
            
        for i in range(self.positionAllocations[3]):
            self.forwardsChosen.append(i)  
            
        goalkeepersCost, defendersCost, midfielderCost, forwardsCost, totalCost = self.getTeamCosts(self.goalkeepersChosen, 
                                                                    self.defendersChosen, self.midfieldersChosen, self.forwardsChosen)
        
        # if best team is over the budget, perform the following greedy algorithm until it is below the budget
        while (totalCost > self.budget):
            # multipliers are the ratio of how underpriced/overpriced each position is (which to increment)
            goalkeeperMult = goalkeepersCost/self.positionBudgets[0]
            defenderMult = defendersCost/self.positionBudgets[1]
            midfielderMult = midfielderCost/self.positionBudgets[2]
            forwardsMult = forwardsCost/self.positionBudgets[3]
            
            print(goalkeeperMult, defenderMult, midfielderMult, forwardsMult)
            
            # determine what position is the most overspent on relative to its budget and change those associated players
            highestMultInd = self.getMaxVal(goalkeeperMult, defenderMult, midfielderMult, forwardsMult)
            
            print(highestMultInd)
            
            if highestMultInd == 0:
                for i in range(len(self.goalkeepersChosen)):
                    self.goalkeepersChosen[i] += 1
            elif highestMultInd == 1:
                for i in range(len(self.defendersChosen)):
                    self.defendersChosen[i] += 1
            elif highestMultInd == 2:
                for i in range(len(self.midfieldersChosen)):
                    self.midfieldersChosen[i] += 1
            else:
                for i in range(len(self.forwardsChosen)):
                    self.forwardsChosen[i] += 1
                    
            # checking cost again to see if this complies with the rules
            goalkeepersCost, defendersCost, midfielderCost, forwardsCost, totalCost = self.getTeamCosts(self.goalkeepersChosen, 
                                                                    self.defendersChosen, self.midfieldersChosen, self.forwardsChosen)
            
            print("Current cost is ", totalCost)
            
        print("Total cost is ", totalCost)
            
    # checks team cost so that we can see if it is over 100 million
    def getTeamCosts(self, goalkeepersChosen, defendersChosen, midfieldersChosen, forwardsChosen):
        goalkeepersCost = 0
        defendersCost = 0
        midfieldersCost = 0
        forwardsCost = 0
        
        for i in goalkeepersChosen:
            goalkeepersCost += (self.goalkeepers.iloc[i])['player_price']
            
        for i in defendersChosen:
            defendersCost += (self.defenders.iloc[i])['player_price']
            
        for i in midfieldersChosen:
            midfieldersCost += (self.midfielders.iloc[i])['player_price']
            
        for i in forwardsChosen:
            forwardsCost += (self.forwards.iloc[i])['player_price']
            
        print(goalkeepersCost, defendersCost, midfieldersCost, forwardsCost)
            
        totalCost = goalkeepersCost + defendersCost + midfieldersCost + forwardsCost
        
        return goalkeepersCost, defendersCost, midfieldersCost, forwardsCost, totalCost
    
    # gets 4 values (really just for the 4 multiplier values and returns 0, 1, 2, or 3 depending on what is the largest)
    def getMaxVal(self, val1, val2, val3, val4):
        maxInd = 0
        maxVal = val1
        
        if val2 > maxVal:
            maxVal = val2
            maxInd = 1
            
        if val3 > maxVal: 
            maxVal = val3
            maxInd = 2
            
        if val4 > maxVal:
            maxVal = val4
            maxInd = 3
            
        return maxInd